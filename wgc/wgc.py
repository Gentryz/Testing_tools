import logging
import threading
from tkinter import *
import tkinter as tk
import time
from selenium.common.exceptions import SessionNotCreatedException
import re
import os
import requests
import zipfile
import itertools
import paramiko
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from pywinauto import Desktop
from pywinauto.keyboard import send_keys


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
root.title('WireGuard 客户端反复断开连接测试')

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

def WEBshowinfo_info(event=''):
    status_label.configure(text="输入网页地址:" + WEB_Input.get())
    showinfo("输入网页地址:" + WEB_Input.get())
    logging.info("输入网页地址:" + WEB_Input.get())
    Check_Input(WEB_Input.get(), WEB_Input)
    WEB.append(WEB_Input.get())

def WEBdelete_info(event=''):
    status_label.configure(text="清楚板子IP：" + WEB_Input.get())

def UUTPWDshowinfo_info(event=''):
    status_label.configure(text="输入设备密码:" + UUTPWD_Input.get())
    showinfo("输入设备密码:" + UUTPWD_Input.get())
    logging.info("输入设备密码:" + UUTPWD_Input.get())
    UUTPWD.append(UUTPWD_Input.get())

def UUTPWDdelete_info(event=''):
    status_label.configure(text="清除设备密码:" + UUTPWD_Input.get())

def Configshowinfo_info(event=''):
    status_label.configure(text="输入配置名称：" + Config_Input.get())
    showinfo("输入配置名称：" + Config_Input.get())
    logging.info("输入配置名称：" + Config_Input.get())
    FIRMWARE.append(Config_Input.get())

def Configdelete_info(event=''):
    status_label.configure(text="清除固件位置：" + Config_Input.get())

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

def check_UUTstatus(ip):
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
                with os.popen("ping -n 3 {}".format(ip), "r") as p:
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
                logging.info("=" * 25 + "等待设备上线中" + "=" * 25)
                while True:
                    with os.popen("ping -n 3 {}".format(ip), "r") as p:
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
        showinfo("升级失败:{}".format(e))
        logging.info("升级失败:{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")



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
frm2.focus_set()
# frm3下的Label
status_label = Label(frm3, text='输入：', anchor=W, width=200, height=3)
status_label.pack(side=LEFT)

# frm2下的Button
Label_list = ["网页地址", "登入密码", "WireGuard配置文件", "循环次数", "间隔时间"]
Y = 20
for i in Label_list:
    Label(frm2, text='{}'.format(i), font=('华文新魏', 10)).place(x=0, y=Y, width=80)
    Y += 30

WEB_M = tk.StringVar(value='192.168.8.1')
WEB_Input = Entry(frm2, textvariable=WEB_M)
WEB_Input.grid(row=1, column=1, sticky="W")
WEB_Input.place(x=85, y=20)
WEB_Input.bind("<Return>", WEBshowinfo_info)
WEB_Input.bind("<Delete>", WEBdelete_info)

UUTPWD_M = tk.StringVar(value='123456')
UUTPWD_Input = Entry(frm2, textvariable=UUTPWD_M)
UUTPWD_Input.grid(row=1, column=1, sticky="W")
UUTPWD_Input.place(x=85, y=50)
UUTPWD_Input.bind("<Return>", UUTPWDshowinfo_info)
UUTPWD_Input.bind("<Delete>", UUTPWDdelete_info())

Config_M = tk.StringVar(value='vpn.conf')
Config_Input = Entry(frm2, textvariable=Config_M)
Config_Input.grid(row=1, column=1, sticky="W")
Config_Input.place(x=85, y=80)
Config_Input.bind("<Return>", Configshowinfo_info)
Config_Input.bind("<Delete>", Configdelete_info())

COUNTT_M = tk.StringVar(value='200')
COUNTT_Input = Entry(frm2, textvariable=COUNTT_M)
COUNTT_Input.grid(row=1, column=1, sticky="W")
COUNTT_Input.place(x=85, y=110)
COUNTT_Input.bind("<Return>", COUNTTshowinfo_info)
COUNTT_Input.bind("<Delete>", COUNTTdelete_info)

INTERVALT_M = tk.StringVar(value='5')
INTERVALT_Input = Entry(frm2, textvariable=INTERVALT_M)
INTERVALT_Input.grid(row=1, column=1, sticky="W")
INTERVALT_Input.place(x=85, y=140)
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

def open_web(ip):
    global browser
    global open_status
    open_status = "True"
    try:
        showinfo("=" * 25 + "打开网页" + "=" * 25)
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging', 'enable-automation'])
        browser = getChromeDriver(options)
        url = r'http://' + ip + '/'
        browser.get(url)
        time.sleep(2)
    except:
        open_status = "flase"

def getChromeDriver(options=None):
    global browser
    try:
        path = os.path.abspath(os.curdir)
        driver_path = path + '\chromedriver.exe'
        logging.info("本机驱动地址{}".format(driver_path))
        browser = webdriver.Chrome(driver_path)
        return browser
    except SessionNotCreatedException as e:
        driver_version = re.search(
            "Chrome version ([\d.]+)", str(e)).group(1)
        chrome_version = re.search(
            "Current browser version is ([\d.]+) with", str(e)).group(1)
        logging.info(f"驱动版本：{driver_version}，谷歌游览器版本：{chrome_version}，不兼容\n开始更新驱动...")
        res = requests.get(
            "https://registry.npmmirror.com/-/binary/chromedriver/")
        versions = [obj["name"][:-1] for obj in res.json() if re.match("\d+",
                                                                       obj["name"]) and obj["name"].count(".") == 3]
        versions = {key: max(versions_split, key=lambda x: int(x[x.rfind(".") + 1:]))
                    for key, versions_split in itertools.groupby(versions, key=lambda x: x[:x.rfind(".")])}
        dest_version = versions[chrome_version[:chrome_version.rfind(".")]]
        logging.info("驱动将更新到:{}".format(dest_version))
        file = f"chromedriver_{dest_version}_win32.zip"
        if not os.path.exists(file):
            url = f"https://registry.npmmirror.com/-/binary/chromedriver/{dest_version}/chromedriver_win32.zip"
            res = requests.get(url)
            with open(file, 'wb') as f:
                f.write(res.content)
        else:
            showinfo("文件已经下载到当前目录，下面直接使用缓存解压覆盖...")
        with zipfile.ZipFile(file) as zf:
            zf.extract("chromedriver.exe", ".")
        browser = webdriver.Chrome(options=options)
        return browser

def setpwd(pwd):
    global setpwds
    setpwds = "True"
    try:
        showinfo("=" * 25 + "设置密码" + "=" * 25)
        time.sleep(1)
        browser.find_element(By.XPATH, "//input[@type='text']").click()
        time.sleep(1)
        ele = browser.find_element(By.XPATH, "//*[@class='el-scrollbar']")
        ActionChains(browser).move_to_element(ele).perform()
        time.sleep(2)
        browser.find_element(By.XPATH, "//span[contains(text(),'English')]").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()
        time.sleep(3)
        status = browser.find_element(By.XPATH, "//input[@type='checkbox']").get_attribute("class")
        if "is-checked" not in status:
            browser.find_element(By.XPATH, "//input[@placeholder='Please enter password']").send_keys(pwd)
            time.sleep(1)
            browser.find_element(By.XPATH, "//input[@placeholder='Must be identical to above']").send_keys(pwd)
            time.sleep(1)
            browser.find_element(By.XPATH, "//button[contains(text(),'Apply')]").click()
            time.sleep(1)
            setpwds = "True"
        else:
            time.sleep(1)
            eles = browser.find_element(By.XPATH, "//input[@type='checkbox']")
            ActionChains(browser).move_to_element(eles).click(eles).perform()
            time.sleep(1)
            browser.find_element(By.XPATH, "//input[@placeholder='Please enter password']").send_keys(pwd)
            time.sleep(1)
            browser.find_element(By.XPATH, "//input[@placeholder='Must be identical to above']").send_keys(pwd)
            time.sleep(1)
            browser.find_element(By.XPATH, "//button[contains(text(),'Apply')]").click()
            setpwds = "True"
    except Exception as e:
        setpwds = "Flase"
        logging.info("设置密码失败:{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")

def changelg():
    try:
        showinfo("=" * 25 + "更改语言" + "=" * 25)
        browser.find_element(By.XPATH, "//span[@class='current-lang']").click()
        ele = browser.find_element(By.XPATH, "//li[contains(text(),'English')]")
        ActionChains(browser).move_to_element(ele).perform()
        time.sleep(2)
        browser.find_element(By.XPATH, "//li[contains(text(),'English')]").click()
        time.sleep(2)
        browser.refresh()
        time.sleep(5)
    except Exception as e:
        showinfo("更改语言失败{}".format(e))
        logging.info("更改语言失败{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")

def login():
    showinfo("=" * 25 + "登入界面" + "=" * 25)
    WebDriverWait(browser, 120, 0.5).until(
        lambda browser: browser.find_element(By.XPATH, "//input[@type='password']"))
    browser.find_element(By.XPATH, "//input[@type='password']").send_keys(123456)
    time.sleep(1)
    browser.find_element(By.XPATH,
                         "//button[@class='gl-btn btn-item primary-type oval-round is-capitalize']").click()
    time.sleep(5)

def import_config(config):
    try:
        showinfo("开始导入WireGuard config")
        browser.find_element(By.XPATH, "//span[contains(text(), ' VPN ')]").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//span[contains(text(), ' WireGuard Client ')]").click()
        time.sleep(1)
        try:
            browser.find_element(By.XPATH, "//span[contains(text(), 'Add Manually')]").click()
        except:
            browser.find_element(By.XPATH, "//span[contains(text(), 'New Group')]").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//span[@class='text-tips']").click()
        time.sleep(2)
        app = Desktop()
        dlg = app["打开"]
        dlg["Toolbar"].click()
        send_keys(config)
        send_keys("{VK_RETURN}", 2)
        time.sleep(5)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//div[@class='confirm-btn']/button")).click()
        time.sleep(5)
    except Exception as e:
        showinfo("导入WireGuard config文件失败：{}".format(e))
        logging.info("导入WireGuard config文件失败：{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")

def login_appli():
    try:
        browser.find_element(By.XPATH, "//span[contains(text(), ' VPN Dashboard ')]").click()
    except Exception as e:
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        showinfo("点击VPN Dashboard失败:{}".format(e))
        logging.info("点击VPN Dashboard失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")
def appli_config():
    showinfo("开始应用WireGuard config配置")
    logging.info("开始应用WireGuard config配置")
    global appli
    try:
        appli = "true"
        time.sleep(2)
        b = browser.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/table/tbody[2]/tr/td[4]/div/div/label/span")
        ActionChains(browser).move_to_element(b).click(b).perform()
        browser.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/table/tbody[2]/tr/td[4]/div/div/label/span").click()
        time.sleep(5)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//ul[@class='info-list']"))
        info_list = browser.find_element(By.XPATH, "//ul[@class='info-list']").text
        showinfo(info_list)
        logging.info(info_list)
        showinfo("开始检查是否能翻墙;ping 通 www.google.com")
        for i in range(5):
            time.sleep(60)
            with os.popen("ping -n 5 www.google.com", "r") as p:
                ping = p.read()
            showinfo("ping result:{}".format(ping))
            logging.info("ping result:{}".format(ping))
            p.close()
            if 'TTL' in ping:
                ping_result = str(re.findall("\d+%", ping)[0]).strip("%")
                showinfo("WireGuard_client connect succend,IPLR:{}".format(ping_result))
                logging.info("WireGuard_client connect succend,IPLR:{}".format(ping_result))
                appli = "true"
                time.sleep(1)
                break
            else:
                showinfo("{}ping google fail".format(i + 1))
                logging.info("{}ping google fail".format(i + 1))
                appli = "flase"
                continue
    except Exception as e:
        appli = "flase"
        showinfo("应用配置失败:{}".format(e))
        logging.info("应用配置失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")
        end.set(value=time.strftime('%m%d %H:%M:%S'))

def Unconfigure():
    try:
        global un
        un = "true"
        showinfo("开始断开WireGuard_client连接")
        logging.info("开始断开WireGuard_client连接")
        time.sleep(2)
        b = browser.find_element(By.XPATH, "//div[@class='status-switch']")
        ActionChains(browser).move_to_element(b).click(b).perform()
        time.sleep(5)
        for i in range(5):
            time.sleep(60)
            with os.popen("ping -n 5 www.baidu.com", "r") as p:
                ping = p.read()
            showinfo("ping result:{}".format(ping))
            logging.info("ping result:{}".format(ping))
            p.close()
            if 'TTL' not in ping:
                showinfo("已关闭WireGuard,{}次ping 百度s失败".format(i + 1))
                logging.info("已关闭WireGuard,{}次ping 百度s失败".format(i + 1))
                time.sleep(1)
                un = "flase"
                continue
            else:
                showinfo("WireGuard_client connect disuccend")
                logging.info("WireGuard_client connect disuccend")
                break
        time.sleep(10)
    except Exception as e:
        un = "flase"
        showinfo("断开WireGuard_client连接失败:{}".format(e))
        logging.info("断开WireGuard_client连接失败:{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")
def ssh_iptables(ip, pwd):
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
        stdin, stdout, stderr = ssh.exec_command("iptables -S")
        err_list = stderr.readlines()
        if len(err_list) > 0:
            showinfo('ssh 执行命令 [%s] 错误: %s' % ("iptables:", err_list[0]))
            logging.info('ssh 执行命令 [%s] 错误: %s' % ("iptables:", err_list[0]))
            SSH_Result = False
        else:
            buff = stdout.read().decode('utf-8')
            logging.info("iptables:{}".format(buff))
            SSH_Result = True
        ssh.close()
    except Exception as e:
        SSH_Result = False
        showinfo("ssh 设备异常:{}".format(e))
        logging.info("ssh 设备异常:{}".format(e))
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")
def WireGuard_client():
    try:
        logging.getLogger().setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        logging.basicConfig(filename=os.path.join(os.getcwd(), "WireGuard_client 反复断开连接测试" + current_time + '.log.txt'),
                            level=logging.DEBUG)
        WEBshowinfo_info()
        UUTPWDshowinfo_info()
        Configshowinfo_info()
        COUNTTshowinfo_info()
        INTERVALTshowinfo_info()
        WEB_Input.configure(state=DISABLED)
        UUTPWD_Input.configure(state=DISABLED)
        Config_Input.configure(state=DISABLED)
        COUNTT_Input.configure(state=DISABLED)
        INTERVALT_Input.configure(state=DISABLED)
        Start.configure(state=DISABLED)
        global WEB_AD
        global WEB_pwd
        global config
        global COUNT
        global INTERVALT
        start.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序进行中", bg="yellow")
        WEB_AD = WEB.pop()
        WEB_pwd = UUTPWD.pop()
        conf_N = FIRMWARE.pop()
        path = os.path.abspath(os.curdir)
        config_path = path + r"\WG_config\{}".format(conf_N)
        config = config_path
        COUNT = int(COUNTT.pop())
        INTERVALT = int(INTERVAL.pop())
        start.set(value=time.strftime('%m%d %H:%M:%S'))
        showinfo("网页IP: {}".format(WEB_AD))
        logging.info("网页IP: {}".format(WEB_AD))
        showinfo("配置地址 :{}".format(config))
        logging.info("配置地址 :{}".format(config))
        showinfo("运行次数：{}".format(COUNT))
        logging.info("运行次数：{}".format(COUNT))
        showinfo("每次循环间隔时间：{}".format(INTERVALT))
        logging.info("每次循环间隔时间：{}".format(INTERVALT))
        check_UUTstatus(WEB_AD)
        open_web(WEB_AD)
        if open_status == "True":
            WebDriverWait(browser, 120, 0.5).until(
                lambda browser: browser.find_element(By.XPATH, "//body"))
            text = browser.find_element(By.XPATH, "//body").text
            if "选择你的语言" in text or "Choose Your Language" in text:
                showinfo("=" * 25 + "初始界面" + "=" * 25)
                setpwd(WEB_pwd)
                if setpwds == "True":
                    browser.implicitly_wait(30)
                    time.sleep(5)
                    WebDriverWait(browser, 120, 0.5).until(
                        lambda browser: browser.find_element(By.XPATH, "//span[contains(text(), 'System')]"))
                    try:
                        import_config(config)
                    except Exception as e:
                        end.set(value=time.strftime('%m%d %H:%M:%S'))
                        showinfo("导入WireGuard配置失败:{}".format(e))
                        logging.info("导入WireGuard配置失败:{}".format(e))
                        status_label.configure(text="程序运行失败", bg="red")
                    login_appli()
                    for i in range(COUNT):
                        status_label.configure(text="程序进行中    循环次数：{}".format(i + 1), bg="yellow")
                        showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
                        appli_config()
                        if appli == "true":
                            time.sleep(10)
                            Unconfigure()
                            ssh_iptables(WEB_AD ,WEB_pwd)
                            if un == "true":
                                if i + 1 < COUNT:
                                    showinfo("=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                          INTERVALT) + "=" * 20)
                                    logging.info("=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                              INTERVALT) + "=" * 30)
                                    time.sleep(INTERVALT)
                                    continue
                                else:
                                    showinfo("程序运行完毕！！！")
                                    logging.info("程序运行完毕！！！")
                                    status_label.configure(text="程序运行完毕", bg="green")

                                    break
                            else:
                                status_label.configure(text="程序运行失败", bg="red")
                                end.set(value=time.strftime('%m%d %H:%M:%S'))
                                break
                        else:
                            showinfo("应用WireGuard配置失败")
                            logging.info("应用WireGuard配置失败")
                            status_label.configure(text="程序运行失败", bg="red")
                            break
                else:
                    end.set(value=time.strftime('%m%d %H:%M:%S'))
                    status_label.configure(text="程序运行失败", bg="red")
                    showinfo("设置密码失败!")

            else:
                login()
                changelg()
                try:
                    import_config(config)
                except Exception as e:
                    showinfo("导入WireGuard配置失败:{}".format(e))
                    logging.info("导入WireGuard配置失败:{}".format(e))
                    end.set(value=time.strftime('%m%d %H:%M:%S'))
                    status_label.configure(text="程序运行失败", bg="red")
                login_appli()
                for i in range(COUNT):
                    status_label.configure(text="程序进行中    循环次数：{}".format(i + 1), bg="yellow")
                    showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
                    appli_config()
                    if appli == "true":
                        time.sleep(10)
                        Unconfigure()
                        ssh_iptables(WEB_AD ,WEB_pwd)
                        if un == "true":
                            if i + 1 < COUNT:
                                showinfo("=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                      INTERVALT) + "=" * 20)
                                logging.info("=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1,
                                                                                                          INTERVALT) + "=" * 30)
                                time.sleep(INTERVALT)
                                continue
                            else:
                                showinfo("程序运行完毕！！！")
                                logging.info("程序运行完毕！！！")
                                status_label.configure(text="程序运行完毕", bg="green")
                                break
                        else:
                            status_label.configure(text="程序运行失败", bg="red")
                            break
                    else:
                        showinfo("应用WireGuard配置失败")
                        logging.info("应用WireGuard配置失败")
                        status_label.configure(text="程序运行失败", bg="red")
                        break
        else:
            showinfo("打开网页失败!")
            end.set(value=time.strftime('%m%d %H:%M:%S'))
            status_label.configure(text="程序运行失败", bg="red")
    except Exception as e:
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        status_label.configure(text="程序运行失败", bg="red")
        showinfo("ssh 设备异常:{}".format(e))
        logging.info("ssh 设备异常:{}".format(e))

Start = Button(frm2, text="开始测试", command=lambda: MyThread(WireGuard_client))
Start.grid(row=1, column=1, sticky="E")
Start.place(width=100, height=30, x=10, y=350)

root.update()

text = Text(frm1, bd=3,
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