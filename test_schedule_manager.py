import unittest
from datetime import datetime
from schedule_manager import ScheduleManager, Course

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.manager = ScheduleManager("test_schedule.json")

    def test_get_courses_on_date(self):
        # Test for a date in the first week
        courses = self.manager.get_courses_on_date(datetime(2024, 2, 26).date())
        self.assertEqual(len(courses), 1)
        self.assertIsInstance(courses[0], Course)
        self.assertEqual(courses[0].name, "Mathematics")

        # Test for a date in the second week
        courses = self.manager.get_courses_on_date(datetime(2024, 3, 5).date())
        self.assertEqual(len(courses), 2)
        self.assertIsInstance(courses[0], Course)
        self.assertEqual(courses[0].name, "Mathematics")
        self.assertEqual(courses[1].name, "Chemistry")

        # Test for a date in the third week
        courses = self.manager.get_courses_on_date(datetime(2024, 3, 12).date())
        self.assertEqual(len(courses), 1)
        self.assertIsInstance(courses[0], Course)
        self.assertEqual(courses[0].name, "Mathematics")

    def test_get_course(self):
        # Test for a time in the first period
        current_time = datetime(2024, 2, 26, 8, 30)
        current_course = self.manager.get_course(current_time)
        self.assertIsInstance(current_course, Course)
        self.assertEqual(current_course.name, "Mathematics")

        # Test for a time in the fifth period
        current_time = datetime(2024, 2, 26, 14, 0)
        current_course = self.manager.get_course(current_time)
        self.assertIsNone(current_course)

    def test_get_next_courses(self):
        # Test for a time before the first period
        current_time = datetime(2024, 2, 26, 8, 0)
        next_courses = self.manager.get_next_courses(current_time)
        self.assertEqual(len(next_courses), 1)
        self.assertIsInstance(next_courses[0], Course)
        self.assertEqual(next_courses[0].name, "Mathematics")

        # Test for a time after the last period
        current_time = datetime(2024, 2, 26, 21, 30)
        next_courses = self.manager.get_next_courses(current_time)
        self.assertEqual(len(next_courses), 0)

if __name__ == "__main__":
    unittest.main()