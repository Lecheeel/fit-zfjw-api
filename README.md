## FIT ZFJW API

### 项目简介
FIT ZFJW API 是一个用于FIT教务系统的Python API包，提供了方便的接口来获取教务信息和管理课表。

### 安装

#### 从源码安装
```bash
git clone https://github.com/Lecheeel/fit-zfjw-api.git
cd fit-zfjw-api
pip install -e .
```

### 环境要求
- Python 3.6 或更高版本
- 依赖包将自动安装：
  - requests>=2.25.1
  - rsa>=4.7
  - pyquery>=1.4.3

### 使用说明

#### 基本用法

```python
from fit_zfjw_api import JWGLClient, ScheduleManager

# 初始化教务客户端
client = JWGLClient(base_url, account, password)

# 登录系统
login_result = client.login()

# 获取课表信息
schedule = client.get_schedule()

# 获取个人信息
info = client.get_info()

# 初始化课表管理器
schedule_manager = ScheduleManager('schedule.json')

# 获取特定日期的课程
from datetime import date
courses = schedule_manager.get_courses_on_date(date.today())

# 获取当前时间的课程
current_course = schedule_manager.get_course()

# 获取接下来的课程
from datetime import datetime
next_courses = schedule_manager.get_next_courses(datetime.now())
```

#### 高级用法

```python
from fit_zfjw_api import JWGLClient, ScheduleManager, Course
from datetime import datetime, date

# 自定义基础URL
base_url = "https://your-jwgl-system.edu.cn"
client = JWGLClient(base_url, "your_username", "your_password")

try:
    # 登录
    login_result = client.login()
    print("登录成功")
    
    # 获取并保存课表
    schedule_response = client.get_schedule()
    schedule_data = schedule_response.json()
    
    # 保存到文件
    import json
    with open('my_schedule.json', 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, ensure_ascii=False, indent=4)
    
    # 使用课表管理器
    manager = ScheduleManager('my_schedule.json', start_date="2024-09-01")
    
    # 获取今天的课程
    today_courses = manager.get_courses_on_date(date.today())
    for course in today_courses:
        print(f"课程: {course.name}, 教师: {course.teacher}, 教室: {course.classroom}")
    
    # 检查当前是否有课
    current_course = manager.get_course(datetime.now())
    if current_course:
        print(f"当前课程: {current_course.name}")
    else:
        print("当前没有课程")
    
except Exception as e:
    print(f"操作失败: {e}")
```

### API参考

#### JWGLClient

主要用于与教务系统交互的客户端类。

**方法：**
- `login()`: 登录教务系统
- `get_schedule()`: 获取课表数据
- `get_info()`: 获取个人信息

#### ScheduleManager

用于管理和查询课表信息的类。

**方法：**
- `get_courses_on_date(target_date)`: 获取指定日期的课程
- `get_course(target_time=None)`: 获取指定时间的当前课程
- `get_next_courses(target_time)`: 获取指定时间之后的课程

#### Course

课程信息类，包含课程的基本信息。

**属性：**
- `name`: 课程名称
- `teacher`: 教师姓名
- `classroom`: 教室位置
- `weeks`: 上课周次
- `weekdays`: 上课星期
- `periods`: 上课节次

### 示例程序

查看 `examples/` 目录获取更多使用示例：
- `JWGL_Client_Usage.py`: 教务客户端使用示例
- `schedule_manager_usage.py`: 课表管理器使用示例
- `course_server_usage.py`: 课程服务器使用示例

### 开发

#### 开发环境设置
```bash
git clone https://github.com/Lecheeel/fit-zfjw-api.git
cd fit-zfjw-api
pip install -e ".[dev]"
```

#### 运行测试
```bash
python -m pytest test/
```

### 注意事项

为避免对教务系统造成不必要的负担，您不应频繁爬取获取数据，以免影响系统正常运行。应合理设置爬取频率，避免对服务器造成过大负载。

### 许可证

本项目使用 GPL 许可证。详见 [LICENSE](LICENSE) 文件。

### 捐赠

想要支持项目作者吗？给我送瓶可乐到A1-312吧 🥤😊

### 免责声明

本项目仅供学习和研究使用，不得用于任何商业用途。使用本项目造成的任何损失或法律责任，均与项目作者无关。用户应自行承担使用本项目的风险，并按照所在地的法律法规合法使用。

本项目涉及到教务系统，用户在使用时应遵守所在学校的规定和相关法律法规。未经授权，用户不得进行任何未经授权的操作，包括但不限于未经许可的登录、获取个人信息等行为。

作者不对使用本项目造成的任何直接或间接损失负责，包括但不限于因使用本项目导致的个人信息泄露、账号被封禁等情况。用户应自行承担风险，并注意保护个人信息安全。

如果您使用本项目，则视为您已接受本免责声明的所有条款和条件。