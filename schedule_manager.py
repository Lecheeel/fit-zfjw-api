import json
from datetime import datetime, time

class Course:
    def __init__(self, weeks, weekdays, name, teacher, classroom, periods):
        self.weeks = weeks
        self.weekdays = weekdays
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.periods = periods

class ScheduleManager:
    TIME_PERIODS = {
        1: (time(8, 30), time(9, 15)),
        2: (time(9, 20), time(10, 5)),
        3: (time(10, 20), time(11, 5)),
        4: (time(11, 10), time(11, 55)),
        5: (time(14, 0), time(14, 45)),
        6: (time(14, 50), time(15, 35)),
        7: (time(15, 45), time(16, 30)),
        8: (time(16, 35), time(17, 20)),
        9: (time(18, 30), time(19, 15)),
        10: (time(19, 25), time(20, 10)),
        11: (time(20, 20), time(21, 5))
    }
    START_DATE = "2024-02-26"

    def __init__(self, file_path, start_date=START_DATE):
        self.schedule = self.load_schedule_from_json(file_path)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.weeks_diff = (datetime.now().date() - self.start_date).days // 7 + 1

    def load_schedule_from_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                schedule_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []

        schedule = schedule_data.get('kbList', [])
        parsed_schedule = []
        for course in schedule:
            weeks = self.parse_weeks(course.get('zcd', '').replace('周', ''))
            weekdays = {int(day) for day in course.get('xqj', '').split(',') if day}
            name = course.get('kcmc', '无')
            teacher = course.get('xm', '无')
            classroom = course.get('cdmc', '无')
            periods = self.parse_weeks(course.get('jcs', '无').replace('节', ''))
            parsed_schedule.append(Course(weeks, weekdays, name, teacher, classroom, periods))
        return parsed_schedule

    def parse_weeks(self, week_string):
        weeks = []
        for part in week_string.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                weeks.extend(range(start, end + 1))
            else:
                weeks.append(int(part))
        return weeks

    def get_courses_on_date(self, target_date):
        target_week = (target_date - self.start_date).days // 7 + 1
        target_day_of_week = target_date.isoweekday()
        return [course for course in self.schedule if target_week in course.weeks and target_day_of_week in course.weekdays]

    def check_schedule_at_time(self, target_time):
        current_period = self.get_current_period(target_time)
        target_date = target_time.date()
        courses = self.get_courses_on_date(target_date)
        current_course = None
        next_courses = []

        if current_period is None:
            return None, courses

        for course in courses:
            if current_period in course.periods:
                current_course = course
            elif max(course.periods) >= current_period:
                next_courses.append(course)

        return current_course, next_courses

    def get_current_period(self, target_time):
        current_time = target_time.time()
        for period, (start_time, end_time) in self.TIME_PERIODS.items():
            if start_time <= current_time <= end_time:
                return period
        return None


def main():
    schedule_manager = ScheduleManager('schedule.json')
    target_date = datetime.now().date()
    print(target_date   )
    target_time_str = "2024-03-21 09:00"
    target_time = datetime.strptime(target_time_str, '%Y-%m-%d %H:%M')

    #target_time = datetime.now().replace(second=0, microsecond=0)

    # 获取指定日期的课程
    courses = schedule_manager.get_courses_on_date(target_date)
    print(f"指定日期 {target_date} 要上的课程有：")
    for course in courses:
        print(f"课程名称: {course.name}, 老师姓名: {course.teacher}, 教室名称: {course.classroom},  课程节数: {course.periods}")

    # 获取当前时间段
    current_period = schedule_manager.get_current_period(target_time)
    if current_period is not None:
        print(f"当前是第{current_period}节课")
    else:
        print("当前时间不在任何时间段内")

    # 检查目标时间是否有课程
    current_course, next_courses = schedule_manager.check_schedule_at_time(target_time)
    if current_course:
        print(f"目标时间有课：{current_course.name}, {current_course.teacher}, {current_course.classroom},  {current_course.weekdays}, {current_course.periods}")
    else:
        print("目标时间无课")

    if next_courses:
        print("接下来的课程有：")
        for course in next_courses:
            print(f"课程名称: {course.name}, 老师姓名: {course.teacher}, 教室名称: {course.classroom},  课程节数: {course.periods}, {course.weekdays}")
    else:
        print("全部课程已上完")

if __name__ == "__main__":
    main()