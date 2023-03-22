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

UUTIP = []
UUTPWD = []
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


root = Tk()
root.geometry('840x440+200+200')
root.resizable(False,False)
root.title('不保留配置升级')



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

def FIRMWAREshowinfo_info(event=''):
    status_label.configure(text="输入固件位置：" + FIRMWARE_Input.get())
    showinfo("输入固件位置：" + FIRMWARE_Input.get())
    logging.info("输入固件位置：" + FIRMWARE_Input.get())
    FIRMWARE.append(FIRMWARE_Input.get())

def FIRMWAREdelete_info(event=''):
    status_label.configure(text="固件位置：" + FIRMWARE_Input.get())

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
Label_list = ["网页地址", "登入密码","固件名称", "循环次数", "间隔时间"]
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

FIRMWARE_M = tk.StringVar(value='openwrt-mt2500-4.2.0-1229-1672298092.bin')
FIRMWARE_Input = Entry(frm2, textvariable=FIRMWARE_M)
FIRMWARE_Input.grid(row=1, column=1, sticky="W")
FIRMWARE_Input.place(x=85, y=80)
FIRMWARE_Input.bind("<Return>", FIRMWAREshowinfo_info)
FIRMWARE_Input.bind("<Delete>", FIRMWAREdelete_info)

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

Start = Button(frm2, text="开始测试", command=lambda: MyThread(start_webtest))
Start.grid(row=1, column=1, sticky="E")
Start.place(width=100, height=30, x=10, y=350)

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
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging', 'enable-automation'])
    browser = getChromeDriver(options)
    url = r'http://' + ip + '/'
    browser.get(url)
    time.sleep(2)

def getChromeDriver(options=None):
    global browser
    try:
        showinfo("开始使用本机驱动打开浏览器")
        logging.info("开始使用本机驱动打开浏览器")
        path = os.path.abspath(os.curdir)
        driver_path = path + '\chromedriver.exe'
        showinfo("本机驱动地址{}".format(driver_path))
        logging.info("本机驱动地址{}".format(driver_path))
        browser = webdriver.Chrome(driver_path)
        return browser
    except SessionNotCreatedException as e:
        showinfo("使用本机驱动打开浏览器异常")
        logging.info("使用本机驱动打开浏览器异常:{}".format(e))
        showinfo("开始下载浏览器驱动")
        logging.info("开始下载浏览器驱动")
        driver_version = re.search(
            "Chrome version ([\d.]+)", str(e)).group(1)
        chrome_version = re.search(
            "Current browser version is ([\d.]+) with", str(e)).group(1)
        showinfo(f"驱动版本：{driver_version}，谷歌游览器版本：{chrome_version}，不兼容\n开始更新驱动...")
        logging.info(f"驱动版本：{driver_version}，谷歌游览器版本：{chrome_version}，不兼容\n开始更新驱动...")
        res = requests.get(
            "https://registry.npmmirror.com/-/binary/chromedriver/")
        versions = [obj["name"][:-1] for obj in res.json() if re.match("\d+",
                                                                       obj["name"]) and obj["name"].count(".") == 3]
        versions = {key: max(versions_split, key=lambda x: int(x[x.rfind(".") + 1:]))
                    for key, versions_split in itertools.groupby(versions, key=lambda x: x[:x.rfind(".")])}
        dest_version = versions[chrome_version[:chrome_version.rfind(".")]]
        showinfo("驱动将更新到:{}".format(dest_version))
        logging.info("驱动将更新到:{}".format(dest_version))
        file = f"chromedriver_{dest_version}_win32.zip"
        if not os.path.exists(file):
            url = f"https://registry.npmmirror.com/-/binary/chromedriver/{dest_version}/chromedriver_win32.zip"
            showinfo("驱动下载地址:{}".format(url))
            logging.info("驱动下载地址:{}".format(url))
            res = requests.get(url)
            with open(file, 'wb') as f:
                f.write(res.content)
        else:
            showinfo("文件已经下载到当前目录，下面直接使用缓存解压覆盖...")
            logging.info("文件已经下载到当前目录，下面直接使用缓存解压覆盖...")
        with zipfile.ZipFile(file) as zf:
            zf.extract("chromedriver.exe", ".")
        browser = webdriver.Chrome(options=options)
        return browser

def setpwd(pwd):
    global setpwds
    setpwds = "True"
    try:
        showinfo("=" * 25 + "开始设置密码" + "=" * 25)
        logging.info("=" * 25 + "开始设置密码" + "=" * 25)
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
        showinfo("设置密码失败:{}".format(e))
        logging.info("设置密码失败:{}".format(e))

def changelg():
    browser.find_element(By.XPATH,"//span[@class='current-lang']").click()
    ele = browser.find_element(By.XPATH,"//li[contains(text(),'English')]")
    ActionChains(browser).move_to_element(ele).perform()
    time.sleep(2)
    browser.find_element(By.XPATH,"//li[contains(text(),'English')]").click()
    time.sleep(2)
    browser.refresh()
    time.sleep(5)

def start_webtest():
    try:
        logging.getLogger().setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        logging.basicConfig(filename=os.path.join(os.getcwd(), "不保留配置页面升级" + current_time + '.log.txt'),
                            level=logging.DEBUG)
        WEBshowinfo_info()
        UUTPWDshowinfo_info()
        FIRMWAREshowinfo_info()
        COUNTTshowinfo_info()
        INTERVALTshowinfo_info()
        WEB_Input.configure(state=DISABLED)
        UUTPWD_Input.configure(state=DISABLED)
        FIRMWARE_Input.configure(state=DISABLED)
        COUNTT_Input.configure(state=DISABLED)
        INTERVALT_Input.configure(state=DISABLED)
        Start.configure(state=DISABLED)

        global WEB_AD
        global WEB_pwd
        global FIR_AD
        global COUNT
        global INTERVALT
        status_label.configure(text="程序进行中", bg="yellow")
        WEB_AD = WEB.pop()
        WEB_pwd = UUTPWD.pop()
        FIR_N = FIRMWARE.pop()
        path = os.path.abspath(os.curdir)
        driver_path = path + r"\firmware\{}".format(FIR_N)
        FIR_AD = driver_path
        COUNT = int(COUNTT.pop())
        INTERVALT = int(INTERVAL.pop())
        start.set(value=time.strftime('%m%d %H:%M:%S'))
        showinfo("网页IP: {}".format(WEB_AD))  # 显示在text中的内容
        logging.info("网页IP: {}".format(WEB_AD))  # 显示在log中的内容
        showinfo("固件地址 :{}".format(FIR_AD))
        logging.info("固件地址 :{}".format(FIR_AD))
        showinfo("运行次数：{}".format(COUNT))
        logging.info("运行次数：{}".format(COUNT))
        showinfo("每次循环间隔时间：{}".format(INTERVALT))
        logging.info("每次循环间隔时间：{}".format(INTERVALT))
        check_UUTstatus(WEB_AD)
        open_web(WEB_AD)
        if open_status == "True":
            success_count = 0
            faild_count = 0
            for i in range(COUNT):
                try:
                    status_label.configure(text="程序进行中    循环次数：{}".format(i + 1), bg="yellow")
                    showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
                    logging.info("=" * 30 + "{}".format(i + 1) + "=" * 30)
                    time.sleep(5)
                    WebDriverWait(browser, 120, 0.5).until(
                        lambda browser: browser.find_element(By.XPATH,"//body"))
                    text = browser.find_element(By.XPATH,"//body").text
                    if "选择你的语言" in text or "Choose Your Language" in text:
                        showinfo("初始界面")
                        logging.info("初始界面")
                        setpwd(WEB_pwd)
                        if setpwds == "True":
                            browser.implicitly_wait(30)
                            time.sleep(5)
                            WebDriverWait(browser, 120, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH,"//span[contains(text(), 'System')]"))
                            showinfo("=" * 25 + "设置密码成功" + "=" * 25)
                            logging.info("=" * 25 + "设置密码成功" + "=" * 25)
                            showinfo("=" * 25 + "开始页面升级" + "=" * 25)
                            logging.info("=" * 25 + "开始页面升级" + "=" * 25)
                            browser.find_element(By.XPATH,"//span[contains(text(), 'System')]").click()
                            time.sleep(2)
                            try:
                                WebDriverWait(browser, 10, 0.5).until(
                                    lambda browser: browser.find_element(By.XPATH,
                                                                         "//*[@id='app']/div/div[2]/div[1]/div/ul/li[7]/ul/li/ul/li[2]/span"))
                                browser.find_element(By.XPATH,
                                                     "//*[@id='app']/div/div[2]/div[1]/div/ul/li[7]/ul/li/ul/li[2]/span").click()
                            except:
                                WebDriverWait(browser, 10, 0.5).until(
                                    lambda browser: browser.find_element(By.XPATH, "//li[contains(text(), 'Upgrade')]"))
                                browser.find_element(By.XPATH, "//li[contains(text(), 'Upgrade')]").click()
                            time.sleep(2)
                            WebDriverWait(browser, 120, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH,"//*[@id='tab-local']"))
                            browser.find_element(By.XPATH,"//*[@id='tab-local']").click()
                            time.sleep(2)
                            WebDriverWait(browser, 120, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH,"//span[@class='allow-text-tips']"))
                            browser.find_element(By.XPATH,"//span[@class='allow-text-tips']").click()
                            showinfo("=" * 25 + "开始选择固件" + "=" * 25)
                            logging.info("=" * 25 + "开始选择固件" + "=" * 25)
                            time.sleep(1)
                            browser.implicitly_wait(5)
                            app = Desktop()  # 创建操作桌面的对象
                            dlg = app["打开"]  # 获取弹窗的窗口标题
                            dlg["Toolbar"].click()  # 获取文件路径填写输入框并点击
                            send_keys(FIR_AD)  # 在文件路径填写输入框输入文件存在的路径
                            send_keys("{VK_RETURN}", 2)  # 输入文件路径后按回车键
                            time.sleep(100)
                            WebDriverWait(browser, 120, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH, "//span[contains(text(),'Upload successful')]"))
                            text = browser.find_element(By.XPATH,"//label[@for='glUploadFile']").text
                            if "Upload successful" in text:
                                time.sleep(10)
                                showinfo("=" * 25 + "固件上传成功" + "=" * 25)
                                logging.info("=" * 25 + "固件上传成功" + "=" * 25)
                                try:
                                    WebDriverWait(browser, 120, 0.5).until(
                                        lambda browser: browser.find_element(By.XPATH,"//input[@type='checkbox']"))
                                    status = browser.find_element(By.XPATH,"//input[@type='checkbox']").get_attribute("class")

                                    if "is-checked" in status:
                                        b = browser.find_element(By.XPATH,"//input[@type='checkbox']")
                                        ActionChains(browser).move_to_element(b).click(b).perform()
                                        time.sleep(2)
                                        browser.find_element(By.XPATH,"//button[contains(text(),'install')]").click()
                                        time.sleep(2)
                                        try:
                                            WebDriverWait(browser, 120, 0.5).until(
                                                lambda browser: browser.find_element(By.XPATH,
                                                    "//*[@class='el-input el-input--suffix']"))
                                        except Exception as e:
                                            showinfo("升级失败:{}".format(e))
                                            logging.info("升级失败:{}".format(e))
                                            status_label.configure(text="程序运行失败", bg="red")
                                            faild_count += 1
                                            fail_ind.append(str(i + 1))
                                            WEB_Input.configure(state=NORMAL)
                                            UUTPWD_Input.configure(state=NORMAL)
                                            FIRMWARE_Input.configure(state=NORMAL)
                                            COUNTT_Input.configure(state=NORMAL)
                                            INTERVALT_Input.configure(state=NORMAL)
                                            Start.configure(state=NORMAL)
                                        finally:
                                            browser.refresh()
                                            time.sleep(2)
                                    else:
                                        WebDriverWait(browser, 120, 0.5).until(
                                            lambda browser: browser.find_element(By.XPATH,"//button[contains(text(),'install')]"))
                                        browser.find_element(By.XPATH,"//button[contains(text(),'install')]").click()
                                        time.sleep(1)
                                        try:
                                            WebDriverWait(browser, 120, 0.5).until(
                                                lambda browser: browser.find_element(By.XPATH,
                                                    "//*[@class='el-input el-input--suffix']"))
                                        except Exception as e:
                                            showinfo("升级失败:{}".format(e))
                                            logging.info("升级失败:{}".format(e))
                                            status_label.configure(text="程序运行失败", bg="red")
                                            faild_count += 1
                                            fail_ind.append(str(i + 1))
                                            WEB_Input.configure(state=NORMAL)
                                            UUTPWD_Input.configure(state=NORMAL)
                                            FIRMWARE_Input.configure(state=NORMAL)
                                            COUNTT_Input.configure(state=NORMAL)
                                            INTERVALT_Input.configure(state=NORMAL)
                                            Start.configure(state=NORMAL)
                                            break
                                        finally:
                                            check_UUTstatus(WEB_AD)
                                            browser.refresh()
                                            time.sleep(2)
                                except:
                                    result = browser.find_element(By.XPATH, "//span[@class='res-badge is-unpass']").text
                                    showinfo("=" * 25 + "固件上传成功,上传结果：{}".format(result) + "=" * 25)
                                    Reasons = browser.find_element(By.XPATH,
                                                                   "//*[@id='pane-local']/div/div[2]/div[1]").text
                                    showinfo("=" * 25 + "{}".format(Reasons) + "=" * 25)
                                    status_label.configure(text="程序运行失败", bg="red")
                                    faild_count += 1
                                    fail_ind.append(str(i + 1))
                                    WEB_Input.configure(state=NORMAL)
                                    UUTPWD_Input.configure(state=NORMAL)
                                    FIRMWARE_Input.configure(state=NORMAL)
                                    COUNTT_Input.configure(state=NORMAL)
                                    INTERVALT_Input.configure(state=NORMAL)
                                    Start.configure(state=NORMAL)
                                    break
                            else:
                                showinfo("固件上传失败：{}".format(text))
                                showinfo("请确认固件是否正确")
                                WEB_Input.configure(state=NORMAL)
                                UUTPWD_Input.configure(state=NORMAL)
                                FIRMWARE_Input.configure(state=NORMAL)
                                COUNTT_Input.configure(state=NORMAL)
                                INTERVALT_Input.configure(state=NORMAL)
                                Start.configure(state=NORMAL)
                                status_label.configure(text="程序运行失败", bg="red")
                                break
                        else:
                            browser.close()
                            showinfo("设置密码失败，程序暂停")
                            logging.info("设置密码失败，程序暂停")
                            status_label.configure(text="程序运行失败", bg="red")
                            WEB_Input.configure(state=NORMAL)
                            UUTPWD_Input.configure(state=NORMAL)
                            FIRMWARE_Input.configure(state=NORMAL)
                            COUNTT_Input.configure(state=NORMAL)
                            INTERVALT_Input.configure(state=NORMAL)
                            Start.configure(state=NORMAL)
                            break
                    else:
                        showinfo("登入界面")
                        logging.info("登入界面")
                        browser.implicitly_wait(30)
                        time.sleep(1)
                        WebDriverWait(browser, 120, 0.5).until(
                            lambda browser: browser.find_element(By.XPATH,"//input[@type='password']"))
                        browser.find_element(By.XPATH,"//input[@type='password']").send_keys(WEB_pwd)
                        time.sleep(1)
                        browser.find_element(By.XPATH,
                            "//button[@class='gl-btn btn-item primary-type oval-round is-capitalize']").click()
                        time.sleep(5)
                        changelg()
                        browser.implicitly_wait(30)
                        WebDriverWait(browser, 120, 0.5).until(
                            lambda browser: browser.find_element(By.XPATH,"//span[contains(text(), 'System')]"))
                        showinfo("=" * 25 + "已登入" + "=" * 25)
                        logging.info("=" * 25 + "已登入" + "=" * 25)
                        showinfo("=" * 25 + "开始页面升级" + "=" * 25)
                        logging.info("=" * 25 + "开始页面升级" + "=" * 25)
                        browser.find_element(By.XPATH,"//span[contains(text(), 'System')]").click()
                        time.sleep(1)
                        try:
                            WebDriverWait(browser, 10, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH,
                                                                     "//*[@id='app']/div/div[2]/div[1]/div/ul/li[7]/ul/li/ul/li[2]/span"))
                            browser.find_element(By.XPATH,
                                                 "//*[@id='app']/div/div[2]/div[1]/div/ul/li[7]/ul/li/ul/li[2]/span").click()
                        except:
                            WebDriverWait(browser, 10, 0.5).until(
                                lambda browser: browser.find_element(By.XPATH, "//li[contains(text(), 'Upgrade')]"))
                            browser.find_element(By.XPATH, "//li[contains(text(), 'Upgrade')]").click()
                        time.sleep(1)
                        WebDriverWait(browser, 120, 0.5).until(
                            lambda browser: browser.find_element(By.XPATH,"//*[@id='tab-local']"))
                        browser.find_element(By.XPATH,"//*[@id='tab-local']").click()
                        time.sleep(1)
                        WebDriverWait(browser, 120, 0.5).until(
                            lambda browser: browser.find_element(By.XPATH,"//span[@class='allow-text-tips']"))
                        browser.find_element(By.XPATH,"//span[@class='allow-text-tips']").click()
                        showinfo("=" * 25 + "开始选择固件" + "=" * 25)
                        logging.info("=" * 25 + "开始选择固件" + "=" * 25)
                        time.sleep(2)
                        app = Desktop()  # 创建操作桌面的对象
                        dlg = app["打开"]  # 获取弹窗的窗口标题

                        dlg["Toolbar"].click()  # 获取文件路径填写输入框并点击
                        send_keys(FIR_AD)  # 在文件路径填写输入框输入文件存在的路径
                        send_keys("{VK_RETURN}", 2)  # 输入文件路径后按回车键
                        time.sleep(100)
                        WebDriverWait(browser, 120, 0.5).until(
                            lambda browser: browser.find_element(By.XPATH,
                                                                 "//span[contains(text(),'Upload successful')]"))
                        text = browser.find_element(By.XPATH,"//label[@for='glUploadFile']").text
                        if "Upload successful" in text:
                            time.sleep(10)
                            showinfo("=" * 25 + "固件上传成功" + "=" * 25)
                            logging.info("=" * 25 + "固件上传成功" + "=" * 25)
                            try:
                                WebDriverWait(browser, 120, 0.5).until(
                                    lambda browser: browser.find_element(By.XPATH, "//input[@type='checkbox']"))
                                status = browser.find_element(By.XPATH, "//input[@type='checkbox']").get_attribute(
                                    "class")

                                if "is-checked" in status:
                                    b = browser.find_element(By.XPATH, "//input[@type='checkbox']")
                                    ActionChains(browser).move_to_element(b).click(b).perform()
                                    time.sleep(2)
                                    browser.find_element(By.XPATH, "//button[contains(text(),'install')]").click()
                                    time.sleep(2)
                                    try:
                                        WebDriverWait(browser, 120, 0.5).until(
                                            lambda browser: browser.find_element(By.XPATH,
                                                                                 "//*[@class='el-input el-input--suffix']"))
                                    except Exception as e:
                                        showinfo("升级失败:{}".format(e))
                                        logging.info("升级失败:{}".format(e))
                                        status_label.configure(text="程序运行失败", bg="red")
                                        faild_count += 1
                                        fail_ind.append(str(i + 1))
                                        WEB_Input.configure(state=NORMAL)
                                        UUTPWD_Input.configure(state=NORMAL)
                                        FIRMWARE_Input.configure(state=NORMAL)
                                        COUNTT_Input.configure(state=NORMAL)
                                        INTERVALT_Input.configure(state=NORMAL)
                                        Start.configure(state=NORMAL)
                                    finally:
                                        browser.refresh()
                                        time.sleep(2)

                                else:
                                    WebDriverWait(browser, 120, 0.5).until(
                                        lambda browser: browser.find_element(By.XPATH,
                                                                             "//button[contains(text(),'install')]"))
                                    browser.find_element(By.XPATH, "//button[contains(text(),'install')]").click()
                                    time.sleep(1)
                                    try:
                                        WebDriverWait(browser, 120, 0.5).until(
                                            lambda browser: browser.find_element(By.XPATH,
                                                                                 "//*[@class='el-input el-input--suffix']"))
                                    except Exception as e:
                                        showinfo("升级失败:{}".format(e))
                                        logging.info("升级失败:{}".format(e))
                                        status_label.configure(text="程序运行失败", bg="red")
                                        faild_count += 1
                                        fail_ind.append(str(i + 1))
                                        WEB_Input.configure(state=NORMAL)
                                        UUTPWD_Input.configure(state=NORMAL)
                                        FIRMWARE_Input.configure(state=NORMAL)
                                        COUNTT_Input.configure(state=NORMAL)
                                        INTERVALT_Input.configure(state=NORMAL)
                                        Start.configure(state=NORMAL)
                                        break
                                    finally:
                                        check_UUTstatus(WEB_AD)
                                        browser.refresh()
                                        time.sleep(2)
                            except:
                                result = browser.find_element(By.XPATH, "//span[@class='res-badge is-unpass']").text
                                showinfo("=" * 25 + "固件上传成功,上传结果：{}".format(result) + "=" * 25)
                                Reasons = browser.find_element(By.XPATH,
                                                               "//*[@id='pane-local']/div/div[2]/div[1]").text
                                showinfo("=" * 25 + "{}".format(Reasons) + "=" * 25)
                                status_label.configure(text="程序运行失败", bg="red")
                                faild_count += 1
                                fail_ind.append(str(i + 1))
                                WEB_Input.configure(state=NORMAL)
                                UUTPWD_Input.configure(state=NORMAL)
                                FIRMWARE_Input.configure(state=NORMAL)
                                COUNTT_Input.configure(state=NORMAL)
                                INTERVALT_Input.configure(state=NORMAL)
                                Start.configure(state=NORMAL)
                                break
                        else:
                            showinfo("固件上传失败：{}".format(text))
                            showinfo("请确认固件是否正确")
                            status_label.configure(text="程序运行失败", bg="red")
                            break
                    if i + 1 < COUNT:
                        success_count += 1
                        showinfo("升級成功,次數:{}".format(success_count))
                        logging.info("升級成功,次數:{}".format(success_count))
                        showinfo("=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 20)
                        logging.info(
                            "=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 30)
                        time.sleep(INTERVALT)
                        continue
                    else:
                        browser.close()
                        success_count += 1
                        showinfo("升級成功,次數:{}".format(success_count))
                        logging.info("升級成功,次數:{}".format(success_count))
                        end.set(value=time.strftime('%m%d %H:%M:%S'))
                        showinfo("程序运行完毕！！！")
                        logging.info("程序运行完毕！！！")
                        status_label.configure(text="程序运行完毕", bg="green")
                        break
                except Exception as e:
                    faild_count += 1
                    fail_ind.append(str(i + 1))
                    showinfo("异常 reason:{},".format(str(e)))
                    logging.info("异常 reason:{},".format(str(e)))
                    showinfo("异常次数 {}".format(faild_count))
                    logging.info("异常次数 {}".format(faild_count))
                    showinfo("异常目前为止错在第｛｝".format(fail_ind))
                    logging.info("异常目前为止错在第｛｝".format(fail_ind))
                    open_web(WEB_AD)
                    status_label.configure(text="程序运行失败", bg="red")
                    break
                showinfo("结束，总共报错在第｛｝".format(fail_ind))
                logging.info("结束，总共报错在第｛｝".format(fail_ind))
        else:
            browser.close()
            showinfo("网页开启失败，程序暂停")
            logging.info("网页开启失败，程序暂停")
            status_label.configure(text="程序运行失败", bg="red")
            WEB_Input.configure(state=NORMAL)
            UUTPWD_Input.configure(state=NORMAL)
            FIRMWARE_Input.configure(state=NORMAL)
            COUNTT_Input.configure(state=NORMAL)
            INTERVALT_Input.configure(state=NORMAL)
            Start.configure(state=NORMAL)
    except Exception as e:
        showinfo("升级失败:{}".format(e))
        logging.info("升级失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")
        WEB_Input.configure(state=NORMAL)
        UUTPWD_Input.configure(state=NORMAL)
        FIRMWARE_Input.configure(state=NORMAL)
        COUNTT_Input.configure(state=NORMAL)
        INTERVALT_Input.configure(state=NORMAL)
        Start.configure(state=NORMAL)
    finally:
        end.set(value=time.strftime('%m%d %H:%M:%S'))
        if i + 1 < COUNT:
            status_label.configure(text="程序运行失败", bg="red")
        else:
            status_label.configure(text="程序运行完毕", bg="green")
        WEB_Input.configure(state=NORMAL)
        UUTPWD_Input.configure(state=NORMAL)
        FIRMWARE_Input.configure(state=NORMAL)
        COUNTT_Input.configure(state=NORMAL)
        INTERVALT_Input.configure(state=NORMAL)
        Start.configure(state=NORMAL)

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

root.mainloop()