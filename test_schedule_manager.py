import unittest
import json
import os
from datetime import datetime
from functions.schedule_manager import ScheduleManager

# Define a sample schedule JSON for testing
SCHEDULE_JSON = '''
{
    "kbList": [
        {
            "zcd": "1-16 weeks",
            "xqj": "1,3,5",
            "kcmc": "Mathematics",
            "xm": "John Doe",
            "cdmc": "Room 101",
            "jcs": "1-2 periods"
        },
        {
            "zcd": "2-8 weeks (even), 12-16 weeks (even), 17th week",
            "xqj": "2,4",
            "kcmc": "Physics",
            "xm": "Jane Doe",
            "cdmc": "Room 102",
            "jcs": "3-4 periods"
        },
        {
            "zcd": "1-3 weeks (odd), 4-5 weeks, 7-11 weeks",
            "xqj": "1,3,5",
            "kcmc": "Chemistry",
            "xm": "Alice Smith",
            "cdmc": "Room 103",
            "jcs": "5-6 periods"
        },
        {
            "zcd": "1-16 weeks",
            "xqj": "2,4",
            "kcmc": "Biology",
            "xm": "Bob Johnson",
            "cdmc": "Room 104",
            "jcs": "7-8 periods"
        },
        {
            "zcd": "1-16 weeks",
            "xqj": "1,3,5",
            "kcmc": "Computer Science",
            "xm": "Charlie Brown",
            "cdmc": "Room 105",
            "jcs": "9-10 periods"
        }
    ]
}
'''

class TestScheduleManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a sample schedule JSON file before running tests."""
        with open('data/schedule.json', 'w') as file:
            file.write(SCHEDULE_JSON)
        cls.manager = ScheduleManager("data/schedule.json", start_date="2024-08-26")

    @classmethod
    def tearDownClass(cls):
        """Remove the sample schedule JSON file after tests."""
        os.remove('data/schedule.json')

    def test_get_courses_on_date(self):
        """Test fetching courses on a specific date."""
        today = datetime.now().date()
        courses = self.manager.get_courses_on_date(today)
        self.assertIsInstance(courses, list, "Expected a list of courses.")
        for course in courses:
            self.assertTrue(hasattr(course, 'name'), "Each course should have a 'name' attribute.")
    
    def test_get_course(self):
        """Test fetching the course at the current time."""
        current_time = datetime.now()
        course = self.manager.get_course(current_time)
        if course:
            self.assertTrue(hasattr(course, 'name'), "The current course should have a 'name' attribute.")
        self.assertTrue(course is None or hasattr(course, 'name'), "The returned course should be a Course object or None.")

    def test_get_next_courses(self):
        """Test fetching the next courses."""
        current_time = datetime.now()
        next_courses = self.manager.get_next_courses(current_time)
        self.assertIsInstance(next_courses, list, "Expected a list of next courses.")
        for course in next_courses:
            self.assertTrue(hasattr(course, 'name'), "Each next course should have a 'name' attribute.")
    
if __name__ == '__main__':
    unittest.main()
