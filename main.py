# main.py

import asyncio
from data_processing import generate_commands
from bluetooth_communication import send_commands_via_bluetooth

def main():
    # 示例输入矩阵：每行 [区域号, 蓝光, 黄光, 红光]
    input_matrix = [
        [1, 0, 0, 1],
        [2, 0, 1, 0],
        [3, 1, 0, 0],
        [4, 0, 1, 1],
        [5, 1, 1, 0],
    ]

    commands = generate_commands(input_matrix)

    # 执行异步蓝牙发送逻辑
    asyncio.run(send_commands_via_bluetooth(commands))

if __name__ == "__main__":
    main()