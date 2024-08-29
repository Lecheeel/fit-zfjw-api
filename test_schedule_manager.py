import unittest
import json
import os
from datetime import datetime
from functions.schedule_manager import ScheduleManager
from functions.configs.settings import START_DATE

class TestScheduleManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = ScheduleManager("data/test_schedule.json", start_date=START_DATE)

    @classmethod
    def tearDownClass(cls):
        """Remove the sample schedule JSON file after tests."""
        # os.remove('data/schedule.json')

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
