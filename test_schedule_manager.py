import unittest
import datetime
from schedule_manager import ScheduleManager, Course

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.manager = ScheduleManager("test_schedule.json")

    def test_load_json(self):
        schedule = self.manager.load_json("test_schedule.json")
        self.assertIsInstance(schedule, list)
        for course in schedule:
            self.assertIsInstance(course, Course)

    def test_get_courses_on_date(self):
        courses = self.manager.get_courses_on_date(datetime.datetime.now().date())
        self.assertIsInstance(courses, list)
        for course in courses:
            self.assertIsInstance(course, Course)

if __name__ == "__main__":
    unittest.main()