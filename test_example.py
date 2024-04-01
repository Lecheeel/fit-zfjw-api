import unittest
from datetime import datetime, time
from schedule_manager import Course, ScheduleManager
import json

class TestScheduleManagerWithJSON(unittest.TestCase):
    def setUp(self):
        self.json_data = """
        {
            "kbList": [
                {
                    "zcd": "1-16周",
                    "xqj": "1,3,5",
                    "kcmc": "Mathematics",
                    "xm": "John Doe",
                    "cdmc": "Room 101",
                    "jcs": "1-2节"
                },
                {
                    "zcd": "1-16双周",
                    "xqj": "2,4",
                    "kcmc": "Physics",
                    "xm": "Jane Doe",
                    "cdmc": "Room 102",
                    "jcs": "3-4节"
                },
                {
                    "zcd": "1-16单周",
                    "xqj": "1,3,5",
                    "kcmc": "Chemistry",
                    "xm": "Alice Smith",
                    "cdmc": "Room 103",
                    "jcs": "5-6节"
                },
                {
                    "zcd": "1-16周",
                    "xqj": "2,4",
                    "kcmc": "Biology",
                    "xm": "Bob Johnson",
                    "cdmc": "Room 104",
                    "jcs": "7-8节"
                },
                {
                    "zcd": "1-16周",
                    "xqj": "1,3,5",
                    "kcmc": "Computer Science",
                    "xm": "Charlie Brown",
                    "cdmc": "Room 105",
                    "jcs": "9-10节"
                }
            ]
        }
        """
        self.schedule_data = json.loads(self.json_data)
        self.manager = ScheduleManager(self.schedule_data)

    def test_load_schedule_from_json(self):
        self.assertIsInstance(self.manager.schedule, list)
        self.assertTrue(all(isinstance(course, Course) for course in self.manager.schedule))

    # Add more tests here...

if __name__ == "__main__":
    unittest.main()