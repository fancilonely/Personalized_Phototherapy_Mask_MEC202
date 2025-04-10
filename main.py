import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime

TARGET_NAME = "HMSoft"  # 你的 BLE 模块名字
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def notification_handler(sender, data):
    log(f"🧠 Arduino 回复: {data.decode().strip()}")

async def main():
    log("🔍 正在扫描 HM-10...")
    devices = await BleakScanner.discover()
    target = None
    for d in devices:
        if d.name and TARGET_NAME in d.name:
            target = d
            break

    if not target:
        log("❌ 未找到 HMSoft")
        return

    async with BleakClient(target.address) as client:
        if not client.is_connected:
            log("❌ 连接失败")
            return

        log("✅ 已连接 HMSoft")
        await client.start_notify(CHAR_UUID, notification_handler)

        try:
            while True:
                cmd = input("📤 输入指令 (OPEN / CLOSE / exit)：").strip()
                if cmd.lower() in ["exit", "quit"]:
                    break
                if not cmd.endswith("\n"):
                    cmd += "\n"
                await client.write_gatt_char(CHAR_UUID, cmd.encode())
                log(f"✅ 已发送: {cmd.strip()}")
                await asyncio.sleep(0.5)
        except KeyboardInterrupt:
            log("⛔ 中断退出")

        await client.stop_notify(CHAR_UUID)
        log("🔌 已断开连接")

asyncio.run(main())
