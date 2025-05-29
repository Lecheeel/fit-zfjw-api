import sys
import os
from pathlib import Path

# 添加包路径以支持独立运行
if __name__ == '__main__':
    # 当作为脚本直接运行时，添加父目录到sys.path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

from flask import Flask, request, jsonify
import json
from datetime import datetime

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .JWGL_Client import JWGLClient
    from .schedule_manager import ScheduleManager
    from .configs.settings import BASE_URL, START_DATE
except ImportError:
    # 作为脚本运行时的绝对导入
    from fit_zfjw_api.JWGL_Client import JWGLClient
    from fit_zfjw_api.schedule_manager import ScheduleManager
    from fit_zfjw_api.configs.settings import BASE_URL, START_DATE

app = Flask(__name__)

def save_to_file(data, filename, indent=None):
    """Save data to a file with indentation."""
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def load_from_file(filename):
    """Load data from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def course_to_dict(course):
    return {
        'name': course.name,
        'teacher': course.teacher,
        'classroom': course.classroom,
        'weekdays': list(course.weekdays),
        'periods': course.periods
    }

@app.route('/get_courses', methods=['POST'])
def get_courses():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    action = data.get('action')
    relogin = data.get('relogin', False)

    # 获取当前脚本的目录
    current_dir = Path(__file__).parent
    # 确定data目录的位置
    if current_dir.name == 'fit_zfjw_api':
        # 如果在fit_zfjw_api目录内运行，data目录在上级目录
        data_dir = current_dir.parent / 'data'
    else:
        # 如果在项目根目录运行，data目录在当前目录
        data_dir = current_dir / 'data'
    
    schedule_file = data_dir / f'{username}_schedule.json'

    # Check if the schedule file exists and no relogin is requested
    if schedule_file.exists() and not relogin:
        schedule = load_from_file(schedule_file)
    else:
        # Create an instance of the JWGLClient with user credentials
        client = JWGLClient(BASE_URL, username, password)
        main_page = client.login()

        if main_page.status_code != 200:
            return jsonify({'error': 'Login failed'}), 401

        # Get the schedule and save it
        schedule_response = client.get_schedule()
        schedule = schedule_response.json()
        save_to_file(schedule, str(schedule_file), indent=4)

    # Create ScheduleManager instance
    manager = ScheduleManager(str(schedule_file), start_date=START_DATE)

    # Perform the requested action
    if action == "today":
        courses_today = manager.get_courses_on_date(datetime.now().date())
        courses_today_dict = [course_to_dict(course) for course in courses_today]
        return jsonify(courses_today_dict)
    
    elif action == "current":
        current_time = datetime.now()
        current_course = manager.get_course(current_time)
        if current_course:
            return jsonify({'current_course': current_course.name})
        else:
            return jsonify({'current_course': 'None'})
    
    elif action == "next":
        current_time = datetime.now()
        next_courses = manager.get_next_courses(current_time)
        return jsonify({'next_courses': [course.name for course in next_courses]})

    elif action == "on_date":
        specific_date = data.get('date')
        if specific_date:
            date = datetime.strptime(specific_date, '%Y-%m-%d').date()
            courses_on_date = manager.get_courses_on_date(date)
            courses_today_dict = [course_to_dict(course) for course in courses_on_date]
            return jsonify(courses_today_dict)
        else:
            return jsonify({'error': 'Date not provided'}), 400

    elif action == "full_schedule":
        # 获取完整学期课表
        full_schedule = manager.get_full_semester_schedule()
        return jsonify(full_schedule)

    return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8072)
