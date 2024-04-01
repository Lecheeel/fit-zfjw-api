import unittest
from datetime import datetime, time
from schedule_manager import Course, ScheduleManager

class TestCourse(unittest.TestCase):
    def setUp(self):
        self.course = Course([1, 2, 3], {1, 2, 3}, "Math", "John Doe", "Room 101", [1, 2])

    def test_repr(self):
        self.assertEqual(repr(self.course), "Course(Math, John Doe, Room 101, {1, 2, 3}, [1, 2])")

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.manager = ScheduleManager("schedule.json")

    def test_load_schedule_from_json(self):
        self.assertIsInstance(self.manager.schedule, list)
        self.assertTrue(all(isinstance(course, Course) for course in self.manager.schedule))

    def test_parse_weeks(self):
        self.assertEqual(self.manager.parse_weeks("1-3"), [1, 2, 3])
        self.assertEqual(self.manager.parse_weeks("1-3单"), [1, 3])
        self.assertEqual(self.manager.parse_weeks("1-3双"), [2])
        self.assertEqual(self.manager.parse_weeks("1,3"), [1, 3])

    def test_is_date_in_course_weeks(self):
        course = Course([1, 2, 3], {1, 2, 3}, "Math", "John Doe", "Room 101", [1, 2])
        self.assertTrue(self.manager.is_date_in_course_weeks(datetime.strptime("2024-03-04", '%Y-%m-%d').date(), course))
        self.assertFalse(self.manager.is_date_in_course_weeks(datetime.strptime("2024-03-11", '%Y-%m-%d').date(), course))

    def test_get_courses_on_date(self):
        courses = self.manager.get_courses_on_date(datetime.strptime("2024-03-04", '%Y-%m-%d').date())
        self.assertIsInstance(courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in courses))

    def test_check_schedule_at_time(self):
        current_course, next_courses = self.manager.check_schedule_at_time(datetime.strptime("2024-03-04 09:00", '%Y-%m-%d %H:%M'))
        self.assertIsInstance(current_course, Course)
        self.assertIsInstance(next_courses, list)
        self.assertTrue(all(isinstance(course, Course) for course in next_courses))

    def test_get_current_period(self):
        self.assertEqual(self.manager.get_current_period(datetime.strptime("09:00", '%H:%M')), 1)
        self.assertEqual(self.manager.get_current_period(datetime.strptime("10:00", '%H:%M')), 3)
        self.assertEqual(self.manager.get_current_period(datetime.strptime("12:00", '%H:%M')), None)

if __name__ == "__main__":
    unittest.main()