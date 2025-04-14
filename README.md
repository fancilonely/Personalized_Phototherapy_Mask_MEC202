# 📘 MEC202《个性化光疗面罩》项目 Version 1.0· Python技术文档
**项目成员专用 | 禁止XJTLU其他小组抄袭**  
**更新日期：2025.4.10**  
**课程：MEC202 | 合作方：苏州市中医医院**

---

## 👆 更新描述
- version 1.1: New logic: multiple phototherapy and reading csv input files.

- Version 1.0: All logic of python and arduino part is completed to realize simple phototherapy task.

- Version 0.4: The RGB light band of WS2812B is controlled by matrix input under HM-10 Bluetooth.

- Version 0.3: The code is updated to realize the control of RGB light band of WS2812B under HM-10 Bluetooth.

- Version 0.2: The code is updated to realize the control of LED on and off under HM-10 Bluetooth

---

## 💡 Arduino UNO R3 代码 version 0.3/0.4/1.0/1.1

Arduino:

    #include <SoftwareSerial.h>
    #include <Adafruit_NeoPixel.h>

    #define LED_COUNT 10   // 每条灯带上的 LED 数量

    // 每个对象只传入 LED 数量
    Adafruit_NeoPixel rgb_display_7(LED_COUNT);  
    Adafruit_NeoPixel rgb_display_8(LED_COUNT);
    Adafruit_NeoPixel rgb_display_9(LED_COUNT);
    Adafruit_NeoPixel rgb_display_10(LED_COUNT);
    Adafruit_NeoPixel rgb_display_11(LED_COUNT);

    // 定义蓝牙模块所使用的软件串口（例如 D2 为 RX，D3 为 TX）
    SoftwareSerial BTSerial(2, 3);

    void setup() {
      Serial.begin(9600);
      BTSerial.begin(9600);

      // 分别初始化5条灯带
      rgb_display_7.begin();
      rgb_display_7.setPin(7);  // 设定 PWM 引脚为 7
      rgb_display_7.clear();
      rgb_display_7.show();

      rgb_display_8.begin();
      rgb_display_8.setPin(8);
      rgb_display_8.clear();
      rgb_display_8.show();

      rgb_display_9.begin();
      rgb_display_9.setPin(9);  
      rgb_display_9.clear();
      rgb_display_9.show();

      rgb_display_10.begin();
      rgb_display_10.setPin(10);
      rgb_display_10.clear();
      rgb_display_10.show();

      rgb_display_11.begin();
      rgb_display_11.setPin(11);
      rgb_display_11.clear();
      rgb_display_11.show();

      Serial.println("Arduino 启动，等待蓝牙指令...");
    }

    void loop() {
      if (BTSerial.available()) {
        // 读取一行蓝牙指令（以换行符为结束）
        String cmd = BTSerial.readStringUntil('\n');
        cmd.trim();  // 去除首尾空格
        Serial.println("收到指令：" + cmd);

        // 要求指令格式为 "PINn:R,G,B"，例如 "PIN9:255,0,0"
        if (cmd.startsWith("PIN")) {
          int pin = -1;
          int r = 0, g = 0, b = 0;
          int colonIndex = cmd.indexOf(':');
          if (colonIndex != -1) {
            // 提取 PIN 后面的数字（引脚号）
            String pinStr = cmd.substring(3, colonIndex);
            pin = pinStr.toInt();

            // 提取颜色部分，格式 R,G,B
            String rgbStr = cmd.substring(colonIndex + 1);
            int firstComma = rgbStr.indexOf(',');
            int secondComma = rgbStr.lastIndexOf(',');
            if (firstComma != -1 && secondComma != -1 && firstComma != secondComma) {
              r = rgbStr.substring(0, firstComma).toInt();
              g = rgbStr.substring(firstComma + 1, secondComma).toInt();
              b = rgbStr.substring(secondComma + 1).toInt();
           }
          }

          // 验证引脚范围和颜色值（要求颜色值仅能为 0 或 255，确保实现开/关效果）
          if (pin >= 7 && pin <= 11 && ((r == 0 || r == 255) && (g == 0 || g == 255) && (b == 0 || b == 255))) {

            // 根据 PIN 号判断具体的 LED 灯带对象，然后设置每个 LED 的颜色并调用 show() 刷新显示
            if (pin == 7) {
              for (int i = 0; i < LED_COUNT; i++) {
                rgb_display_7.setPixelColor(i, r, g, b);
              }
              rgb_display_7.show();
            } else if (pin == 8) {
              for (int i = 0; i < LED_COUNT; i++) {
                rgb_display_8.setPixelColor(i, r, g, b);
              }
              rgb_display_8.show();
            } else if (pin == 9) {
              for (int i = 0; i < LED_COUNT; i++) {
                rgb_display_9.setPixelColor(i, r, g, b);
              }
              rgb_display_9.show();
            } else if (pin == 10) {
              for (int i = 0; i < LED_COUNT; i++) {
                rgb_display_10.setPixelColor(i, r, g, b);
              }
              rgb_display_10.show();
            } else if (pin == 11) {
              for (int i = 0; i < LED_COUNT; i++) {
                rgb_display_11.setPixelColor(i, r, g, b);
              }
              rgb_display_11.show();
            }
            BTSerial.println("OK: PIN" + String(pin) + ":" + String(r) + "," + String(g) + "," + String(b));
          } else {
            BTSerial.println("ERR: INVALID FORMAT OR VALUES");
          }
        } else {
          BTSerial.println("ERR: UNKNOWN COMMAND");
        }
      }
    }

---

## 🔰 项目概述

本项目是基于深度学习分析的「面部病变区域识别 + 光源治疗策略」的数据控制系统，使用 Python 连接蓝牙模块，将识别结果转换成 Arduino 可读懂的 LED PWM 指令。

---

## 📚 整体流程

```
[面部图像] → [AI识别 (ResNet18)] → [Python处理] → [通讯 (BLE/串口)] → [Arduino] → [PWM LED]
```

- Python 读取识别结果 (json/矩阵)
- 生成格式为 `PINx:val` 的指令
- BLE/串口方式发送给 Arduino
- Arduino 输出 PWM 控制 LED

---

## 🛠️ HM-10 BLE 模块说明

HM-10 是一款支持 BLE 4.0 协议的低功耗蓝牙模块，符合 GATT 通信规范，适合 Windows/Linux/macOS BLE 平台通信。

### 基本性能：
- 蓝牙名称默认为 `HMSoft`
- 默认通讯渠 UUID：
  - Service UUID: `0000ffe0-0000-1000-8000-00805f9b34fb`
  - Characteristic UUID: `0000ffe1-0000-1000-8000-00805f9b34fb`
- 通讯方式：收发都通过 GATT characteristic `FFE1`

### 硬件接线：
- HM-10 TXD 接 Arduino D2 (RX)
- HM-10 RXD 接 Arduino D3 (TX)
  - 需用两个 2kΩ 电阻给 D3 分压，将 5V 降至 2.5V~3.3V，保护 HM-10 RX
- VCC 可接 Arduino 5V
- GND 同地

### 处理策略：
- 大多数环境下我们无法创建虚拟串口，所以我们采用了基本的蓝牙API进行通信。
- HC-05和HC-06也是可用的，但是具体的库和协议有所不同。

### 操作步骤：
- 用ide烧录代码到arduino，注意蓝牙需先断开（RX/TX）
- 打开python，进行控制，可以输入OPEN/CLOSE开灯关灯(PIN9)

## HM-10 模块所需库

| 库名     | 功能说明 | 是否必须 |
|----------|----------|-----------|
| **`bleak`** | 	轻量级、跨平台的 Python BLE (Bluetooth Low Energy) 通信库 | 用于与 HM-10 建立 BLE 连接、发送指令、接收反馈（通过 GATT） | ✅ 必须 |
| `asyncio`   | Python内建异步通信框架 | bleak 基于 asyncio，因此用它运行主程序 |❌ 备选 |
| `datetime`  | 打印日志时间戳等 | 内建库，不需安装 |❌ 备选 |
| `logging`   | 替代 print 做更正式的调试日志 | 可选 |❌ 备选 |
| `json`      | 若需读取 AI 模型输出结果 | 若你处理 `.json` 格式 AI 结果，可使用 |❌ 备选 |


## HC-05/06 或串行情况下：

| 必要的库 | 原因 |
|------------|------|
| `pyserial` | HM-10 是 BLE，不会创建串口（COM） |
| `pybluez`  | 只支持经典蓝牙（如 HC-05），不能用于 BLE |

---
## 本版本更新：
- 多串口多方向的开发，PINn:R,G,B的引脚：开关指令的设计。
- 输入矩阵转化为引脚指令。
- 开启后自动读取数据，自动关闭。

## 下版本更新：
- 自动化处理识别的结果。
- 时间函数和亮度函数。

**特别提示：**
- HM-10 BLE 非传统蓝牙，无 COM端口，需用 `bleak` 连接
- 不支持 PyBluez 类似协议


## Version 0.2 LED 代码参考
Python:


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




