import asyncio
from data_processing import generate_commands, generate_shutdown_commands
from bluetooth_communication import send_commands_via_bluetooth

async def control_with_timer(input_matrix, duration):
    # 生成启动命令
    commands = generate_commands(input_matrix)
    await send_commands_via_bluetooth(commands)

    print(f"[INFO] 光疗开始，预计 {duration} 秒后关闭。")
    await asyncio.sleep(duration)  # ⏱️ 定时器：控制光疗时间

    # 生成关闭命令
    shutdown_commands = generate_shutdown_commands(input_matrix)
    print("[INFO] 时间到，正在关闭光疗...")
    await send_commands_via_bluetooth(shutdown_commands)
    print("[INFO] 光疗已关闭。")

def main():
    # 示例输入矩阵：每行 [区域号, 红光, 绿光, 蓝光]
    input_matrix = [
        [1, 0, 0, 0],
        [2, 0, 1, 0],
        [3, 0, 0, 0],
        [4, 0, 0, 0],
        [5, 0, 0, 0],
    ]

    duration = 5  # ⏳ 预留时间函数的位置（秒）
    asyncio.run(control_with_timer(input_matrix, duration))

if __name__ == "__main__":
    main()
