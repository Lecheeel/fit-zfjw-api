from flask import Flask, request, jsonify
from JWGL_Client import JWGLClient
from schedule_manager import ScheduleManager
import json
import os
from datetime import datetime
from configs.settings import BASE_URL

app = Flask(__name__)

def save_to_file(data, filename, indent=None):
    """Save data to a file with indentation."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def load_from_file(filename):
    """Load data from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/get_courses', methods=['POST'])
def get_courses():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    action = data.get('action')
    relogin = data.get('relogin', False)

    # Define the base URL for the JWGL system
    schedule_file = f'../data/{username}_schedule.json'

    # Check if the schedule file exists and no relogin is requested
    if os.path.exists(schedule_file) and not relogin:
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
        save_to_file(schedule, schedule_file, indent=4)

    # Create ScheduleManager instance
    manager = ScheduleManager(schedule_file, start_date="2024-08-26")

    # Perform the requested action
    if action == "today":
        courses_today = manager.get_courses_on_date(datetime.now().date())
        return jsonify({'courses_today': [course.name for course in courses_today]})
    
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
            return jsonify({'courses_on_date': [course.name for course in courses_on_date]})
        else:
            return jsonify({'error': 'Date not provided'}), 400

    return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
