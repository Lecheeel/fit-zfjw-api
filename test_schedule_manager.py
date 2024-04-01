import os
import unittest
from datetime import datetime, time
from schedule_manager import Course, ScheduleManager
import tempfile
import json
from unittest.mock import mock_open, patch

class TestScheduleManagerWithJSON(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.json_data = {
            "kbList": [
                {"zcd": "1-16周", "xqj": "1,3,5", "kcmc": "Mathematics", "xm": "John Doe", "cdmc": "Room 101", "jcs": "1-2节"},
                {"zcd": "1-16双周", "xqj": "2,4", "kcmc": "Physics", "xm": "Jane Doe", "cdmc": "Room 102", "jcs": "3-4节"},
                {"zcd": "1-16单周", "xqj": "1,3,5", "kcmc": "Chemistry", "xm": "Alice Smith", "cdmc": "Room 103", "jcs": "5-6节"},
                {"zcd": "1-16周", "xqj": "2,4", "kcmc": "Biology", "xm": "Bob Johnson", "cdmc": "Room 104", "jcs": "7-8节"},
                {"zcd": "1-16周", "xqj": "1,3,5", "kcmc": "Computer Science", "xm": "Charlie Brown", "cdmc": "Room 105", "jcs": "9-10节"}
            ]
        }
        cls.json_str = json.dumps(cls.json_data)

    def setUp(self):
        self.mock_file = mock_open(read_data=self.json_str)
        self.open_name = 'builtins.open'
        with patch(self.open_name, self.mock_file):
            self.manager = ScheduleManager('dummy_path')

    def test_load_schedule_from_json(self):
        with patch(self.open_name, self.mock_file):
            self.manager = ScheduleManager('dummy_path')
            self.assertIsInstance(self.manager.schedule, list)
            self.assertTrue(all(isinstance(course, Course) for course in self.manager.schedule))

    def test_schedule_length(self):
        self.assertEqual(len(self.manager.schedule), 5)

    def test_course_attributes(self):
        course = self.manager.schedule[0]
        self.assertEqual(course.kcmc, "Mathematics")
        self.assertEqual(course.xm, "John Doe")
        self.assertEqual(course.cdmc, "Room 101")
        self.assertEqual(course.jcs, "1-2节")

    def test_get_courses_on_date(self):
        courses = self.manager.get_courses_on_date(datetime.now().date())
        self.assertIsInstance(courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in courses))

    def test_check_schedule_at_time(self):
        current_course, upcoming_courses = self.manager.check_schedule_at_time(datetime.now())
        if current_course is not None:
            self.assertIsInstance(current_course, Course)
        self.assertIsInstance(upcoming_courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in upcoming_courses))

    def test_get_current_period(self):
        period = self.manager.get_current_period(time(10, 30))
        self.assertIsInstance(period, int)
if __name__ == "__main__":
    unittest.main()