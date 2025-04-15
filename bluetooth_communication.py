# bluetooth_communication.py
import asyncio
from bleak import BleakScanner, BleakClient
from config import TARGET_NAME, CHAR_UUID
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

class BluetoothController:
    def __init__(self):
        self.client = None

    async def connect(self):
        log("🔍 正在扫描HM-10蓝牙设备...")
        devices = await BleakScanner.discover()
        target = next((d for d in devices if d.name and TARGET_NAME in d.name), None)

        if not target:
            log("❌ 未找到目标蓝牙设备")
            return

        self.client = BleakClient(target.address)
        await self.client.connect()

        if not self.client.is_connected:
            log("❌ 蓝牙连接失败")
            self.client = None
        else:
            log("✅ 已连接蓝牙设备")

    async def send_command(self, cmd):
        if not self.client or not self.client.is_connected:
            log("⚠️ 蓝牙尚未连接")
            return
        await self.client.write_gatt_char(CHAR_UUID, (cmd + "\n").encode())
        log(f"📤 发送命令: {cmd}")
        await asyncio.sleep(0.2)  # 防止堆积太快

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            log("🔌 已断开蓝牙连接")
