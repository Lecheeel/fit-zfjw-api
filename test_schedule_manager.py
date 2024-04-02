import unittest
import datetime
from schedule_manager import ScheduleManager, Course

class TestScheduleManagerMethods(unittest.TestCase):
    def setUp(self):
        self.manager = ScheduleManager("test_schedule.json")

    def test_load_json(self):
        schedule = self.manager.load_json("test_schedule.json")
        self.assertIsInstance(schedule, list)
        for course in schedule:
            self.assertIsInstance(course, Course)

    def test_parse_weeks(self):
        weeks = self.manager.parse_weeks("1-16周")
        self.assertEqual(weeks, list(range(1, 17)))

        weeks = self.manager.parse_weeks("2-8周(双),12-16周(双),17周")
        self.assertEqual(weeks, [2, 4, 6, 8, 12, 14, 16, 17])

    def test_is_date_in_course_weeks(self):
        course = Course([1, 2, 3], [1, 2, 3], "Mathematics", "John Doe", "Room 101", [1, 2])
        target_date = datetime.strptime("2024-03-05", '%Y-%m-%d').date()
        self.assertTrue(self.manager.is_date_in_course_weeks(target_date, course))

    def test_get_courses_on_date(self):
        target_date = datetime.strptime("2024-03-05", '%Y-%m-%d').date()
        courses = self.manager.get_courses_on_date(target_date)
        self.assertIsInstance(courses, list)
        for course in courses:
            self.assertIsInstance(course, Course)

    def test_get_course(self):
        target_time = datetime.strptime("2024-03-05 09:00:00", '%Y-%m-%d %H:%M:%S')
        course = self.manager.get_course(target_time)
        self.assertIsInstance(course, Course)

    def test_get_next_courses(self):
        target_time = datetime.strptime("2024-03-05 09:00:00", '%Y-%m-%d %H:%M:%S')
        courses = self.manager.get_next_courses(target_time)
        self.assertIsInstance(courses, list)
        for course in courses:
            self.assertIsInstance(course, Course)

    def test_get_period(self):
        target_time = datetime.strptime("09:00:00", '%H:%M:%S').time()
        period = self.manager.get_period(target_time)
        self.assertEqual(period, 1)