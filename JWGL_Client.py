import requests
import rsa
import binascii
from pyquery import PyQuery as pq
from io import BytesIO
import ddddocr
from datetime import datetime
import json

class JWGLClient:
    def __init__(self, base_url, account, password):
        self.base_url = base_url
        self.account = account
        self.password = password
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
        self.login_url = f'{base_url}/xtgl/login_slogin.html'
        self.key_url = f'{base_url}/xtgl/login_getPublicKey.html'
        self.captcha_url = f'{base_url}/kaptcha'
        self.inf_url = f'{base_url}/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801'
        self.schedule_url = f'{base_url}/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151&su={self.account}'

    def get_csrf_token_and_public_key(self):
        res = self.session.get(self.login_url, headers=self.headers)
        doc = pq(res.text)
        csrf_token = doc('#csrftoken').attr('value')

        res = self.session.get(self.key_url, headers=self.headers)
        data = res.json()
        modulus = data.get("modulus")
        exponent = data.get("exponent")

        return csrf_token, modulus, exponent

    def get_captcha(self):
        ocr = ddddocr.DdddOcr()
        res = self.session.get(self.captcha_url, headers=self.headers)
        with BytesIO(res.content) as image_stream:
            captcha = ocr.classification(image_stream.read())
        return captcha

    def encrypt_password(self, pwd, modulus, exponent):
        message = str(pwd).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(modulus))
        rsa_e = binascii.b2a_hex(binascii.a2b_base64(exponent))
        key = rsa.PublicKey(int(rsa_n, 16), int(rsa_e, 16))
        encropy_pwd = rsa.encrypt(message, key)
        result = binascii.b2a_base64(encropy_pwd)
        return result

    def login(self):
        csrf_token, modulus, exponent = self.get_csrf_token_and_public_key()
        captcha = self.get_captcha()
        encrypted_pwd = self.encrypt_password(self.password, modulus, exponent)
        login_data = {
            "csrftoken": csrf_token,
            "yhm": self.account,
            "mm": encrypted_pwd,
            "yzm": captcha,
        }
        res = self.session.post(self.login_url, headers=self.headers, data=login_data)
        return res

    def get_schedule(self):
        current_date = datetime.now()
        xqm = '12' if 2 <= current_date.month <= 8 else '3'
        xnm = str(current_date.year - 1)
        data = {'xnm': xnm, 'xqm': xqm}
        res = self.session.post(self.schedule_url, headers=self.headers, data=data)
        return res

    def get_info(self):
        res = self.session.get(self.inf_url, headers=self.headers)
        doc = pq(res.text)

        info_elements = doc('.form-control-static')
        student_info = {}
        for element in info_elements.items():
            label = element.parent().prev().text().strip()
            value = element.text().strip()
            student_info[label] = value

        student_info = {key: value for key, value in student_info.items() if value}
        return student_info
