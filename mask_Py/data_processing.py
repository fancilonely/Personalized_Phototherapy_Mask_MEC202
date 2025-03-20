# data_processing.py
from config import PIN_MAPPING, CONFIDENCE_THRESHOLD
import logging

def generate_commands(input_matrix):
    """
    将输入矩阵转换为 Arduino 的控制指令列表。
    每行格式：[区域号, 蓝光, 黄光, 红光]
    如果值为 1，则输出 255（全亮），否则 0（关闭）。
    """
    commands = []
    for row in input_matrix:
        region = row[0]
        blue_val, yellow_val, red_val = row[1], row[2], row[3]

        # 若需要使用置信度，可在此进行逻辑判断
        # 例如 if blue_val >= CONFIDENCE_THRESHOLD: blue_val = 1 else: blue_val = 0
        # 这里示例假设输入矩阵中已是二值化(0或1)

        # 处理蓝光
        if (region, "blue") in PIN_MAPPING:
            pin = PIN_MAPPING[(region, "blue")]
            cmd = f"PIN{pin}:{255 if blue_val == 1 else 0}"
            commands.append(cmd)

        # 处理黄光
        if (region, "yellow") in PIN_MAPPING:
            pin = PIN_MAPPING[(region, "yellow")]
            cmd = f"PIN{pin}:{255 if yellow_val == 1 else 0}"
            commands.append(cmd)

        # 处理红光
        if (region, "red") in PIN_MAPPING:
            pin = PIN_MAPPING[(region, "red")]
            cmd = f"PIN{pin}:{255 if red_val == 1 else 0}"
            commands.append(cmd)

    logging.info("共生成 %d 条指令。", len(commands))
    return commands
