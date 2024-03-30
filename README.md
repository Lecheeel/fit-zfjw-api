## FIT ZFJW API

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
为避免对教务系统造成不必要的负担，您不应频繁爬取获取数据，以免影响系统正常运行。应合理设置爬取频率，避免对服务器造成过大负载。

## 捐赠

想要支持项目作者吗？给我送瓶可乐到A1-312吧 🥤😊

## 免责声明

本项目仅供学习和研究使用，不得用于任何商业用途。使用本项目造成的任何损失或法律责任，均与项目作者无关。用户应自行承担使用本项目的风险，并按照所在地的法律法规合法使用。

本项目涉及到教务系统，用户在使用时应遵守所在学校的规定和相关法律法规。未经授权，用户不得进行任何未经授权的操作，包括但不限于未经许可的登录、获取个人信息等行为。

作者不对使用本项目造成的任何直接或间接损失负责，包括但不限于因使用本项目导致的个人信息泄露、账号被封禁等情况。用户应自行承担风险，并注意保护个人信息安全。

如果您使用本项目，则视为您已接受本免责声明的所有条款和条件。