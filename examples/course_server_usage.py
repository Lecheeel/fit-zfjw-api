import requests
import json

def get_courses(username, password, action, relogin=False, force_update=False, date=None):
    url = 'http://127.0.0.1:8072/get_courses'
    headers = {'Content-Type': 'application/json'}
    data = {
        'username': username,
        'password': password,
        'action': action,
        'relogin': relogin,
        'force_update': force_update
    }
    if date:
        data['date'] = date

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# 示例用法
username = ''
password = ''

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
print('2025-05-29的课程:')
print(get_courses(username, password, 'on_date', date='2025-05-29'))

# 获取完整学期课表
print('\n' + '='*50)
print('完整学期课表:')
print('='*50)
full_schedule = get_courses(username, password, 'full_schedule')

if 'error' not in full_schedule:
    # 显示学期基本信息
    semester_info = full_schedule['semester_info']
    print(f"学期开始日期: {semester_info['start_date']}")
    print(f"当前第 {semester_info['current_week']} 周")
    print(f"课程总数: {semester_info['total_courses']} 门")
    print('\n课程详细信息:')
    print('-' * 80)
    
    # 显示每门课程的详细信息
    for i, course in enumerate(full_schedule['courses'], 1):
        print(f"{i}. {course['name']}")
        print(f"   任课教师: {course['teacher']}")
        print(f"   上课教室: {course['classroom']}")
        print(f"   上课周次: {course['formatted_info']['weeks_text']}")
        print(f"   上课时间: {course['formatted_info']['weekdays_text']} {course['formatted_info']['periods_text']}")
        print(f"   具体时间: {course['formatted_info']['time_text']}")
        print()
else:
    print(f"获取完整课表失败: {full_schedule['error']}")

print('='*50)

# 强制更新课表缓存后获取今天的课程
print('\n强制更新课表后，今天的课程:')
print(get_courses(username, password, 'today', force_update=True))
