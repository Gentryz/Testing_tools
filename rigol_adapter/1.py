
#
#
# # y=12.433788 12.433878 12.433952 11.887831 12.051287 11.898119
# # str1 = y.replace("","")
# # print(str1)
#
# import matplotlib.pyplot as plt
# x=[]
# numbers = ['12.210466', '11.830385', '12.015356', '11.844238', '12.023359', '11.854380']
# for i, v in enumerate(numbers):
#     numbers[i] = float(v)
#
# print(len(numbers))
# for i in range(len(numbers)):
#     x.append(i+1)
# print(x,numbers)
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *

mytitle = '适配器变交测试'
global textMess
# 建立主窗口
root = tk.Tk()
root.title(mytitle)
root.geometry('{}x{}+{}+{}'.format(900, 650, 400, 75))
frame = tk.Frame(root)
frame.pack()
label_1 = Label(frame, width=10, text="请输入IDN:", font=("黑体", 11))
label_1.pack(side=LEFT, padx=0, pady=10)
entry_1 = Entry(frame, width=20, font=("Consolas", 11))
entry_1.pack(side=LEFT, after=label_1, padx=10, pady=10, fill=X)
label_2 = Label(frame, width=5, text="电流A:", font=("黑体", 11))
label_2.pack(side=LEFT, after=entry_1, padx=10, pady=10)
entry_2 = Entry(frame, width=10, font=("Consolas", 11))
entry_2.pack(side=LEFT, after=label_2, padx=0, pady=10, fill=X)
label_3 = Label(frame, width=5, text="电流B:", font=("黑体", 11))
label_3.pack(side=LEFT, after=entry_2, padx=10, pady=10)
entry_3 = Entry(frame, width=10, font=("Consolas", 11))
entry_3.pack(side=LEFT, after=label_3, padx=0, pady=10, fill=X)
timeout = tk.IntVar(value=3)
button = tk.Button(frame, text='start', font=("Consolas", 11))
button.pack(side=LEFT, after=entry_3, ipadx=10, padx=20)
button['command'] = lambda: start()
button2 = tk.Button(frame, text='stop', font=("Consolas", 11))
button2.pack(side=LEFT, after=button, ipadx=10, padx=20)
button2['command'] = lambda: stop()
button3 = tk.Button(frame, text='chart', font=("Consolas", 11))
button3.pack(side=LEFT, after=button2, ipadx=10, padx=20)
button3['command'] = lambda: MyThread1(chart())
frame1 = tk.Frame(root)
frame1.pack()
# 显示help信息
frame2 = tk.LabelFrame(root, text='Help', height=7, font=("consolas", 11))
frame2.pack(fill=tk.BOTH, expand=0)
textMess_2 = ScrolledText(frame2, bg='white', height=7, font=("consolas", 11))
textMess_2.pack(fill=tk.BOTH, expand=1)
textMess_2.insert(tk.END, "IDN : The IDN you want to scan : USB0::0x1AB1::0x0E11::DL3A245001322::INSTR\n")
textMess_2.insert(tk.END, "CURRENTA : Current A is the current set for the first time,\n "
                          "           which is generally 75% of the limit current of the adapter\n")
textMess_2.insert(tk.END, "CURRENTB : Current B is the current set for the second time,\n "
                          "           which is generally 100% of the limit current of the adapter or overloaded\n")
textMess_2.insert(tk.END, "start: Start running the program\n")
textMess_2.insert(tk.END, "stop:  Stop running the program\n")
textMess_2.insert(tk.END, "chart: Shows a line chart made from voltage\n")

# 为信息框设置一个容器
frame3 = tk.LabelFrame(root, text='信息框', height=10, font=("黑体", 11))
frame3.pack(fill=tk.BOTH, expand=1)
# 放置一个文本框作为信息输出窗口
textMess = ScrolledText(frame3, bg='white', height=10, font=("consolas", 11))
textMess.pack(fill=tk.BOTH, expand=YES)
root.mainloop()