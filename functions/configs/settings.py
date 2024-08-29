from datetime import time

# 配置文件: configs/settings.py

TIME_PERIODS = {
    1: (time(8, 30), time(9, 15)),
    2: (time(9, 15), time(10, 5)),
    3: (time(10, 5), time(11, 5)),
    4: (time(11, 5), time(11, 55)),
    5: (time(14, 0), time(14, 45)),
    6: (time(14, 45), time(15, 35)),
    7: (time(15, 35), time(16, 30)),
    8: (time(16, 30), time(17, 20)),
    9: (time(17, 20), time(19, 15)),
    10: (time(19, 15), time(20, 10)),
    11: (time(20, 10), time(21, 5))
}

START_DATE = "2024-02-26"

BASE_URL = 'http://oaa.fitedu.net/jwglxt'
