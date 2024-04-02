import unittest
import datetime
from schedule_manager import ScheduleManager, Course

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.manager = ScheduleManager("test_schedule.json")

    def test_load_schedule_from_json(self):
        schedule = self.manager.load_schedule_from_json("test_schedule.json")
        self.assertIsInstance(schedule, list)
        for course in schedule:
            self.assertIsInstance(course, Course)

    def test_get_courses_on_date(self):
        courses = self.manager.get_courses_on_date(datetime.datetime.now().date())
        self.assertIsInstance(courses, list)
        for course in courses:
            self.assertIsInstance(course, Course)

    def test_check_schedule_at_time(self):
        current_course, next_courses = self.manager.check_schedule_at_time(datetime.datetime.now())
        if current_course:
            self.assertIsInstance(current_course, Course)
        if next_courses:
            for course in next_courses:
                self.assertIsInstance(course, Course)

if __name__ == "__main__":
    unittest.main()