import requests
import json

def get_courses(username, password, action, relogin=False, date=None):
    url = 'http://127.0.0.1:5000/get_courses'
    headers = {'Content-Type': 'application/json'}
    data = {
        'username': username,
        'password': password,
        'action': action,
        'relogin': relogin
    }
    if date:
        data['date'] = date

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# 示例用法
username = '2301123104'
password = 'Ryancuee85173'

# 获取今天的课程
print('今天的课程:')
print(get_courses(username, password, 'today'))

# 获取当前课程
print('当前的课程:')
print(get_courses(username, password, 'current'))

# 获取接下来的课程
print('接下来的课程:')
print(get_courses(username, password, 'next'))

# 获取指定日期的课程
print('2024-08-30的课程:')
print(get_courses(username, password, 'on_date', date='2024-08-30'))
