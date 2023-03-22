import ctypes
import inspect
import logging
import sys
import threading
from tkinter import *
import tkinter as tk
import  time
import os
import paramiko
from sys import *







class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()
        self._stop_event = threading.Event()

    def run(self):
        self.func(*self.args)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


    def _async_raise(self,tid, exctype):

        """raises the exception, performs cleanup if needed"""

        tid = ctypes.c_long(tid)

        if not inspect.isclass(exctype):
            exctype = type(exctype)

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

        if res == 0:

            raise ValueError("invalid thread id")

        elif res != 1:

            # """if it returns a number greater than one, you're in trouble,

            # and you should call it again with exc=NULL to revert the effect"""

            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)


UUTIP = []
UUTPWD =[]
COUNTT = []
INTERVAL = []

root = Tk()
root.geometry('840x440+200+200')
root.resizable(False,False)
root.title('反复重启测试')

def Check_Input(input, entry):
    ip_list = input.split(".")  # 将字符串按点分割成列表
    flag = True
    for num in ip_list:
        if len(ip_list) == 4 and num.isdigit() and 0 <= int(num) <= 255:
            continue
        else:
            flag = False
            break
    if flag:
        showinfo("输入是合法的ip地址")
        logging.info("输入是合法的ip地址")
    else:
        entry.delete(0, END)
        showinfo("输入不是合法的ip地址")
        logging.info("输入不是合法的ip地址")

def Check_Number(number, entry):
    if number.count('.') == 0:
        showinfo("输入是合法数字")
        logging.info("输入是合法数字")
    else:
        entry.delete(0, END)
        showinfo("输入不是合法数字")
        logging.info("输入不是合法数字")

def showinfo(result):
    """
    将系统时间和传入结果
    将结果显示在text框里面
    """
    realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + result
    text.insert("end", textvar)
    text.insert("insert", '\n')
    text.see("end")
    text.update()
    root.update_idletasks()

def UPshowinfo_info(event=''):
    status_label.configure(text="输入板子IP:" + IP_Input.get())
    showinfo("输入板子IP:" + IP_Input.get())
    logging.info("输入板子IP:" + IP_Input.get())
    Check_Input(IP_Input.get(), IP_Input)
    UUTIP.append(IP_Input.get())

def UPdelete_info(event=''):
    status_label.configure(text="清楚板子IP：" + IP_Input.get())

def UUTPWDshowinfo_info(event=''):
    status_label.configure(text="输入设备密码:" + UUTPWD_Input.get())
    showinfo("输入设备密码:" + UUTPWD_Input.get())
    logging.info("输入设备密码:" + UUTPWD_Input.get())
    UUTPWD.append(UUTPWD_Input.get())

def UUTPWDdelete_info(event=''):
    status_label.configure(text="清除设备密码:" + UUTPWD_Input.get())

def COUNTTshowinfo_info(event=''):
    status_label.configure(text="循环次数:" + COUNTT_Input.get())
    showinfo("循环次数:" + COUNTT_Input.get())
    logging.info("循环次数:" + COUNTT_Input.get())
    Check_Number(COUNTT_Input.get(), COUNTT_Input)
    COUNTT.append(COUNTT_Input.get())

def COUNTTdelete_info(event=''):
    status_label.configure(text="清除运行时间：" + COUNTT_Input.get())

def INTERVALTshowinfo_info(event=''):
    INTERVAL.append("10")
    status_label.configure(text="输入间隔时间:" + INTERVALT_Input.get())
    showinfo("输入间隔时间:" + INTERVALT_Input.get())
    logging.info("输入间隔时间:" + INTERVALT_Input.get())
    INTERVAL.append(INTERVALT_Input.get())

def INTERVALTdelete_info(event=''):
    status_label.configure(text="清除运行时间：" + INTERVALT_Input.get())

def check_UUTstatus():
    """
    检查设备是否在线
    超过5次一直循环等待设备上线
    :return:
    """
    try:
        count = 0
        while True:
            count += 1
            if count <= 5:
                showinfo("开始检查设备是否在线")
                logging.info("开始检查设备是否在线")
                logging.info("=" * 50)
                logging.info("=" * 25 + "正在检查" + "=" * 25)
                with os.popen("ping -n 3 {}".format(UUT_IP), "r") as p:
                    ping = p.read()
                logging.info("ping result:", ping)
                p.close()
                if 'TTL' in ping:
                    # ping_result = str(re.findall("\d+%", ping)[0]).strip("%")
                    showinfo("=" * 25 + "检查完毕" + "=" * 25)
                    logging.info("=" * 25 + "检查完毕" + "=" * 25)
                    showinfo("=" * 25 + "设备在线" + "=" * 25)
                    logging.info("=" * 25 + "设备在线" + "=" * 25)
                    # logging.info("丢包率：", ping_result + "%")
                    time.sleep(1)
                    break
                else:
                    showinfo("=" * 25 + "设备未上线" + "=" * 25)
                    logging.info("=" * 25 + "设备未上线" + "=" * 25)
                    continue
            else:
                status_label.configure(text="请检查设备是否开电", bg="blue")
                showinfo("=" * 25 + "等待设备上线中" + "=" * 25)
                while True:
                    with os.popen("ping -n 3 {}".format(UUT_IP), "r") as p:
                        ping = p.read()
                    p.close()
                    if 'TTL' in ping:
                        # ping_result = str(re.findall("\d+%", ping)[0]).strip("%")
                        showinfo("=" * 25 + "检查完毕" + "=" * 25)
                        logging.info("=" * 25 + "检查完毕" + "=" * 25)
                        showinfo("=" * 25 + "设备在线" + "=" * 25)
                        logging.info("=" * 25 + "设备在线" + "=" * 25)
                        # logging.info("丢包率：", ping_result + "%")
                        time.sleep(1)
                        status_label.configure(text="程序进行中", bg="yellow")
                        break
                    else:
                        time.sleep(5)
                        continue
                break
    except Exception as e:
        showinfo(e)
        logging.info(e)

def check_UUTstatusF():
    """
    检查设备是否断电
    :return:
    """
    try:
        showinfo("开始检查设备是否关机")
        logging.info("开始检查设备是否关机")
        logging.info("=" * 30)
        logging.info("=" * 25 + "正在检查" + "=" * 25)
        while True:
            with os.popen("ping -n 3 {}".format(UUT_IP), "r") as p:
                ping = p.read()
            logging.info("ping result:", ping)
            p.close()
            if 'TTL' in ping:
                continue
            else:
                showinfo("=" * 25 + "设备已关机" + "=" * 25)
                logging.info("=" * 25 + "设备已关机" + "=" * 25)
                break
    except Exception as e:
        showinfo(e)
        logging.info(e)

frm1 = Frame(root)
frm2 = Frame(root)
frm3 = Frame(root)
start = tk.StringVar()
end = tk.StringVar()
frm1.config(height=385, width=630)
frm1.place(x=210, y=0)
frm2.config(height=385, width=200)
frm2.place(x=5, y=0)
frm3.config(height=60, width=840, relief=SUNKEN)
frm3.place(x=0, y=390)

# frm3下的Label
status_label = Label(frm3, text='输入：', anchor=W, width=200, height=3)
status_label.pack(side=LEFT)

# frm2下的Button
Label_list = ["设备IP", "设备密码","reboot次数","间隔时间"]
Y = 20
for i in Label_list:
    Label(frm2, text='{}'.format(i), font=('华文新魏', 10)).place(x=0, y=Y, width=80)
    Y += 30
IP_M = tk.StringVar(value='192.168.8.1')
IP_Input = Entry(frm2,textvariable=IP_M)
IP_Input.grid(row=1, column=1, sticky="W")
IP_Input.place(x=85, y=20)
IP_Input.bind("<Return>", UPshowinfo_info)
IP_Input.bind("<Delete>", UPdelete_info)

UUTPWD_M = tk.StringVar(value='123456')
UUTPWD_Input = Entry(frm2,textvariable=UUTPWD_M)
UUTPWD_Input.grid(row=1, column=1, sticky="W")
UUTPWD_Input.place(x=85, y=50)
UUTPWD_Input.bind("<Return>", UUTPWDshowinfo_info)
UUTPWD_Input.bind("<Delete>", UUTPWDdelete_info())

COUNTT_M = tk.StringVar(value='200')
COUNTT_Input = Entry(frm2,textvariable=COUNTT_M)
COUNTT_Input.grid(row=1, column=1, sticky="W")
COUNTT_Input.place(x=85, y=80)
COUNTT_Input.bind("<Return>", COUNTTshowinfo_info)
COUNTT_Input.bind("<Delete>", COUNTTdelete_info)

INTERVALT_M = tk.StringVar(value='10')
INTERVALT_Input = Entry(frm2,textvariable=INTERVALT_M)
INTERVALT_Input.grid(row=1, column=1, sticky="W")
INTERVALT_Input.place(x=85, y=110)
INTERVALT_Input.bind("<Return>", INTERVALTshowinfo_info)
INTERVALT_Input.bind("<Delete>", INTERVALTdelete_info)

IP_label = Label(frm2, text="开始时间:", font=('华文新魏', 10))
IP_label.grid(row=1, column=1, sticky="E")
IP_label.place(x=5, y=260)
start_time = Label(master=frm2, textvariable=start, height=3)
start_time.grid(row=1, column=1, sticky="E")
start_time.place(width=100, height=30, x=70, y=255)

IP_label = Label(frm2, text="结束时间:", font=('华文新魏', 10))
IP_label.grid(row=1, column=1, sticky="E")
IP_label.place(x=5, y=305)
start_time = Label(master=frm2, textvariable=end, height=3)
start_time.grid(row=1, column=1, sticky="E")
start_time.place(width=100, height=30, x=70, y=300)

Start = Button(frm2, text="开始测试", command=lambda: MyThread(start_RBtest))
Start.grid(row=1, column=1, sticky="E")
Start.place(width=80, height=30, x=5, y=350)





def ssh_reboot(ip, pwd):
    global SSH_Result
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip,
                    username="root",
                    port="22",
                    password=pwd,
                    allow_agent=False,
                    look_for_keys=False)
        showinfo("ssh设备成功")
        time.sleep(0.5)
        stdin, stdout, stderr = ssh.exec_command("reboot")
        err_list = stderr.readlines()
        if len(err_list) > 0:
            showinfo('ssh 执行命令 [%s] 错误: %s' % ("reboot", err_list[0]))
            SSH_Result = False
        else:
            buff = stdout.read().decode('utf-8')
            showinfo(buff)
            logging.info(buff)
            SSH_Result = True
        ssh.close()
    except Exception as e:
        SSH_Result = False
        showinfo("ssh 设备异常:{}".format(e))
        logging.info("ssh 设备异常：{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")

def Restore_button():
    IP_Input.configure(state=NORMAL)
    UUTPWD_Input.configure(state=NORMAL)
    COUNTT_Input.configure(state=NORMAL)
    INTERVALT_Input.configure(state=NORMAL)
    Start.configure(state=NORMAL)

def disable_button():
    IP_Input.configure(state=DISABLED)
    UUTPWD_Input.configure(state=DISABLED)
    COUNTT_Input.configure(state=DISABLED)
    INTERVALT_Input.configure(state=DISABLED)
    Start.configure(state=DISABLED)

def start_RBtest():
    try:
        logging.getLogger().setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        logging.basicConfig(filename=os.path.join(os.getcwd(), "reboot" + current_time + '.log.txt'),
                            level=logging.DEBUG)
        UPshowinfo_info()
        UUTPWDshowinfo_info()
        COUNTTshowinfo_info()
        INTERVALTshowinfo_info()
        disable_button()
        global UUT_IP
        global PC_LANIP
        global PC_WLANIP
        global WIFI_Name
        global WIFI_PASSWD
        global RUNTIME
        global INTERVALT
        global COUNT
        status_label.configure(text="程序进行中", bg="yellow")
        UUT_IP = UUTIP.pop()
        UUT_PWD = UUTPWD.pop()
        COUNT = int(COUNTT.pop())
        INTERVALT = int(INTERVAL.pop())
        start.set(value=time.strftime('%m%d %H:%M:%S'))
        showinfo("UUT IP : {}".format(UUT_IP))  # 显示在text中的内容
        logging.info("UUT IP : %s", UUT_IP)  # 显示在log中的内容
        showinfo("UUT PASSWD :{}".format(UUT_PWD))
        logging.info("UUT PASSWD :{}".format(UUT_PWD))
        showinfo("运行次数：{}".format(COUNT))
        logging.info("运行次数：{}".format(COUNT))
        showinfo("每次循环间隔时间：{}".format(INTERVALT))
        logging.info("每次循环间隔时间：{}".format(INTERVALT))
        for i in range(COUNT):
            status_label.configure(text="程序进行中    循环次数：{}".format(i + 1), bg="yellow")
            showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
            logging.info("=" * 30 + "{}".format(i + 1) + "=" * 30)
            check_UUTstatus()
            ssh_reboot(UUT_IP, UUT_PWD)
            if SSH_Result == True:
                showinfo("reboot命令发送成功")
                check_UUTstatusF()
                time.sleep(60)
                check_UUTstatus()
                showinfo("设备reboot成功")
                logging.info("设备reboot成功")
                if i + 1 < COUNT:
                    showinfo("=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 20)
                    logging.info(
                        "=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 30)
                    time.sleep(INTERVALT)
                else:
                    end.set(value=time.strftime('%m%d %H:%M:%S'))
                    showinfo("程序运行完毕！！！")
                    logging.info("程序运行完毕！！！")
                    status_label.configure(text="程序运行完毕", bg="green")
                    break
            else:
                showinfo("reboot命令发送失败")
                status_label.configure(text="程序运行失败", bg="red")
                break
        Restore_button()
    except Exception as e:
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")
        showinfo("测试失败：{}".format(e))
        logging.info("测试失败: {}".format(e))





text = Text(frm1,bd=3,
            height=29,
            width=87,
            padx=1,
            pady=1,
            state='normal',
            cursor='arrow',
            font=('黑体', 10),
            wrap='char',
            )
sl1 = Scrollbar(frm1)
text.configure(yscrollcommand=sl1.set)
sl1['command'] = text.yview
sl1.grid(row=0, column=1, sticky=S + W + E + N)
text.grid(row=0, column=0, sticky=S + W + E + N)

root.mainloop()