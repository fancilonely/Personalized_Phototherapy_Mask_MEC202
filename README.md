# 📘 MEC202《个性化光疗面罩》项目 · Python技术文档
**项目成员专用 | 禁止XJTLU其他小组抄袭**  
**更新日期：2025.4.10**  
**课程：MEC202 | 合作方：苏州市中医医院**

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
## 下一步的方向：
- 多串口多方向的开发，PINX:X的引脚：亮度指令的设计。
- 自动化处理识别的结果。

**特别提示：**
- HM-10 BLE 非传统蓝牙，无 COM端口，需用 `bleak` 连接
- 不支持 PyBluez 类似协议



