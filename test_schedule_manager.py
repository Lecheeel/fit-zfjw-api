import unittest
from datetime import datetime, date, time
from schedule_manager import ScheduleManager, Course

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.schedule_manager = ScheduleManager('path/to/schedule.json', start_date='2024-02-26')

    def test_load_json(self):
        # Test loading JSON file
        self.assertEqual(len(self.schedule_manager.schedule), 3)
        self.assertIsInstance(self.schedule_manager.schedule[0], Course)
        self.assertEqual(self.schedule_manager.schedule[0].name, 'Math')
        self.assertEqual(self.schedule_manager.schedule[0].teacher, 'John Doe')
        self.assertEqual(self.schedule_manager.schedule[0].classroom, 'Room 101')
        self.assertEqual(self.schedule_manager.schedule[0].periods, [1, 3, 5])

    def test_parse_weeks(self):
        # Test parsing week string
        self.assertEqual(self.schedule_manager.parse_weeks('1-3,5'), [1, 2, 3, 5])
        self.assertEqual(self.schedule_manager.parse_weeks('1,3,5,7'), [1, 3, 5, 7])
        self.assertEqual(self.schedule_manager.parse_weeks('1,3,5-7'), [1, 3, 5, 6, 7])

    def test_is_date_in_course_weeks(self):
        # Test checking if date is in course weeks
        target_date = date(2024, 3, 10)
        course = Course([1, 2, 3, 5], {1, 3, 5}, 'Math', 'John Doe', 'Room 101', [1, 3, 5])
        self.assertTrue(self.schedule_manager.is_date_in_course_weeks(target_date, course))

    def test_get_courses_on_date(self):
        # Test getting courses on a specific date
        target_date = date(2024, 3, 10)
        courses = self.schedule_manager.get_courses_on_date(target_date)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, 'Math')
        self.assertEqual(courses[0].teacher, 'John Doe')
        self.assertEqual(courses[0].classroom, 'Room 101')
        self.assertEqual(courses[0].periods, [1, 3, 5])

    def test_get_course(self):
        # Test getting course at a specific time
        target_time = datetime(2024, 3, 10, 9, 0)
        course = self.schedule_manager.get_course(target_time)
        self.assertEqual(course.name, 'Math')
        self.assertEqual(course.teacher, 'John Doe')
        self.assertEqual(course.classroom, 'Room 101')
        self.assertEqual(course.periods, [1, 3, 5])

    def test_get_next_courses(self):
        # Test getting next courses after a specific time
        target_time = datetime(2024, 3, 10, 9, 0)
        next_courses = self.schedule_manager.get_next_courses(target_time)
        self.assertEqual(len(next_courses), 1)
        self.assertEqual(next_courses[0].name, 'Math')
        self.assertEqual(next_courses[0].teacher, 'John Doe')
        self.assertEqual(next_courses[0].classroom, 'Room 101')
        self.assertEqual(next_courses[0].periods, [1, 3, 5])

    def test_get_period(self):
        # Test getting period for a specific time
        target_time = time(9, 0)
        period = self.schedule_manager.get_period(target_time)
        self.assertEqual(period, 1)

if __name__ == '__main__':
    unittest.main()