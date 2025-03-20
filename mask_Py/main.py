# main.py
import logging
from data_processing import generate_commands
from usb_communication import send_commands_via_usb
from config import SERIAL_PORT, BAUDRATE

def main():
    logging.info("开始执行 main 函数...")

    # 示例输入矩阵（9×4），每行 [区域号, 蓝光, 黄光, 红光]
    input_matrix = [
        [1, 0, 0, 0],
        [2, 0, 0, 0],
        [3, 0, 0, 0],
        [4, 1, 0, 0],
        [5, 0, 1, 0],
        [6, 0, 0, 1],
        [7, 0, 0, 0],
        [8, 0, 0, 0],
        [9, 0, 0, 0]
    ]

    # 生成控制指令
    commands = generate_commands(input_matrix)
    logging.info("生成的指令列表：%s", commands)

    # 发送指令
    send_commands_via_usb(commands, SERIAL_PORT, BAUDRATE)

if __name__ == "__main__":
    # 如果需要自定义日志，可在此处调用 utils.setup_logging()
    main()
