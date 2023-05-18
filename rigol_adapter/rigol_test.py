# __author__ = 'sn01309'
# coding=utf-8
import threading
import time
import pyvisa
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                                   NavigationToolbar2Tk)

class MyThread1(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()

    def run(self):
        self.func(*self.args)


class MyThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.func()

    def stop(self):
        self.stop_event.set()


class ricol():
    __console = ''
    __call = ''

    def __init__(self, IDN):
        self.IDN = IDN

    def connect(self):
        try:
            self.__console = pyvisa.ResourceManager()
            self.__call = self.__console.open_resource(f"{self.IDN}")
            myprint("connect RIGOL result: ---> success")
        except Exception as e:
            myprint("connect RIGOL result: ---> fail")
            myprint("fail: ---> {}".format(e))

    def set_modul(self):
        try:
            self.__call.write("SOUR:LIST:MODE CC")
            self.__call.write("SOUR:LIST:MODE?")
            modul = self.__call.read()
            myprint(f"set modul success: ---> {modul}")
        except:
            myprint(f"set modul fail: ---> {modul}")

    # def send_commend(self,commend):
    #     try:
    #         self.__call.write(commend)
    #         send_result=self.__call.read()
    #         myprint(f"send commmend success: ---> {send_result}")
    #         return send_result
    #     except Exception as e:
    #         myprint(f"send commmend fail: ---> {e}")

    def read_IDN(self):
        try:
            self.__call.write("*IDN?")
            result = self.__call.read()
            myprint(f"read IDN success: ---> {result}")
            return result
        except Exception as e:
            myprint(f"read IDN fail: ---> {e}")

    def set_current(self, current):
        self.__call.write(f"SOUR:CURR:LEV:IMM {current}")
        time.sleep(1)
        self.__call.write("SOUR:CURR:LEV:IMM?")
        currentd = self.__call.read()
        myprint(f"set current success: ---> {currentd}")

    def cc_button(self):
        self.__call.write("SYST:KEY 0")

    def ON_OFF_button(self):
        self.__call.write("SYST:KEY 32")

    def read_v(self):
        global number
        self.__call.write("MEASure:VOLTage:DC?")
        v = self.__call.read()
        number.append(v.replace('\n', '').replace("", ""))
        myprint(f"read volta: ---> {v}")

    def close(self):
        self.__call.close()


# class CServer(threading.Thread):
#
#     def __init__(self, name, lock):
#         threading.Thread.__init__(self)
#         self.mName = name
#         self.mLock = lock
#         self.mEvent = threading.Event()
#
#     def run(self):
#         count = 0
#
#         while (True):
#             self.mEvent.wait()
#             self.mLock.acquire()
#             count += 1
#             print("CServer::{}   count{}".format(self.mName, count))
#             self.mLock.release()
#             time.sleep(3)
#
#     def pause(self):
#         self.mEvent.clear()
#
#     def resume(self):
#         self.mEvent.set()


if __name__ == '__main__':
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
    def start():
        global thread
        thread = MyThread(test)
        thread.start()
    def stop():
        global t
        call.ON_OFF_button()
        thread.stop()
        colormyprint("程序暂停", 'red')
        # colormyprint(number, 'green')
        t = 0
    t = 0;number = [];x = []
    def test():
        try:
            global t, call, sent_current_A, sent_current_B, number
            if t == 0:
                # call=ricol("USB0::0x1AB1::0x0E11::DL3A245001322::INSTR")
                call = ricol(entry_1.get())
                call.connect()
                IDN = call.read_IDN()
                call.set_modul()
                call.cc_button()
                call.ON_OFF_button()
                sent_current_A = entry_2.get()
                sent_current_B = entry_3.get()
                call.set_current(f"{sent_current_A}")
                call.read_v()
                myprint(f"start sleep {int(entry_4.get())} time")
                time.sleep(int(entry_4.get()))
                call.set_current(f"{sent_current_B}")
                call.read_v()
                myprint(f"start sleep {int(entry_5.get())} time")
                time.sleep(int(entry_5.get()))
                t += 1
            else:
                call.set_current(f"{sent_current_A}")
                call.read_v()
                myprint(f"start sleep {int(entry_4.get())} time")
                time.sleep(int(entry_4.get()))
                call.set_current(f"{sent_current_B}")
                call.read_v()
                myprint(f"start sleep {int(entry_5.get())} time")
                time.sleep(int(entry_5.get()))
        except Exception as e:
            call.ON_OFF_button()
            call.close()
            colormyprint(f"error ----> : {e}",'red')
    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        for i, v in enumerate(number):
            number[i] = float(v)
        plot1 = fig.add_subplot(111)
        plot1.plot(number)
        if checkbut_limit_3.get()==1:
            myprint("设置电压limit正负3%")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 0.97}")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 1.03}")
            myprint(round(int(number[0]), 0))
            plot1.axhline(y=int(number[0])*0.97, ls=":", c="green", lw=3)  # 添加水平直线
            plot1.axhline(y=int(number[0]) * 1.03, ls=":", c="green", lw=3)
        elif checkbut_limit_5.get()==1:
            myprint("设置电压limit正负5%")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 0.95}")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 1.05}")
            myprint(round(int(number[0]), 0))
            plot1.axhline(y=int(number[0]) * 0.95, ls=":", c="green", lw=3)  # 添加水平直线
            plot1.axhline(y=int(number[0]) * 1.05, ls=":", c="green", lw=3)
        else:
            myprint("未设置电压limit，默认正负3%")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 0.97}")
            myprint(f"volaet limit : {round(int(number[0]), 0) * 1.03}")
            myprint(round(int(number[0]), 0))
            round(int(number[0]), 0)
            plot1.axhline(y=int(number[0]) * 0.97, ls=":", c="green", lw=3)  # 添加水平直线
            plot1.axhline(y=int(number[0]) * 1.03, ls=":", c="green", lw=3)
        canvas = FigureCanvasTkAgg(fig,
                                   master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                       window)
        toolbar.update()
        canvas.get_tk_widget().pack()
    def clear():
        global number
        number=[]
        colormyprint(f"清除number：{number}",'red')
    def chart():
        try:
            global window ,number
            window = tk.Toplevel(root)
            window.title('Plotting in Tkinter')
            window.geometry("500x500")
            frame = tk.Frame(window)
            frame.pack()
            plot_button = tk.Button(frame, text='Plot', font=("Consolas", 11),command=plot)
            plot_button.pack(side=LEFT, ipadx=10, padx=20)

            button3 = tk.Button(frame, text='clear', font=("Consolas", 11),command=clear)
            button3.pack(side=LEFT, after=plot_button, ipadx=10, padx=20)
            window.mainloop()
            thread.stop()
        except Exception as e:
            myprint(e)
            print(e)

    def start_chart():
        global thread
        thread = MyThread(chart)
        thread.start()
    button2 = tk.Button(frame, text='stop', font=("Consolas", 11))
    button2.pack(side=LEFT, after=button, ipadx=10, padx=20)
    button2['command'] = lambda: stop()
    button3 = tk.Button(frame, text='chart', font=("Consolas", 11))
    button3.pack(side=LEFT, after=button2, ipadx=10, padx=20)
    button3['command'] = lambda: MyThread1(chart())
    frame1 = tk.Frame(root)
    frame1.pack()

    label_4 = Label(frame1, width=15, text="电流A持续时间:", font=("黑体", 11))
    label_4.pack(side=LEFT, padx=0, pady=10)
    entry_4 = Entry(frame1, width=10, font=("Consolas", 11))
    entry_4.pack(side=LEFT, after=label_4, padx=0, pady=10, fill=X)
    label_5 = Label(frame1, width=15, text="电流B持续时间:", font=("黑体", 11))
    label_5.pack(side=LEFT, after=entry_4, padx=10, pady=10)
    entry_5 = Entry(frame1, width=10, font=("Consolas", 11))
    entry_5.pack(side=LEFT, after=label_5, padx=0, pady=10, fill=X)

    checkbut_limit_3=BooleanVar()
    checkbtn_1=Checkbutton(frame1, width=10,text="3%",variable=checkbut_limit_3, font=("Consolas",11))
    checkbtn_1.pack(side=LEFT,after=entry_5)

    checkbut_limit_5=BooleanVar()
    checkbtn_2=Checkbutton(frame1, width=10,text="5%",variable=checkbut_limit_5, font=("Consolas",11))
    checkbtn_2.pack(side=LEFT, after=checkbtn_1)


    # 显示help信息
    frame2 = tk.LabelFrame(root, text='Help', height=7, font=("consolas", 11))
    frame2.pack(fill=tk.BOTH, expand=0)
    textMess_2 = ScrolledText(frame2, bg='white', height=7, font=("consolas", 11))
    textMess_2.pack(fill=tk.BOTH, expand=1)
    textMess_2.insert(tk.END, "IDN :      The IDN you want to scan : USB0::0x1AB1::0x0E11::DL3A245001322::INSTR\n")
    textMess_2.insert(tk.END, "CURRENTA : Current A is the current set for the first time,\n "
                              "          which is generally 75% of the limit current of the adapter\n")
    textMess_2.insert(tk.END, "CURRENTB : Current B is the current set for the second time,\n "
                              "          which is generally 100% of the limit current of the adapter or overloaded\n")
    textMess_2.insert(tk.END, "start:     Start running the program\n")
    textMess_2.insert(tk.END, "stop:      Stop running the program\n")
    textMess_2.insert(tk.END, "chart:     Shows a line chart made from voltage\n")
    textMess_2.insert(tk.END, "3%:        The upper limit of voltage is set to 3%\n")
    textMess_2.insert(tk.END, "5%:        The upper limit of voltage is set to 5%\n")
    textMess_2.insert(tk.END, "Current A duration: Set current A holding time\n")
    textMess_2.insert(tk.END, "Current B duration: Set current B holding time\n")


    # 为信息框设置一个容器
    frame3 = tk.LabelFrame(root, text='信息框', height=10, font=("黑体", 11))
    frame3.pack(fill=tk.BOTH, expand=1)
    # 放置一个文本框作为信息输出窗口
    textMess = ScrolledText(frame3, bg='white', height=10, font=("consolas", 11))
    textMess.pack(fill=tk.BOTH, expand=YES)

    # # 输出信息
    def myprint(txt):
        global textMess
        if textMess != None:
            textMess.insert(tk.END, txt)
            textMess.insert(tk.END, '\n')
            textMess.see(tk.END)
    # 输出回车
    def myprint_n():
        global textMess
        textMess.insert(tk.END, '\n')
        textMess.see(tk.END)
    # 输出彩色信息
    def colormyprint(txt, color):
        global textMess
        if textMess != None:
            if color != 'black':
                textMess.tag_config(color, foreground=color)
            textMess.insert(tk.END, txt, color)
            textMess.insert(tk.END, '\n')
            textMess.see(tk.END)
    # 进入Tkinter消息循环
    root.mainloop()
