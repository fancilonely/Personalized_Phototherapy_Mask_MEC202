#main.py
import asyncio
import time
from data_processing import (
    generate_commands,
    generate_shutdown_commands,
    split_matrix_dynamically
)
from bluetooth_communication import send_commands_via_bluetooth
from data_processing import split_matrix_dynamically, read_matrix_from_csv #csv导入
# 其他导入不变

async def control_dynamically(input_matrix, duration_per_round=5):
    """
    根据输入矩阵执行动态光疗轮次，每轮执行唯一颜色控制区域
    """
    all_rounds = split_matrix_dynamically(input_matrix)
    print(f"[INFO] 本次共需执行 {len(all_rounds)} 轮光疗")

    for idx, round_matrix in enumerate(all_rounds):
        print("=" * 50)
        print(f"[INFO] ➤ 第 {idx + 1} 轮光疗开始，共 {len(round_matrix)} 个区域")
        print(f"[INFO] ⏱️ 每轮持续时间：{duration_per_round} 秒")

        # 生成命令并发送
        commands = generate_commands(round_matrix)
        await send_commands_via_bluetooth(commands)

        # 开始计时
        start_time = time.time()
        await asyncio.sleep(duration_per_round)
        elapsed = time.time() - start_time

        # 关闭LED
        shutdown_commands = generate_shutdown_commands(round_matrix)
        await send_commands_via_bluetooth(shutdown_commands)

        print(f"[INFO] 第 {idx + 1} 轮光疗结束，用时 {elapsed:.1f} 秒")
        print("=" * 50)

    print("[INFO] ✅ 所有光疗轮次执行完成！")

def main():
    # 示例输入矩阵：每行 [区域号, 红光, 绿光, 蓝光]

#    input_matrix = [
#        [1, 1, 1, 0],  # R+G
#        [2, 0, 1, 0],  # G
#        [3, 0, 0, 1],  # B
#        [4, 1, 0, 0],  # R
#        [5, 1, 1, 1],  # R+G+B
#    ]
    file_path = "input_matrix.csv"  # 👈 放你自己的文件路径
    input_matrix = read_matrix_from_csv(file_path)

    if not input_matrix:
        print("[ERROR] 输入矩阵为空或CSV文件格式错误")
        return

    duration_per_round = 5
    asyncio.run(control_dynamically(input_matrix, duration_per_round))

if __name__ == "__main__":
    main()
