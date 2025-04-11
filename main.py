import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime

TARGET_NAME = "HMSoft"  # HM-10 的设备名
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"  # HM-10 所使用的特征 UUID

def log(msg):
    """打印带时间戳的日志消息"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def notification_handler(sender, data):
    """处理从 Arduino / 蓝牙模块返回的通知消息"""
    log(f"Arduino 回复: {data.decode().strip()}")

async def main():
    log("🔍 正在扫描 HM-10 蓝牙设备...")
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
                # 提示用户输入指令，格式要求为 PINn:R,G,B
                cmd = input("📤 请输入指令 (格式: PINn:R,G,B，例如 PIN7:255,0,0；输入 exit 退出)：").strip()
                if cmd.lower() in ["exit", "quit"]:
                    break
                # 补充换行符保证 Arduino 使用 readStringUntil('\n') 正确解析
                if not cmd.endswith("\n"):
                    cmd += "\n"
                await client.write_gatt_char(CHAR_UUID, cmd.encode())
                log(f"✅ 已发送: {cmd.strip()}")
                # 稍作延时，确保命令发送完成
                await asyncio.sleep(0.5)
        except KeyboardInterrupt:
            log("⛔ 中断退出")

        await client.stop_notify(CHAR_UUID)
        log("🔌 已断开连接")

asyncio.run(main())
