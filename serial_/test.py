import serial
import tkinter as tk

# 创建串口对象
ser = serial.Serial()

# 设置串口号
ser.port = 'COM3'

# 设置波特率
ser.baudrate = 115200

# 打开串口
ser.open()

# 创建tkinter窗口
window = tk.Tk()

# 创建文本框
text_box = tk.Text(window)
text_box.pack()

text_box.mainloop()

# 循环接收数据，此为死循环，可用线程实现
while True:
    # 获取单次串口数据
    data = ser.readline()

    # 在文本框中显示数据
    text_box.insert(tk.END, data)

    # 更新窗口
    window.update()

