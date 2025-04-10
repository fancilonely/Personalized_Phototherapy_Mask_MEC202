# 📘 MEC202《个性化光疗面罩》项目 · Python技术文档
**项目成员专用 | 禁止XJTLU其他小组剖裂抄袭**  
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

**特别提示：**
- HM-10 BLE 非传统蓝牙，无 COM端口，需用 `bleak` 连接
- 不支持 PyBluez 类似协议



