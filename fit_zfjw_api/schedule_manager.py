import json
import logging
from datetime import datetime, time
from pathlib import Path
import re
from .configs.settings import TIME_PERIODS, START_DATE

class Course:
    def __init__(self, weeks, weekdays, name, teacher, classroom, periods):
        self.weeks = weeks
        self.weekdays = weekdays
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.periods = periods

    def __repr__(self):
        return f"Course({self.name}, {self.teacher}, {self.classroom}, {self.weekdays}, {self.periods})"
    
    def get_start_time(self, schedule_manager):
        start_period = min(self.periods)
        return TIME_PERIODS[start_period][0]


class ScheduleManager:
    def __init__(self, file_path, start_date=START_DATE):
        self.schedule = self.load_json(file_path)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.weeks_diff = (datetime.now().date() - self.start_date).days // 7 + 1

    def load_json(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            logging.error(f"File '{file_path}' not found.")
            return []

        with file_path.open('r', encoding='utf-8') as file:
            schedule_data = json.load(file)

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
        for part in re.split(',|，', week_string):
            if '单' in part:
                start, end = map(int, re.findall(r'\d+', part))
                weeks.extend(range(start, end + 1, 2))
            elif '双' in part:
                start, end = map(int, re.findall(r'\d+', part))
                weeks.extend(range(start, end + 1, 2))
            elif '-' in part:
                start, end = map(int, re.findall(r'\d+', part))
                weeks.extend(range(start, end + 1))
            else:
                weeks.append(int(part))
        return weeks

    def is_date_in_course_weeks(self, target_date, course):
        target_week = (target_date - self.start_date).days // 7 + 1
        return target_week in course.weeks

    def get_courses_on_date(self, target_date):
        target_day_of_week = target_date.isoweekday()
        return [course for course in self.schedule if self.is_date_in_course_weeks(target_date, course) and target_day_of_week in course.weekdays]

    def get_course(self, target_time=None):
        if target_time is None:
            target_time = datetime.now()
        target_date = target_time.date()
        courses = self.get_courses_on_date(target_date)
        current_period = self.get_period(target_time)
        for course in courses:
            if current_period is not None and current_period in course.periods:
                return course
        return None

    def get_next_courses(self, target_time):
        target_date = target_time.date()
        courses = self.get_courses_on_date(target_date)
        return [course for course in courses if course.get_start_time(self) > target_time.time()]

    def get_period(self, target_time):
        current_time = target_time.time()
        for period, (start_time, end_time) in TIME_PERIODS.items():
            if start_time <= current_time <= end_time:
                return period
        return None

    def get_full_semester_schedule(self):
        """
        获取完整学期的课表数据
        返回格式化的课表信息，包含每门课程的详细信息
        """
        full_schedule = []
        
        for course in self.schedule:
            course_info = {
                'name': course.name,
                'teacher': course.teacher,
                'classroom': course.classroom,
                'weeks': course.weeks,
                'weekdays': list(course.weekdays),  # 转换为列表便于JSON序列化
                'periods': course.periods,
                'formatted_info': {
                    'weeks_text': self._format_weeks(course.weeks),
                    'weekdays_text': self._format_weekdays(course.weekdays),
                    'periods_text': self._format_periods(course.periods),
                    'time_text': self._format_time_periods(course.periods)
                }
            }
            full_schedule.append(course_info)
        
        return {
            'semester_info': {
                'start_date': START_DATE,
                'current_week': self.weeks_diff,
                'total_courses': len(full_schedule)
            },
            'courses': full_schedule
        }
    
    def _format_weeks(self, weeks):
        """格式化周次显示"""
        if not weeks:
            return "无"
        
        # 对周次进行排序
        sorted_weeks = sorted(weeks)
        
        # 合并连续的周次
        ranges = []
        start = sorted_weeks[0]
        end = sorted_weeks[0]
        
        for week in sorted_weeks[1:]:
            if week == end + 1:
                end = week
            else:
                if start == end:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{end}")
                start = end = week
        
        # 添加最后一个范围
        if start == end:
            ranges.append(f"{start}")
        else:
            ranges.append(f"{start}-{end}")
        
        return f"{','.join(ranges)}周"
    
    def _format_weekdays(self, weekdays):
        """格式化星期显示"""
        weekday_names = {
            1: "周一", 2: "周二", 3: "周三", 4: "周四", 
            5: "周五", 6: "周六", 7: "周日"
        }
        return ",".join([weekday_names.get(day, f"周{day}") for day in sorted(weekdays)])
    
    def _format_periods(self, periods):
        """格式化节次显示"""
        if not periods:
            return "无"
        return f"{min(periods)}-{max(periods)}节"
    
    def _format_time_periods(self, periods):
        """格式化时间段显示"""
        if not periods:
            return "无"
        
        start_period = min(periods)
        end_period = max(periods)
        
        if start_period in TIME_PERIODS and end_period in TIME_PERIODS:
            start_time = TIME_PERIODS[start_period][0]
            end_time = TIME_PERIODS[end_period][1]
            return f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
        
        return "时间未知"