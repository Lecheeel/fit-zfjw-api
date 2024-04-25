from schedule_manager import ScheduleManager
from datetime import datetime, time
# 创建 ScheduleManager 实例
manager = ScheduleManager("2301123104.json",start_date="2024-02-26")

# 获取当前日期的课程
#courses_today = manager.get_courses_on_date(datetime(2024,4,17).date())
courses_today = manager.get_courses_on_date(datetime.now().date())
#manager.get_courses_on_date(datetime(2024,4,10).date())
print("----------今天的课程----------")
for course in courses_today:
    print(course.name)

# 检查当前时间的课程
print('----------当前时间的课程----------')
current_time = datetime.now()
current_course = manager.get_course(current_time)
if current_course:
    print(f"当前课程：{current_course.name}")
else:
    print("当前没有课程。")

print("----------接下来的课程----------")
next_courses = manager.get_next_courses(current_time)
if next_courses:
    for course in next_courses:
        print(course.name)
else:
    print("今天没有更多的课程了。")





# {
    #     "kbList": [
    #         {
    #             "zcd": "1-16周",
    #             "xqj": "1,3,5",
    #             "kcmc": "Mathematics",
    #             "xm": "John Doe",
    #             "cdmc": "Room 101",
    #             "jcs": "1-2节"
    #         },
    #         {
    #             "zcd": "2-8周(双),12-16周(双),17周",
    #             "xqj": "2,4",
    #             "kcmc": "Physics",
    #             "xm": "Jane Doe",
    #             "cdmc": "Room 102",
    #             "jcs": "3-4节"
    #         },
    #         {
    #             "zcd": "1-3周(单),4-5周,7-11周",
    #             "xqj": "1,3,5",
    #             "kcmc": "Chemistry",
    #             "xm": "Alice Smith",
    #             "cdmc": "Room 103",
    #             "jcs": "5-6节"
    #         },
    #         {
    #             "zcd": "1-16周",
    #             "xqj": "2,4",
    #             "kcmc": "Biology",
    #             "xm": "Bob Johnson",
    #             "cdmc": "Room 104",
    #             "jcs": "7-8节"
    #         },
    #         {
    #             "zcd": "1-16周",
    #             "xqj": "1,3,5",
    #             "kcmc": "Computer Science",
    #             "xm": "Charlie Brown",
    #             "cdmc": "Room 105",
    #             "jcs": "9-10节"
    #         }
    #     ]
    # }
