## Fit ZFJW API

### 项目简介
FIT ZFJW API 是一个用于FIT教务的Python API

### 环境要求
- Python 3.6 或更高版本
- Requests 库 (`pip install requests`)
- RSA 库 (`pip install rsa`)
- PyQuery 库 (`pip install pyquery`)

### 使用方法
1. 克隆仓库：
   ```bash
   git clone https://github.com/Lecheeel/fit_zfjw_api.git
   ```

2. 导入所需模块：
   ```python
   from fit_zfjw_api import JWGLClient, ScheduleManager
   ```

3. 使用基本 URL、账号和密码初始化 JWGLClient：
   ```python
   client = JWGLClient(base_url, account, password)
   ```

4. 登录系统：
   ```python
   login_result = client.login()
   ```

5. 获取课表信息：
   ```python
   schedule = client.get_schedule()
   ```

6. 获取个人信息：
   ```python
   info = client.get_info()
   ```

7. 或者，使用 ScheduleManager 来管理与课表相关的任务：
   ```python
   schedule_manager = ScheduleManager('schedule.json')
   ```

   - 获取特定日期的课程：
     ```python
     courses = schedule_manager.get_courses_on_date(target_date)
     ```

   - 检查特定时间的课程安排：
     ```python
     current_course, next_courses = schedule_manager.check_schedule_at_time(target_time)
     ```

### 示例
```python
from fit_zfjw_api import JWGLClient, ScheduleManager

# 初始化 JWGLClient
client = JWGLClient(base_url, account, password)

# 登录
login_result = client.login()

# 获取课表
schedule = client.get_schedule()

# 获取个人信息
info = client.get_info()

# 初始化 ScheduleManager
schedule_manager = ScheduleManager('schedule.json')

# 获取特定日期的课程
courses = schedule_manager.get_courses_on_date(target_date)

# 检查特定时间的课程安排
current_course, next_courses = schedule_manager.check_schedule_at_time(target_time)
```

### 注意
低调使用