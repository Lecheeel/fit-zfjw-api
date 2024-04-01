# Import the JWGLClient class from the JWGL_Client module
from JWGL_Client import JWGLClient
import json  # Import the json module

# Define your account credentials and the base URL for the JWGL system
account = 'your_account'
password = 'your_password'
base_url = 'http://oaa.fitedu.net/jwglxt'

# Create an instance of the JWGLClient with your credentials
client = JWGLClient(base_url, account, password)

# Attempt to login
main_page = client.login()

# Check if the login was successful
if main_page.status_code == 200:
    print('Login result: ok')

    # Get the schedule and print it
    schedule = client.get_schedule().json()
    #print('Schedule:', schedule)

    # Save the schedule to a local file
    with open('schedule.json', 'w') as f:
        json.dump(schedule, f)

    # Get the student info and print it
    info = client.get_info()
    print('Student Info:', info)

    # Save the student info to a local file
    with open('info.json', 'w') as f:
        json.dump(info, f)
else:
    print('Login failed')