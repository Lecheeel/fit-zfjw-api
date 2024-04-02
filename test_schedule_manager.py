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

    def test_is_date_in_course_weeks(self):
        target_date = datetime.date(2024, 2, 28)
        course = Course([1, 3, 5], [1, 3, 5], "Math", "John Doe", "Room 101", [1, 2, 3])
        result = self.manager.is_date_in_course_weeks(target_date, course)
        self.assertTrue(result)

    def test_get_courses_on_date(self):
        target_date = datetime.date(2024, 2, 28)
        courses = self.manager.get_courses_on_date(target_date)
        self.assertIsInstance(courses, list)
        for course in courses:
            self.assertIsInstance(course, Course)

    def test_get_course(self):
        target_time = datetime.datetime(2024, 2, 28, 9, 0)
        course = self.manager.get_course(target_time)
        self.assertIsInstance(course, Course)

    def test_get_next_courses(self):
        target_time = datetime.datetime(2024, 2, 28, 9, 0)
        next_courses = self.manager.get_next_courses(target_time)
        self.assertIsInstance(next_courses, list)
        for course in next_courses:
            self.assertIsInstance(course, Course)

    def test_get_period(self):
        target_time = datetime.datetime(2024, 2, 28, 9, 0)
        period = self.manager.get_period(target_time)
        self.assertIsInstance(period, int)

if __name__ == "__main__":
    unittest.main()