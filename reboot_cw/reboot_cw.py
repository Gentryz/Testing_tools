import logging
import threading
from tkinter import *
import tkinter as tk
import pywifi, time
from pywifi import const
import subprocess
import tempfile
import os
import paramiko


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()

    def run(self):
        self.func(*self.args)

root = Tk()
root.geometry('840x440+200+200')
root.resizable(False,False)
root.title('控制继电器重启且连接wifi跑流测试')

UUTIP = []
UUTPWD =[]
PCIP = []
PCWLANIP = []
WIFINAME = []
WIFIPWD = []
RUNT = []
COUNTT = []
INTERVAL = []
WEB = []
FIRMWARE = []
fail_ind = []




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

def UPshowinfo_info(event=''):
    status_label.configure(text="输入板子IP:" + IP_Input.get())
    showinfo("输入板子IP:" + IP_Input.get())
    logging.info("输入板子IP:" + IP_Input.get())
    Check_Input(IP_Input.get(), IP_Input)
    UUTIP.append(IP_Input.get())

def UPdelete_info(event=''):
    status_label.configure(text="清楚板子IP：" + IP_Input.get())

def PCLshowinfo_info(event=''):
    status_label.configure(text="输入PC LAN口IP:" + PCIP_Input.get())
    showinfo("输入板子IP:" + PCIP_Input.get())
    logging.info("输入板子IP:" + PCIP_Input.get())
    Check_Input(PCIP_Input.get(), PCIP_Input)
    PCIP.append(PCIP_Input.get())

def PCLdelete_info(event=''):
    status_label.configure(text="清除PC LAN口IP：" + PCIP_Input.get())

def PCWIPshowinfo_info(event=''):
    status_label.configure(text="输入PC WLAN IP:" + PCWIP_Input.get())
    showinfo("输入板子IP:" + PCWIP_Input.get())
    logging.info("输入板子IP:" + PCWIP_Input.get())
    Check_Input(PCWIP_Input.get(), PCWIP_Input)
    PCWLANIP.append(PCWIP_Input.get())

def PCWIPdelete_info(event=''):
    status_label.configure(text="清除PC WLAN IP：" + PCWIP_Input.get())

def WIFINAMEshowinfo_info(event=''):
    status_label.configure(text="输入wifi名称:" + WIFIName_Input.get())
    showinfo("输入wifi名称:" + WIFIName_Input.get())
    logging.info("输入wifi名称:" + WIFIName_Input.get())
    WIFINAME.append(WIFIName_Input.get())

def WIFINAMEdelete_info(event=''):
    status_label.configure(text="清除Pwifi名称：" + WIFIName_Input.get())

def WIFIPSWDshowinfo_info(event=''):
    status_label.configure(text="输入wifi密码:" + WIFIPWD_Input.get())
    showinfo("输入wifi密码:" + WIFIPWD_Input.get())
    logging.info("输入wifi密码:" + WIFIPWD_Input.get())
    WIFIPWD.append(WIFIPWD_Input.get())

def WIFIPSWDdelete_info(event=''):
    status_label.configure(text="清除Pwifi名称：" + WIFIPWD_Input.get())

def RUNTshowinfo_info(event=''):
    status_label.configure(text="输入运行时间:" + RUNT_Input.get() + "S")
    showinfo("输入运行时间:" + RUNT_Input.get() + "S")
    logging.info("输入运行时间:" + RUNT_Input.get() + "S")
    Check_Number(RUNT_Input.get(), RUNT_Input)
    RUNT.append(RUNT_Input.get())

def RUNTdelete_info(event=''):
    status_label.configure(text="清除运行时间：" + RUNT_Input.get() + "S")

def COUNTTshowinfo_info(event=''):
    status_label.configure(text="循环次数:" + COUNTT_Input.get())
    showinfo("循环次数:" + COUNTT_Input.get())
    logging.info("循环次数:" + COUNTT_Input.get())
    Check_Number(COUNTT_Input.get(), COUNTT_Input)
    COUNTT.append(COUNTT_Input.get())

def COUNTTdelete_info(event=''):
    status_label.configure(text="清除运行时间：" + COUNTT_Input.get())

def INTERVALTshowinfo_info(event=''):
    status_label.configure(text="输入间隔时间:" + INTERVALT_Input.get())
    showinfo("输入间隔时间:" + INTERVALT_Input.get())
    logging.info("输入间隔时间:" + INTERVALT_Input.get())
    INTERVAL.append(INTERVALT_Input.get())

def INTERVALTdelete_info(event=''):
    status_label.configure(text="清除运行时间：" + INTERVALT_Input.get())

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
                        break
                    else:
                        time.sleep(5)
                        continue
                break
    except Exception as e:
        showinfo("检查设备失败:{}".format(e))
        logging.info("检查设备失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")
def check_UUTstatusF():
    """
    检查设备是否断电
    :return:
    """
    try:
        showinfo("开始检查设备是否断电")
        logging.info("开始检查设备是否断电")
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
                showinfo("=" * 25 + "设备已断电" + "=" * 25)
                logging.info("=" * 25 + "设备已断电" + "=" * 25)
                break
    except Exception as e:
        showinfo("检查设备失败:".format(e))
        logging.info("检查设备失败:".format(e))
        status_label.configure(text="程序运行失败", bg="red")

def Start_iperfServer():
    """
    开启iperf Server
    :return:
    """
    global iperfS_status
    try:
        with os.popen("taskkill /im iperf3.exe /f".format(UUT_IP), "r") as s:
            kill = s.read()
            logging.info(kill)
            s.close()
        with os.popen("tasklist|findstr iperf3.exe".format(UUT_IP), "r") as p:
            status = p.read()
            logging.info("查看进程：" + status)
            time.sleep(0.5)
            p.close()
            root.update()
        if "iperf3.exe" in status:
            logging.info("iperf server 已开启")
            iperfS_status = "True"
            time.sleep(1)
        else:
            showinfo("=" * 25 + "开启iperf Server" + "=" * 25)
            logging.info("=" * 25 + "开启iperf Server" + "=" * 25)
            showinfo("iperf3.exe -B {} -s &".format(PC_LANIP))
            out_temp = tempfile.SpooledTemporaryFile()
            fileno = out_temp.fileno()
            time.sleep(1)
            obj = subprocess.Popen("iperf3.exe -B {} -s &".format(PC_LANIP), stdout=fileno, stderr=fileno,
                                   shell=True)
            time.sleep(5)
            out_temp.seek(0)
            iperf = out_temp.readlines()
            with os.popen("tasklist|findstr iperf3.exe".format(UUT_IP), "r") as p:
                status = p.read()
                logging.info("查看进程：" + status)
                time.sleep(0.5)
                p.close()
                root.update()
            if "iperf3.exe" in status:
                showinfo("iperf server 已开启")
                logging.info("iperf server 已开启")
                iperfS_status = "True"
                time.sleep(1)
            else:
                showinfo("iperf server 开启失败")
                logging.info("iperf server 开启失败")
                iperfS_status = "False"

    except Exception as e:
        showinfo("iperf 运行失败{}".format(e))
        logging.info("iperf 运行失败{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")

def Start_iperfClient():
    global iperfC_statusT
    global iperfC_statusR
    for i in range(3):
        showinfo("=" * 25 + "开启TX跑流{}S".format(RUNTIME) + "=" * 25)
        logging.info("=" * 25)
        logging.info("开启TX跑流{}S".format(RUNTIME))
        with os.popen("iperf3.exe -B {} -c {} -i 1  -t {} -R".format(PC_WLANIP, PC_LANIP, RUNTIME), "r") as p:
            iperf = p.read()
            logging.info(str(iperf))
            time.sleep(1)
            if "iperf Done" in iperf:
                p.close()
                logging.info("=" * 25 + "iperf 运行成功" + "=" * 25)
                showinfo("=" * 25 + "iperf 运行成功" + "=" * 25)
                TX_results = iperf.split("\n").pop(-5)
                TX_result = TX_results.split()[6]
                TX_result_units = TX_results.split()[7]
                showinfo("运行成功，下载流量:{}".format(TX_result + TX_result_units))
                logging.info("运行成功，下载流量：{}".format(TX_result + TX_result_units))
                iperfC_statusT = "True"
                break
            else:
                logging.info("=" * 25 + "iperf 运行失败" + "=" * 25)
                showinfo("=" * 25 + "iperf 运行失败" + "=" * 25)
                showinfo(str(iperf))
                logging.info(str(iperf))
                p.close()
                iperfC_statusT = "False"
                continue
    for i in range(3):
        showinfo("=" * 25 + "开启RX跑流{}S".format(RUNTIME) + "=" * 25)
        logging.info("=" * 25)
        logging.info("开启RX跑流{}S".format(RUNTIME))
        time.sleep(2)
        with os.popen("iperf3.exe -B {} -c {} -i 1  -t {} ".format(PC_WLANIP, PC_LANIP, RUNTIME), "r") as p:
            iperf = p.read()
            logging.info(str(iperf))
            time.sleep(1)
            if "iperf Done" in iperf:
                p.close()
                logging.info("=" * 25 + "iperf 运行成功" + "=" * 25)
                showinfo("=" * 25 + "iperf 运行成功" + "=" * 25)
                TX_results = iperf.split("\n").pop(-5)
                TX_result = TX_results.split()[6]
                TX_result_units = TX_results.split()[7]
                showinfo("运行成功，上传流量:{}".format(TX_result + TX_result_units))
                logging.info("运行成功，上传流量：{}".format(TX_result + TX_result_units))
                iperfC_statusR = "True"
                break
            else:
                logging.info("=" * 25 + "iperf 运行失败" + "=" * 25)
                showinfo("=" * 25 + "iperf 运行失败" + "=" * 25)
                showinfo(str(iperf))
                logging.info(str(iperf))
                p.close()
                iperfC_statusR = "False"
                continue

def wifi_connect_status():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    if iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        showinfo("wifi connected!")
        logging.info("wifi connected!")
        time.sleep(1)
        return 1
    else:
        showinfo("wifi not connected!")
        logging.info("wifi not connected!")
        return 0

# 扫描wifi：
def scan_wifi():
    showinfo("=" * 30 + "开始扫描WIFI" + "=" * 30)
    logging.info("=" * 30 + "开始扫描WIFI" + "=" * 30)
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(1)
    basewifi = iface.scan_results()
    for i in basewifi:
        logging.info("wifi scan result:{}".format(i.ssid))
        logging.info("wifi device MAC address:{}".format(i.bssid))
    time.sleep(1)
    return basewifi

# 连接指定的wifi：
def connect_wifi(SSID, PASSWD):
    global connect_status
    try:
        for i in range(5):
            time.sleep(30)
            wifi = pywifi.PyWiFi()
            ifaces = wifi.interfaces()[0]
            showinfo("无线网卡：{}".format(ifaces.name()))  # 输出无线网卡名称
            logging.info("无线网卡：{}".format(ifaces.name()))
            ifaces.disconnect()
            time.sleep(3)
            profile = pywifi.Profile()  # 配置文件
            profile.ssid = SSID  # wifi名称
            profile.auth = const.AUTH_ALG_OPEN  # 需要密码
            profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
            profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
            profile.key = PASSWD  # wifi密码
            ifaces.remove_all_network_profiles()  # 删除其它配置文件
            tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
            ifaces.connect(tmp_profile)
            time.sleep(5)
            isok = True
            if ifaces.status() == const.IFACE_CONNECTED:
                showinfo("connect successfully!")
                logging.info("connect successfully!")
                connect_status = "True"
                break
            else:
                showinfo("connect failed!")
                logging.info("connect failed!")
                showinfo("connect again")
                logging.info("connect again")
                connect_status = "False"
                continue
            time.sleep(1)
            return isok
    except Exception as e:
        showinfo("连接WIFI失败:{}".format(e))
        logging.info("连接WIFI失败:{}".format(e))


def power_on():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="192.168.1.1",
                username="root",
                port="22",
                password="goodlife1")
    send_command = ssh.invoke_shell()
    send_command.send(r"stty -F /dev/ttyUSB0  speed 9600  cs8 -parenb -cstopb" + '\n')
    send_command.send(r"echo -e '\xA0\x01\x01\xA2' > /dev/ttyUSB0" + '\n')
    time.sleep(5)
    ssh.close()

def power_off():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="192.168.1.1",
                username="root", port="22",
                password="goodlife1")
    send_command = ssh.invoke_shell()
    send_command.send(r"stty -F /dev/ttyUSB0  speed 9600  cs8 -parenb -cstopb" + '\n')
    time.sleep(0.5)
    send_command.send(r"echo -e '\xA0\x01\x00\xA1' > /dev/ttyUSB0" + '\n')
    time.sleep(0.5)
    send_command.send(r"stty -F /dev/ttyUSB0  speed 9600  cs8 -parenb -cstopb" + '\n')
    time.sleep(0.5)
    send_command.send(r"echo -e '\xA0\x01\x00\xA1' > /dev/ttyUSB0" + '\n')
    time.sleep(3)
    ssh.close()



# root.attributes('-disabled', True)
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
Label_list = ["设备IP", "PC LAN IP", "PC WLAN IP", "WIFI名字", "WIFI密码", "运行时间", "运行次数", "间隔时间"]

Y = 20
for i in Label_list:
    Label(frm2, text='{}'.format(i), font=('华文新魏', 10)).place(x=0, y=Y, width=80)
    Y += 30
IP_M = tk.StringVar(value='192.168.8.1')
IP_Input = Entry(frm2, textvariable=IP_M)
IP_Input.grid(row=1, column=1, sticky="W")
IP_Input.place(x=80, y=20)
IP_Input.bind("<Return>", UPshowinfo_info)
IP_Input.bind("<Delete>", UPdelete_info)

PCIP_M = tk.StringVar(value='192.168.8.246')
PCIP_Input = Entry(frm2,textvariable=PCIP_M)
PCIP_Input.grid(row=1, column=1, sticky="W")
PCIP_Input.place(x=80, y=50)
PCIP_Input.bind("<Return>", PCLshowinfo_info)
PCIP_Input.bind("<Delete>", PCLdelete_info)

PCWIP_M = tk.StringVar(value='192.168.8.157')
PCWIP_Input = Entry(frm2,textvariable=PCWIP_M)
PCWIP_Input.grid(row=1, column=1, sticky="W")
PCWIP_Input.place(x=80, y=80)
PCWIP_Input.bind("<Return>", PCWIPshowinfo_info)
PCWIP_Input.bind("<Delete>", PCWIPdelete_info)

WIFIName_M = tk.StringVar(value='GL-TEST-PY')
WIFIName_Input = Entry(frm2,textvariable=WIFIName_M)
WIFIName_Input.grid(row=1, column=1, sticky="W")
WIFIName_Input.place(x=80, y=110)
WIFIName_Input.bind("<Return>", WIFINAMEshowinfo_info)
WIFIName_Input.bind("<Delete>", WIFINAMEdelete_info)

WIFIPWD_M = tk.StringVar(value='goodlife')
WIFIPWD_Input = Entry(frm2,textvariable=WIFIPWD_M)
WIFIPWD_Input.grid(row=1, column=1, sticky="W")
WIFIPWD_Input.place(x=80, y=140)
WIFIPWD_Input.bind("<Return>", WIFIPSWDshowinfo_info)
WIFIPWD_Input.bind("<Delete>", WIFIPSWDdelete_info)

RUNT_M = tk.StringVar(value='5')
RUNT_Input = Entry(frm2,textvariable=RUNT_M)
RUNT_Input.grid(row=1, column=1, sticky="W")
RUNT_Input.place(x=80, y=170)
RUNT_Input.bind("<Return>", RUNTshowinfo_info)
RUNT_Input.bind("<Delete>", RUNTdelete_info)

COUNTT_M = tk.StringVar(value='200')
COUNTT_Input = Entry(frm2,textvariable=COUNTT_M)
COUNTT_Input.grid(row=1, column=1, sticky="W")
COUNTT_Input.place(x=80, y=200)
COUNTT_Input.bind("<Return>", COUNTTshowinfo_info)
COUNTT_Input.bind("<Delete>", COUNTTdelete_info)

INTERVALT_M =  tk.StringVar(value='5')
INTERVALT_Input = Entry(frm2,textvariable=INTERVALT_M)
INTERVALT_Input.grid(row=1, column=1, sticky="W")
INTERVALT_Input.place(x=80, y=230)
INTERVALT_Input.bind("<Return>", INTERVALTshowinfo_info)
INTERVALT_Input.bind("<Delete>", INTERVALTdelete_info)

# 开始时间：
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

text = Text(frm1, bd=3,  # 边框的大小
            height=29,  # 高度
            width=87,  # 宽度
            padx=1,  # 内间距，字体与边框的X距离
            pady=1,  # 内间距，字体与边框的Y距离
            state='normal',  # 设置状态 normal、active、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('黑体', 10),  # 字体
            wrap='char',  # 字数够width后是否换行 char, none,  word
            )
sl1 = Scrollbar(frm1)
text.configure(yscrollcommand=sl1.set)
sl1['command'] = text.yview
sl1.grid(row=0, column=1, sticky=S + W + E + N)
text.grid(row=0, column=0, sticky=S + W + E + N)

Start = Button(frm2, text="开始测试", command=lambda: MyThread(StartTest))
Start.grid(row=1, column=1, sticky="E")
Start.place(width=100, height=30, x=10, y=350)
def StartTest():
    try:
        logging.getLogger().setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        logging.basicConfig(filename=os.path.join(os.getcwd(), "控制继电器上下电wifi跑流" + current_time + '.log.txt'),
                            level=logging.DEBUG)
        UPshowinfo_info()
        PCLshowinfo_info()
        PCWIPshowinfo_info()
        WIFINAMEshowinfo_info()
        WIFIPSWDshowinfo_info()
        RUNTshowinfo_info()
        COUNTTshowinfo_info()
        INTERVALTshowinfo_info()
        IP_Input.configure(state=DISABLED)
        PCIP_Input.configure(state=DISABLED)
        PCWIP_Input.configure(state=DISABLED)
        WIFIName_Input.configure(state=DISABLED)
        WIFIPWD_Input.configure(state=DISABLED)
        RUNT_Input.configure(state=DISABLED)
        COUNTT_Input.configure(state=DISABLED)
        INTERVALT_Input.configure(state=DISABLED)
        Start.configure(state=DISABLED)
        global UUT_IP
        global PC_LANIP
        global PC_WLANIP
        global WIFI_Name
        global WIFI_PASSWD
        global RUNTIME
        global INTERVALT
        status_label.configure(text="程序进行中", bg="yellow")
        UUT_IP = UUTIP.pop()
        PC_LANIP = PCIP.pop()
        PC_WLANIP = PCWLANIP.pop()
        WIFI_Name = WIFINAME.pop()
        WIFI_PASSWD = WIFIPWD.pop()
        RUNTIME = RUNT.pop()
        COUNT = int(COUNTT.pop())
        INTERVALT = int(INTERVAL.pop())
        start.set(value=time.strftime('%m%d %H:%M:%S'))
        for i in range(COUNT):
            status_label.configure(text="程序进行中    循环次数：{}".format(i + 1), bg="yellow")
            showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
            logging.info("=" * 30 + "{}".format(i + 1) + "=" * 30)
            showinfo("UUT IP : {}".format(UUT_IP))  # 显示在text中的内容
            showinfo("PC　LAN IP : {}".format(PC_LANIP))
            showinfo("PC　WLAN IP ：{}".format(PC_WLANIP))
            showinfo(" connect wifi name：{}".format(WIFI_Name))
            showinfo(" connect wifi password：{}".format(WIFI_PASSWD))
            showinfo(" sent iperf run time: {}".format(RUNTIME))
            logging.info("UUT IP : %s", UUT_IP)  # 显示在log中的内容
            logging.info("PC　LAN IP : %s", PC_LANIP)
            logging.info("PC　WLAN IP ：%s", PC_WLANIP)
            logging.info(" connect wifi name：%s", PCWLANIP)
            logging.info(" connect wifi password：%s", WIFI_Name)
            logging.info(" sent iperf run time: {}".format(RUNTIME))
            showinfo("=" * 25 + "开始上电" + "=" * 25)
            power_on()
            showinfo("=" * 25 + "继电器已上电" + "=" * 25)
            time.sleep(30)
            check_UUTstatus()
            time.sleep(0.5)
            wifi_connect_status()
            scan_wifi()
            connect_wifi(WIFI_Name, WIFI_PASSWD)
            if connect_status == "True":
                Start_iperfServer()
                if iperfS_status == "True":
                    Start_iperfClient()
                    if iperfC_statusT == "True" or iperfC_statusR == "True":
                        if i + 1 < COUNT:
                            showinfo("=" * 20 + "准备继电器断电" + "=" * 20)
                            logging.info("=" * 20 + "准备继电器断电" + "=" * 20)
                            power_off()
                            check_UUTstatusF()
                            showinfo("=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                  INTERVALT) + "=" * 20)
                            logging.info("=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                      INTERVALT) + "=" * 30)
                            time.sleep(INTERVALT)
                        else:
                            power_off()
                            showinfo("程序运行完毕！！！")
                            logging.info("程序运行完毕！！！")
                            status_label.configure(text="程序运行完毕", bg="green")
                            break
                    else:
                        showinfo("iperf client运行失败，程序暂停")
                        status_label.configure(text="程序运行失败", bg="red")
                        break
                else:
                    showinfo("iperf server开启失败，程序暂停")
                    status_label.configure(text="程序运行失败", bg="red")
                    break
            else:
                showinfo("WIFI连接失败，程序暂停")
                status_label.configure(text="程序运行失败", bg="red")
                break
        end.set(value=time.strftime('%m%d %H:%M:%S'))
    except Exception as e:
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")
        showinfo("测试失败：{}".format(e))
        logging.info("测试失败: {}".format(e))


root.mainloop()