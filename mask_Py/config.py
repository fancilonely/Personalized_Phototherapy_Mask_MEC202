# config.py

# 串口配置
SERIAL_PORT = "COM3"   # 根据实际情况修改，如在 Linux 上可能是 /dev/ttyUSB0
BAUDRATE = 9600

# 9 个区域 × 3 种颜色的引脚映射（手动定义）
PIN_MAPPING = {
    (1, "blue"): 2,
    (1, "yellow"): 3,
    (1, "red"): 4,
    (2, "blue"): 5,
    (2, "yellow"): 6,
    (2, "red"): 7,
    (3, "blue"): 8,
    (3, "yellow"): 9,
    (3, "red"): 10,
    (4, "blue"): 11,
    (4, "yellow"): 12,
    (4, "red"): 13,
    (5, "blue"): 14,
    (5, "yellow"): 15,
    (5, "red"): 16,
    (6, "blue"): 17,
    (6, "yellow"): 18,
    (6, "red"): 19,
    (7, "blue"): 20,
    (7, "yellow"): 21,
    (7, "red"): 22,
    (8, "blue"): 23,
    (8, "yellow"): 24,
    (8, "red"): 25,
    (9, "blue"): 26,
    (9, "yellow"): 27,
    (9, "red"): 28
}

# 如果需要在数据处理时用到置信度判断，可在此定义
CONFIDENCE_THRESHOLD = 0.9
