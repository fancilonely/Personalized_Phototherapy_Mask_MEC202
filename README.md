# 📘 MEC202《个性化光疗面罩》项目 · Python技术文档  
**项目成员专用 | 禁止XJTLU其他小组剽窃抄袭**  
**更新日期：2025.3.24**  
**课程：MEC202 | 合作方：苏州市中医医院**
- 项目背景说明
- Python模块职责与整体架构
- 蓝牙与USB控制方案代码示例
- Arduino端详细解释与代码
- 接线图建议与扩展方向

## 🔰 项目简介与模块定位

本项目为西交利物浦大学MEC202课程下的工业合作项目，旨在开发一款基于AI诊断的**个性化面部光疗面罩**系统。项目核心包括：

- 使用深度学习模型（ResNet18）识别面部9个区域的皮肤病症；
- 生成区域对应的治疗方案（红光、黄光、蓝光）；
- 通过Python处理识别结果，转换为Arduino可理解的控制指令；
- 最终驱动27个LED完成局部治疗。

这里提供的部分是 **Python数据处理与串口通信模块**，实现从AI识别 → 控制光源的整个控制路径。


## 🧩 系统流程简图

```plaintext
[ 手机摄像头 ] → [ 电脑AI识别 ] → [ Python处理+串口输出 ] → [ Arduino ] → [ 发光面罩 ]
```

- Python部分：读取AI模型输出的矩阵（或JSON），筛选置信度、生成控制命令，如 `"PIN10:255"`。
- Arduino端：接收指令，通过PWM控制对应区域的LED亮度。

# 具体举例
```plaintext
[ 电脑 (Python脚本) ] → 蓝牙串口发送控制命令 → [ 蓝牙虚拟串口 (如 COM5) ] →蓝牙通信 → [ HC-05 模块 ] → 串口数据传输 →  [ Arduino 板 ] → PWM 控制LED→ [ LED阵列发光（蓝/红/黄） ]
```

## 🟦 Python 蓝牙控制代码（适用于无线HC-05）

```python
import serial
import time

BLUETOOTH_PORT = 'COM5'  # ⚠️请替换为实际端口 HC-05是USB最方便替换的方案；也是同样使用串口输出。使用蓝牙连接，采用虚拟端口。
BAUDRATE = 9600

try:
    bluetooth = serial.Serial(BLUETOOTH_PORT, BAUDRATE)
    print("已连接蓝牙模块")
    time.sleep(2)
except:
    print("串口连接失败，请确认蓝牙是否配对成功")
    exit()

commands = ["PIN3:255", "PIN5:128", "PIN6:0"]

for cmd in commands:
    bluetooth.write((cmd + "\n").encode())
    print("发送指令：", cmd)
    time.sleep(0.2)

bluetooth.close()
print("指令全部发送完成。")
```

📌 **格式说明**：
- `"PIN3:255"`：表示引脚3全亮。
- `"PIN6:0"`：表示引脚6关闭。
- 前面是引脚，后面是亮度(0-255)


## 🟩 Arduino 端串口接收与控制代码（适用于USB或蓝牙）

```cpp
#include <SoftwareSerial.h>
SoftwareSerial bluetooth(10, 11); // D10=RX, D11=TX（用于HC-05）

void setup() {
  bluetooth.begin(9600);
  Serial.begin(9600); // 调试用
  for (int pin = 2; pin <= 13; pin++) {
    pinMode(pin, OUTPUT);
    analogWrite(pin, 0);
  }
  bluetooth.println("Arduino蓝牙准备就绪");
}

void loop() {
  if (bluetooth.available()) {
    String cmd = bluetooth.readStringUntil('\n');
    cmd.trim();
    if (cmd.startsWith("PIN")) {
      int pin = cmd.substring(3, cmd.indexOf(':')).toInt();
      int value = cmd.substring(cmd.indexOf(':') + 1).toInt();
      analogWrite(pin, value);
      Serial.println("执行：" + cmd);
    }
  }
}
```


## 🔌 HC-05 蓝牙模块与 Arduino 连接图

| HC-05 引脚 | 接 Arduino | 说明            |
|------------|-------------|-----------------|
| VCC        | 5V          | 电源            |
| GND        | GND         | 接地            |
| TXD        | D10         | 模块发送 → 板子接收 |
| RXD        | D11（需降压）| 板子发送 → 模块接收（⚠ 需分压）|

💡 降压方法：D11 → 1kΩ → 分接 → 2kΩ → GND → RXD


## 🧪 Python 示例：处理深度学习结果 → 自动生成控制指令

```python
input_data = {
  "predictions": [
    {"region": "forehead", "confidence": 0.92, "treatment": "Blue Light"},
    {"region": "cheek_left", "confidence": 0.87, "treatment": "Pulsed Dye Laser"},
    {"region": "chin", "confidence": 0.65, "treatment": "Red Light"}
  ]
}

pin_map = {
    "forehead": {"pin": 3, "treatment": "Blue Light"},
    "cheek_left": {"pin": 5, "treatment": "Pulsed Dye Laser"},
    "chin": {"pin": 6, "treatment": "Red Light"}
}

def generate_commands(data, threshold=0.80):
    result = []
    for pred in data["predictions"]:
        if pred["confidence"] >= threshold and pred["region"] in pin_map:
            match = pin_map[pred["region"]]
            value = 255 if pred["treatment"] == match["treatment"] else 0
            result.append(f"PIN{match['pin']}:{value}")
    return result
```


## 🧱 项目模块化说明（对应交付）

模块 | 功能 | 技术
------|------|-----
数据预处理模块 | AI输出 → 区域识别矩阵 | Python + NumPy
控制指令模块 | 转换为 "PINx:xxx" 格式 | Python
串口通信模块 | 发送至Arduino | pyserial
日志记录模块 | 指令输出与异常处理 | Python `logging`
Arduino接收控制模块 | 接收串口指令并控制PWM输出 | C/C++ (Arduino IDE)


## 🏁 测试建议

- 💡 使用USB调试时可用Arduino串口监视器直接输入 `PIN3:255` 测试；
- 💡 蓝牙测试前先完成配对，并确认COM口（设备管理器中可查看）；
- 💡 若LED不亮，请检查：
  - 引脚对应是否正确；
  - 是否加了限流电阻（如220Ω）；
  - 是否有供电问题；
  - 波特率是否一致（9600）。
