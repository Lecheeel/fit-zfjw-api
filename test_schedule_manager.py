import unittest
from datetime import datetime
from schedule_manager import ScheduleManager

class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.schedule_manager = ScheduleManager("test_schedule.json")

    def test_loaded_courses(self):
        self.assertEqual(len(self.schedule_manager.schedule), 5)

    def test_get_course(self):
        test_time = datetime.strptime("2024-03-05 09:00", "%Y-%m-%d %H:%M")
        course = self.schedule_manager.get_course(test_time)
        self.assertEqual(course.name, "Mathematics")
        self.assertEqual(course.teacher, "John Doe")
        self.assertEqual(course.classroom, "Room 101")

    def test_get_next_courses(self):
        test_time = datetime.strptime("2024-03-05 09:00", "%Y-%m-%d %H:%M")
        next_courses = self.schedule_manager.get_next_courses(test_time)
        self.assertEqual(len(next_courses), 4)
        self.assertEqual(next_courses[0].name, "Physics")
        self.assertEqual(next_courses[1].name, "Chemistry")
        self.assertEqual(next_courses[2].name, "Biology")
        self.assertEqual(next_courses[3].name, "Computer Science")

if __name__ == '__main__':
    unittest.main()
