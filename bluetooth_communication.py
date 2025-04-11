# bluetooth_communication.py

import asyncio
from bleak import BleakScanner, BleakClient
from config import TARGET_NAME, CHAR_UUID
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

async def send_commands_via_bluetooth(commands):
    log("🔍 正在扫描HM-10蓝牙设备...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if d.name and TARGET_NAME in d.name), None)

    if not target:
        log("❌ 未找到目标蓝牙设备")
        return

    async with BleakClient(target.address) as client:
        if not client.is_connected:
            log("❌ 蓝牙连接失败")
            return

        log("✅ 已连接蓝牙设备")

        for cmd in commands:
            full_cmd = cmd + "\n"
            await client.write_gatt_char(CHAR_UUID, full_cmd.encode())
            log(f"📤 发送命令: {cmd}")
            await asyncio.sleep(0.3)

        log("📡 命令发送完成")
