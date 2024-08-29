import requests
import rsa
import binascii
from pyquery import PyQuery as pq
from io import BytesIO
import ddddocr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JWGLClient:
    def __init__(self, base_url, account, password):
        self.base_url = base_url
        self.account = account
        self.password = password
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }
        self.login_url = f'{base_url}/xtgl/login_slogin.html'
        self.areaone_url = f'{base_url}/xtgl/index_cxAreaOne.html'
        self.key_url = f'{base_url}/xtgl/login_getPublicKey.html'
        self.captcha_url = f'{base_url}/kaptcha'
        self.inf_url = f'{base_url}/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801'
        self.schedule_url = f'{base_url}/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151&su={self.account}'
        self.xnm = None
        self.xqm = None

    def get_csrf_token_and_public_key(self):
        try:
            res = self.session.get(self.login_url, headers=self.headers)
            res.raise_for_status()
            doc = pq(res.text)
            csrf_token = doc('#csrftoken').attr('value')

            res = self.session.get(self.key_url, headers=self.headers)
            res.raise_for_status()
            data = res.json()
            modulus = data.get("modulus")
            exponent = data.get("exponent")

            if not all([csrf_token, modulus, exponent]):
                raise ValueError("Failed to retrieve necessary authentication data.")

            return csrf_token, modulus, exponent
        except Exception as e:
            logging.error(f"Error in get_csrf_token_and_public_key: {e}")
            raise

    def get_captcha(self):
        try:
            ocr = ddddocr.DdddOcr()
            res = self.session.get(self.captcha_url, headers=self.headers)
            res.raise_for_status()
            with BytesIO(res.content) as image_stream:
                captcha = ocr.classification(image_stream.read())
            return captcha
        except Exception as e:
            logging.error(f"Error in get_captcha: {e}")
            raise

    def encrypt_password(self, pwd, modulus, exponent):
        try:
            message = pwd.encode()
            rsa_n = int(binascii.hexlify(binascii.a2b_base64(modulus)), 16)
            rsa_e = int(binascii.hexlify(binascii.a2b_base64(exponent)), 16)
            key = rsa.PublicKey(rsa_n, rsa_e)
            encrypted_pwd = rsa.encrypt(message, key)
            return binascii.b2a_base64(encrypted_pwd).decode().strip()
        except Exception as e:
            logging.error(f"Error in encrypt_password: {e}")
            raise

    def login(self):
        try:
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
            res.raise_for_status()

            cx_data = {
                "localeKey": "zh_CN",
                "gnmkdm": "index",
            }
            res = self.session.post(self.areaone_url, headers=self.headers, data=cx_data)
            res.raise_for_status()
            doc = pq(res.text)
            self.xnm = doc('input[name="xnm"]').val()
            self.xqm = doc('input[name="xqm"]').val()

            logging.info(f"Login successful: xnm: {self.xnm}, xqm: {self.xqm}")
            return res
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise

    def get_schedule(self):
        if not self.xnm or not self.xqm:
            logging.error("Schedule retrieval failed: xnm or xqm not set. Ensure you are logged in.")
            return None

        try:
            data = {'xnm': self.xnm, 'xqm': self.xqm}
            res = self.session.post(self.schedule_url, headers=self.headers, data=data)
            res.raise_for_status()
            return res
        except Exception as e:
            logging.error(f"Error in get_schedule: {e}")
            raise

    def get_info(self):
        try:
            res = self.session.get(self.inf_url, headers=self.headers)
            res.raise_for_status()
            doc = pq(res.text)

            student_info = {}
            for element in doc('.form-control-static').items():
                label = element.parent().prev().text().strip()
                value = element.text().strip()
                if value:
                    student_info[label] = value

            return student_info
        except Exception as e:
            logging.error(f"Error in get_info: {e}")
            raise
