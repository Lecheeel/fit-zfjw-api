# Import the JWGLClient class from the JWGL_Client module
from JWGL_Client import JWGLClient
import json  # Import the json module

def save_to_file(data, filename, indent=None):
    """Save data to a file with indentation."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

# Define your account credentials and the base URL for the JWGL system
account = ''
password = ''
base_url = 'http://oaa.fitedu.net/jwglxt'

# Create an instance of the JWGLClient with your credentials
client = JWGLClient(base_url, account, password)

# Attempt to login
main_page = client.login()

# Check if the login was successful
if main_page.status_code == 200:
    print('Login result: ok')

    # Get the schedule
    schedule_response = client.get_schedule()

    if schedule_response.status_code == 200:
        schedule = schedule_response.json()
        # print('Schedule:', schedule)
        save_to_file(schedule, 'schedule.json', indent=4)
        print("Schedule loaded and saved successfully.")
    else:
        print('Failed to get schedule:', schedule_response.status_code)

    # Get the student info
    info = client.get_info()

    if info:
        print('Student Info:')
        for key, value in info.items():
            print(f"{key} {value}")
        # save_to_file(info, 'info.json', indent=4)
        # print("Student info loaded and saved successfully.")
    else:
        print('Failed to get student info.')
else:
    print('Login failed')
