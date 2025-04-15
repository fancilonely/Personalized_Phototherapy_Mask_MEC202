# main.py
import asyncio
from data_processing import read_matrix_from_csv, generate_commands
from bluetooth_communication import BluetoothController
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

class RegionController:
    def __init__(self, zone_id, rgb_flags, total_duration, ble_controller):
        self.zone_id = zone_id
        self.rgb_flags = rgb_flags  # [R, G, B]
        self.total_duration = total_duration
        self.ble_controller = ble_controller
        self.subtasks = self._build_subtasks()
        self.step_duration = total_duration / len(self.subtasks) if self.subtasks else 0

    def _build_subtasks(self):
        tasks = []
        if self.rgb_flags[0]:
            tasks.append([self.zone_id, 1, 0, 0])
        if self.rgb_flags[1]:
            tasks.append([self.zone_id, 0, 1, 0])
        if self.rgb_flags[2]:
            tasks.append([self.zone_id, 0, 0, 1])
        return tasks

    async def run(self):
        for matrix in self.subtasks:
            await self.ble_controller.send_command(f"PIN{self.zone_id + 6}:0,0,0")
            await asyncio.sleep(0.1)

            cmd = generate_commands([matrix])[0]
            await self.ble_controller.send_command(cmd)

            await asyncio.sleep(2)  # ✅ 给 Arduino 2秒缓冲显示
            log(f"[ZONE {self.zone_id}] 发光 {matrix[1:]}, 时长 {self.step_duration:.2f}s")

            await asyncio.sleep(self.step_duration)


async def control_all_regions_parallel(matrix, total_duration):
    ble_controller = BluetoothController()
    await ble_controller.connect()

    if not ble_controller.client:
        return

    log(f"[INFO] 开始并行光疗，总时间：{total_duration}秒")

    # 为每个区域生成控制器
    tasks = []
    for row in matrix:
        zone, r, g, b = row
        controller = RegionController(zone, [r, g, b], total_duration, ble_controller)
        tasks.append(controller.run())

    await asyncio.gather(*tasks)

    # 所有区域关闭
    shutdown_matrix = [[row[0], 0, 0, 0] for row in matrix]
    shutdown_cmds = generate_commands(shutdown_matrix)
    for cmd in shutdown_cmds:
        await ble_controller.send_command(cmd)
        log(f"🛑 关闭命令: {cmd}")

    await asyncio.sleep(1)  # 给Arduino响应时间
    log("[INFO] ✅ 所有光疗完成并已关闭")

    await ble_controller.disconnect()

def main():
    file_path = "input_matrix.csv"
    input_matrix = read_matrix_from_csv(file_path)

    if not input_matrix:
        print("[ERROR] 输入矩阵为空或CSV文件格式错误")
        return

    total_time = 24  # ⏱️ 总时间
    asyncio.run(control_all_regions_parallel(input_matrix, total_time))

if __name__ == "__main__":
    main()
