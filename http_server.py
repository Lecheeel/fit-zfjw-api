from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from JWGL_Client import JWGLClient
from schedule_manager import ScheduleManager
from datetime import datetime,timedelta
import json,os

# Define the base URL for the JWGL system
base_url = 'http://oaa.fitedu.net/jwglxt'

# Dictionary to store already logged in accounts
logged_in_accounts = {}

class RequestHandler(BaseHTTPRequestHandler):
    def save_to_file(self, data, filename, indent=None):
        """Save data to a file with indentation."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    def acc_login(self,query_params):
        account = query_params['acc'][0]
        password = query_params['psw'][0]
        client = JWGLClient(base_url, account, password)
        main_page = client.login()
        if main_page.status_code == 200:
            logged_in_accounts[account] = True
            if not os.path.isfile(f"{account}.json"):
                schedule_response = client.get_schedule()
                try:
                    schedule = schedule_response.json()
                    self.save_to_file(schedule, f"{account}.json", indent=4)
                    print(f"Schedule for account {account} saved successfully.")
                except json.JSONDecodeError:
                    print('Failed to parse schedule:', schedule_response.text)
        
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            if ('acc' not in query_params )or ('psw' not in query_params):
                print("'acc' and 'psw' parameter is required for initializing the schedule.")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes("Bad request. 'acc' and 'psw' parameter is required for initializing the schedule.", "utf-8"))
            else:
                print('check acc and psw is ok.')
                account = query_params['acc'][0]
                if (os.path.isfile(f"{account}.json")):
                    print(f"Login successful for account {account}")
                    json_data=[]
                    manager = ScheduleManager(f"{account}.json")
                    if 'get_courses_today' in query_params:
                        courses_today = manager.get_courses_on_date(datetime.now().date())
                        for course in courses_today:
                            day_of_week = list(course.weekdays)[0]
                            time_slots = course.periods
                            course_dict = {
                                "name": course.name,
                                "teacher": course.teacher,
                                "location": course.classroom,
                                "day_of_week": day_of_week,
                                "time_slots": time_slots
                            }
                            json_data.append(course_dict)
                    if 'get_courses_tomorrow' in query_params:
                        courses_tomorrow = manager.get_courses_on_date((datetime.now() + timedelta(days=1)).date())
                        for course in courses_tomorrow:
                            day_of_week = list(course.weekdays)[0]
                            time_slots = course.periods
                            course_dict = {
                                "name": course.name,
                                "teacher": course.teacher,
                                "location": course.classroom,
                                "day_of_week": day_of_week,
                                "time_slots": time_slots
                            }
                            json_data.append(course_dict)
                    if 'get_courses_on_date' in query_params:
                        date_list = query_params['get_courses_on_date']
                        if not date_list or not isinstance(date_list, list):
                            return {"error": "Invalid date. Expected a list with one date string."}, 400
                        date_str = date_list[0]
                        if not isinstance(date_str, str):
                            return {"error": "Invalid date format. Expected a string."}, 400
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            return {"error": "Invalid date format. Expected 'YYYY-MM-DD'."}, 400
                    
                        try:
                            courses_on_date = manager.get_courses_on_date(date_obj)
                        except Exception as e:
                            return {"error": f"Error getting courses: {str(e)}"}, 500
                    
                        for course in courses_on_date:
                            day_of_week = list(course.weekdays)[0]
                            time_slots = course.periods
                            course_dict = {
                                "name": course.name,
                                "teacher": course.teacher,
                                "location": course.classroom,
                                "day_of_week": day_of_week,
                                "time_slots": time_slots
                            }
                            json_data.append(course_dict)
                    if 'get_current_course' in query_params:
                        current_course = manager.get_course(datetime.now())
                        if current_course:
                            json_data.append({
                                "current_course": current_course.name
                            })
                    if 'get_next_courses' in query_params:
                        next_courses = manager.get_next_courses(datetime.now())
                        if next_courses:
                            json_data.append({
                                "next_courses": [course.name for course in next_courses]
                            })
                    if json_data:
                        json_result = json.dumps(json_data, ensure_ascii=False, indent=4)
                    else:
                        json_result = "{}"

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json_result.encode('utf-8'))
                else:
                    self.acc_login(query_params)
                    if(logged_in_accounts[account] == True):
                        print(f"Login successful for account {account}")
                    else:
                        print(f"Login failed for account {account}")
                        self.send_response(401)
                        self.end_headers()
                        self.wfile.write(bytes("Login failed.", "utf-8"))
        except ConnectionAbortedError:
            print("Connection was closed by the client.")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=6026):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
