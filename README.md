本项目为XJTLU的MEC202课程项目Personalized Phototherapy Mask的Python部分代码,该项目是与苏州市中医院合作的工业项目。
禁止任何XJTLU的其他小组学生剽窃抄袭本项目代码的行为。

以下内容为材料参考，提供给项目参与者。

Python代码的运行步骤大致可以分为以下几个部分：

    启动程序
        当在命令行或IDE中运行 main.py 时，程序从 if __name__ == "__main__": 开始执行。

    数据获取与处理
        在 main.py 中，会定义一个输入矩阵（例如，从深度学习模型得到的9×4矩阵），该矩阵包含了各个区域的光疗需求信息。
        程序调用 data_processing.py 中的 generate_commands(input_matrix) 函数，该函数会遍历输入矩阵，根据预先在 config.py 中定义好的 PIN_MAPPING 映射表，将每个区域和颜色的状态（1表示需要光疗，0表示不需要）转换为控制指令字符串，比如 "PIN10:255"（表示将对应引脚输出最大亮度）或 "PIN10:0"（表示关闭）。

    生成控制指令
        generate_commands 函数会返回一个包含所有控制指令的列表。此时，可以在日志中看到这些指令的输出，便于调试和确认数据处理是否正确。

    USB串口通信
        程序随后调用 usb_communication.py 中的 send_commands_via_usb(commands, port, baudrate) 函数，将生成的控制指令逐条发送到 Arduino。
        在该函数中，程序会打开指定的串口（例如 COM3），等待连接稳定，然后逐条将指令发送出去（每条指令后附加一个换行符 \n 作为结束标志）。
        每发送一条指令后，会有一个短暂延时，以避免数据发送过快导致问题。所有指令发送完成后，函数关闭串口，并在日志中记录发送状态。

    程序结束
        当所有指令发送完毕后，main() 函数结束，Python程序退出。
        此时，Arduino已经通过USB接收到了这些控制指令，并根据预先烧录的Arduino代码执行相应的LED控制操作（例如将指定引脚输出PWM信号达到全亮或关闭的效果）。

总结来说，Python端的整体流程是：

    读取/定义输入数据 → 数据处理生成指令 → 通过USB串口发送指令 → 程序结束

 Arduino 示例代码，该代码能够从串口接收由 Python 发送的指令（例如 "PIN10:255"），解析指令后对对应引脚进行 PWM 控制。你可以将以下代码烧录到 Arduino 开发板中，Arduino 程序独立运行，等待电脑通过 USB 发送控制指令。

    void setup() {
      Serial.begin(9600);  // 初始化串口，波特率需与 Python 端保持一致
      // 预设所有可能用到的引脚为输出模式
      // 如果你使用的是 Uno 板，建议设置数字引脚2~28
      for (int pin = 2; pin <= 28; pin++) {
        pinMode(pin, OUTPUT);
        analogWrite(pin, 0);  // 初始时关闭所有 LED
      }
      Serial.println("Arduino Ready");
    }

    void loop() {
      if (Serial.available() > 0) {
        // 读取直到换行符为止的一行数据
        String command = Serial.readStringUntil('\n');
        command.trim();  // 去除前后空白字符

        // 判断指令是否以 "PIN" 开头
        if (command.startsWith("PIN")) {
          int colonIndex = command.indexOf(':');
          if (colonIndex != -1) {
            // 提取引脚号和 PWM 值
            String pinStr = command.substring(3, colonIndex);
            String valueStr = command.substring(colonIndex + 1);
        
            int pin = pinStr.toInt();
            int value = valueStr.toInt();
        
            // 对应引脚输出 PWM 信号
            analogWrite(pin, value);
        
            // 可选：通过串口反馈信息，便于调试
            Serial.print("Set PIN");
            Serial.print(pin);
            Serial.print(" to ");
            Serial.println(value);
          } else {
            Serial.println("Invalid command format");
          }
        } else {
          Serial.println("Unknown command");
        }
      }
    }

代码说明

setup() 函数

1.使用 Serial.begin(9600); 初始化串口，波特率与 Python 端一致。

2.通过循环将数字引脚 2~28 统一设置为输出模式，并初始关闭（输出 0），确保在接收到指令前 LED 都处于关闭状态。

3.输出 "Arduino Ready" 表示程序已启动。


loop() 函数

1.判断是否有串口数据，若有则使用 Serial.readStringUntil('\n') 读取一行数据。

2.使用 trim() 去除前后空格，并判断指令是否以 "PIN" 开头。

3.通过 indexOf(':') 查找冒号分隔符，提取冒号前的引脚号和冒号后的 PWM 值，将其转换为整数。

4.使用 analogWrite(pin, value); 对对应引脚进行 PWM 控制，实现 LED 全亮（255）或关闭（0）。 

5.最后输出调试信息，反馈当前操作结果。

这样，在实际使用中，当 Python 程序通过 USB 串口发送类似 "PIN10:255\n" 的指令时，Arduino 程序就会解析出引脚号 10 并将其 PWM 输出设为 255，从而使接在引脚 10 上的 LED 达到最大亮度。可以根据实际需要对代码进行进一步扩展或调整。
