# usb_communication.py
import serial
import time
import logging

def send_commands_via_usb(commands, port, baudrate):

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # 等待串口稳定
        logging.info("已打开串口 %s，波特率 %d。", port, baudrate)

        for cmd in commands:
            command_str = cmd + "\n"
            ser.write(command_str.encode())
            logging.info("已发送指令: %s", command_str.strip())
            time.sleep(0.1)  # 短暂延迟，避免发送过快

        ser.close()
        logging.info("所有指令发送完毕，串口已关闭。")
    except Exception as e:
        logging.error("串口通信出错: %s", e)
