"""
FIT ZFJW API - 一个用于FIT教务系统的Python API包

该包提供了以下主要功能：
- JWGLClient: 教务系统登录和数据获取客户端
- ScheduleManager: 课表管理器
- Course: 课程信息类
"""

from .JWGL_Client import JWGLClient
from .schedule_manager import ScheduleManager, Course
from .configs.settings import BASE_URL, START_DATE
__version__ = "1.0.0"
__author__ = "Lecheeel"
__email__ = ""

__all__ = [
    "JWGLClient",
    "ScheduleManager", 
    "Course",
    "BASE_URL",
    "START_DATE"
]
