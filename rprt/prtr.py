import logging
import threading
import tkinter
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

root = Tk()
root.geometry('840x440+200+200')
root.resizable(False,False)
root.title('反复重启中继测试')


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
Label_list = ["网页地址", "登入密码", "中继wifi名称","中继wifi密码" ,"循环次数", "间隔时间"]
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

WIFIName_M = tk.StringVar(value='GL-TEST-PY')
WIFIName_Input = Entry(frm2, textvariable=WIFIName_M)
WIFIName_Input.grid(row=1, column=1, sticky="W")
WIFIName_Input.place(x=80, y=80)
WIFIName_Input.bind("<Return>", WIFINAMEshowinfo_info)
WIFIName_Input.bind("<Delete>", WIFINAMEdelete_info)

WIFIPWD_M = tk.StringVar(value='goodlife')
WIFIPWD_Input = Entry(frm2, textvariable=WIFIPWD_M)
WIFIPWD_Input.grid(row=1, column=1, sticky="W")
WIFIPWD_Input.place(x=80, y=110)
WIFIPWD_Input.bind("<Return>", WIFIPSWDshowinfo_info)
WIFIPWD_Input.bind("<Delete>", WIFIPSWDdelete_info)

COUNTT_M = tk.StringVar(value='200')
COUNTT_Input = Entry(frm2, textvariable=COUNTT_M)
COUNTT_Input.grid(row=1, column=1, sticky="W")
COUNTT_Input.place(x=80, y=140)
COUNTT_Input.bind("<Return>", COUNTTshowinfo_info)
COUNTT_Input.bind("<Delete>", COUNTTdelete_info)

INTERVALT_M = tk.StringVar(value='5')
INTERVALT_Input = Entry(frm2, textvariable=INTERVALT_M)
INTERVALT_Input.grid(row=1, column=1, sticky="W")
INTERVALT_Input.place(x=80, y=170)
INTERVALT_Input.bind("<Return>", INTERVALTshowinfo_info)
INTERVALT_Input.bind("<Delete>", INTERVALTdelete_info)

def open_web(ip):
    global browser
    global open_status
    showinfo("=" * 20+"开始打开网页"+"=" * 20)
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
        logging.info(r"驱动版本:{}，谷歌游览器版本：{}，不兼容\n开始更新驱动...".format(driver_version,chrome_version))
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
            url = r"https://registry.npmmirror.com/-/binary/chromedriver/{}/chromedriver_win32.zip".format(dest_version)
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
        showinfo("=" * 20+"开始设置密码"+"=" * 20)
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
        status_label.configure(text="程序运行失败", bg="red")

def changelg():
    browser.find_element(By.XPATH, "//span[@class='current-lang']").click()
    ele = browser.find_element(By.XPATH, "//li[contains(text(),'English')]")
    ActionChains(browser).move_to_element(ele).perform()
    time.sleep(2)
    browser.find_element(By.XPATH, "//li[contains(text(),'English')]").click()
    time.sleep(2)
    browser.refresh()
    time.sleep(5)

def login():
    WebDriverWait(browser, 120, 0.5).until(
        lambda browser: browser.find_element(By.XPATH, "//input[@type='password']"))
    browser.find_element(By.XPATH, "//input[@type='password']").send_keys(123456)
    time.sleep(1)
    browser.find_element(By.XPATH,
                         "//button[@class='gl-btn btn-item primary-type oval-round is-capitalize']").click()
    time.sleep(5)

def check_status():
    global sta
    showinfo("=" * 20+"开始检查设备是否已中继"+"=" * 20)
    time.sleep(10)
    browser.implicitly_wait(30)
    WebDriverWait(browser, 120, 0.5).until(
        lambda browser: browser.find_element(By.XPATH, "//span[contains(text(), 'System')]"))
    t = browser.find_element(By.XPATH, "//*[@class='repeater-container']").text
    logging.info("中继状态:{}".format(t))
    if "disabled" in t:
        sta = "disconnected"
    else:
        sta = "connected"

def input_connect(WIFI_NAME,WIFI_PWD):
    try:
        showinfo("=" * 25 + "开始输入方式中继" + "=" * 25)
        logging.info("=" * 25 + "开始输入方式中继" + "=" * 25)
        browser.find_element(By.XPATH, "//span[@class='operation']").click()
        time.sleep(5)
        browser.find_element(By.XPATH, "//span[contains(text(), 'Join Other Network')]").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//input[@maxlength='32']").send_keys(WIFI_NAME)
        time.sleep(1)
        browser.find_element(By.XPATH, "//input[@placeholder='请选择']").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//span[contains(text(), 'WPA/WPA2/WPA3')]").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//*[@id='wifiKey']").send_keys(WIFI_PWD)
        time.sleep(1)
        browser.find_element(By.XPATH, "//div[@class='dialog-footer-btns']/button[2]").click()
        time.sleep(10)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//button[contains(text(),'Disable')]"))
        t = browser.find_element(By.XPATH, "//div[@class='repeater-wrapper']").text
        logging.info("查看中继是否成功:{}".format(t))
        if WIFI_NAME in t:
            showinfo("输入中继成功")
            showinfo(t)
            connect_reps == "True"
        else:
            showinfo("输入中继失败")
            showinfo(t)
            connect_reps == "False"
    except Exception as e:
        showinfo("输入中继fail:{}".format(e))
        logging.info("输入中继fail:{}".format(e))
        connect_reps == "False"
def scan_connect(WIFI_NAME,WIFI_PWD):
    global connect_reps
    try:
        showinfo("=" * 25 + "开始扫描方式中继" + "=" * 25)
        logging.info("=" * 25 + "开始扫描方式中继" + "=" * 25)
        clear_list(WIFI_NAME)
        time.sleep(10)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//span[contains(text(), '{}')]".format(WIFI_NAME)))
        time.sleep(3)
        browser.find_element(By.XPATH, "//span[contains(text(), '{}')]".format(WIFI_NAME)).click()
        time.sleep(5)
        b = browser.find_element(By.XPATH, "//*[@class='inp el-input el-input--suffix']")
        ActionChains(browser).move_to_element(b).click(b).perform()
        browser.find_element(By.XPATH, "//*[@class='inp el-input el-input--suffix']").click()
        time.sleep(1)
        browser.find_element(By.XPATH, "//*[@id='wifiKey']").send_keys(WIFI_PWD)
        time.sleep(1)
        browser.find_element(By.XPATH, "//div[@class='dialog-footer-btns']/button[2]").click()
        time.sleep(10)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//button[contains(text(),'Disable')]"))
        t = browser.find_element(By.XPATH, "//div[@class='repeater-wrapper']").text
        logging.info("查看中继是否成功:{}".format(t))
        if WIFI_NAME in t:
            showinfo("=" * 25 + "扫描方式中继成功" + "=" * 25)
            logging.info("=" * 25 + "扫描方式中继成功" + "=" * 25)
            logging.info(t)
            connect_reps == "True"
        else:
            showinfo("=" * 25 + "扫描方式中继失败" + "=" * 25)
            logging.info("=" * 25 + "扫描方式中继失败" + "=" * 25)
            status_label.configure(text="程序运行失败", bg="red")
            connect_reps == "False"
    except Exception as  e:
        connect_reps == "False"
        showinfo("扫描方式中继失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")

def clear_list(WIFI_NAME):
    showinfo("开始清除连接列表")
    browser.find_element(By.XPATH, "//span[@class='operation']").click()
    time.sleep(1)
    l=browser.find_element(By.XPATH, "//div[@class='el-dialog__body']").text
    logging.info("Known Networks:{}".format(l))
    if "Known Networks" in l:
        showinfo("存在需要清除的wifi")
        logging.info("存在需要清除的wifi")
        list=browser.find_element(By.XPATH, "//div[@class='saved-ap-main']").text
        if WIFI_NAME in list:
            logging.info("list:{}".format(list))
            browser.find_element(By.XPATH, "//span[@class='iconfont icon-delete']").click()
            time.sleep(3)
        else:
            time.sleep(1)
    else:
        showinfo("不存在需要清除的wifi")
        logging.info("不存在需要清除的wifi")
        time.sleep(1)

def disconnect():
    showinfo("=" * 25 + "开始断开中继" + "=" * 25)
    logging.info("=" * 25 + "开始断开中继" + "=" * 25)
    browser.find_element(By.XPATH, "//button[contains(text(),'Disable')]").click()
    time.sleep(3)

def connect_rep():
    global connect_reps
    WebDriverWait(browser, 120, 0.5).until(
        lambda browser: browser.find_element(By.XPATH, "//body"))
    text = browser.find_element(By.XPATH, "//body").text
    if "选择你的语言" in text or "Choose Your Language" in text:
        setpwd(WEB_pwd)
        if setpwds == "True":
            browser.implicitly_wait(30)
            time.sleep(5)
            WebDriverWait(browser, 120, 0.5).until(
                lambda browser: browser.find_element(By.XPATH, "//span[contains(text(), 'System')]"))
            try:
                check_status()
            except Exception as e:
                showinfo("检查设备中继状态失败:{}".format(e))
                logging.info("检查设备中继状态失败:{}".format(e))
                status_label.configure(text="程序运行失败", bg="red")
            if sta == "disconnected":
                showinfo("=" * 20 + "中继未连接，开始中继wifi" + "=" * 20)
                logging.info("=" * 20 + "中继未连接，开始中继wifi" + "=" * 20)
                try:
                    scan_connect(WIFI_NAME, WIFI_PWD)
                except Exception as e:
                    showinfo("扫描中继测试fail:{}".format(e))
                    logging.info("扫描中继测试fail:{}".format(e))
                    try:
                        input_connect(WIFI_NAME, WIFI_PWD)
                    except Exception as e:
                        showinfo("输入中继测试fail:{}".format(e))
                        logging.info("输入中继测试fail:{}".format(e))
            else:
                showinfo("=" * 20 + "中继已连接" + "=" * 20)
                disconnect()
                try:
                    scan_connect(WIFI_NAME, WIFI_PWD)
                except Exception as e:
                    showinfo("扫描中继测试fail:{}".format(e))
                    logging.info("扫描中继测试fail:{}".format(e))
                    try:
                        input_connect(WIFI_NAME, WIFI_PWD)
                    except Exception as e:
                        showinfo("输入中继测试fail:{}".format(e))
                        logging.info("输入中继测试fail:{}".format(e))
        else:
            showinfo("设置密码失败")
            status_label.configure(text="程序运行失败", bg="red")
    else:
        showinfo("=" * 20 + "登入界面" + "=" * 20)
        browser.implicitly_wait(30)
        time.sleep(1)
        try:
            login()
        except Exception as e:
            showinfo("登入WEB失败:{}".format(e))
            status_label.configure(text="程序运行失败", bg="red")
        try:
            changelg()
        except Exception as e:
            showinfo("更改语言失败:{}".format(e))
            status_label.configure(text="程序运行失败", bg="red")
        try:
            check_status()
        except Exception as e:
            showinfo("检查设备中继状态失败:{}".format(e))
            logging.info("检查设备中继状态失败:{}".format(e))
            status_label.configure(text="程序运行失败", bg="red")
        if sta == "disconnected":
            showinfo("=" * 20 + "中继未连接，开始中继wifi" + "=" * 20)
            logging.info("=" * 20 + "中继未连接，开始中继wifi" + "=" * 20)
            try:
                scan_connect(WIFI_NAME, WIFI_PWD)
            except Exception as e:
                showinfo("扫描中继测试fail:{}".format(e))
                logging.info("扫描中继测试fail:{}".format(e))
                try:
                    input_connect(WIFI_NAME, WIFI_PWD)
                except Exception as e:
                    showinfo("输入中继测试fail:{}".format(e))
                    logging.info("输入中继测试fail:{}".format(e))
        else:
            showinfo("=" * 20 + "中继已连接" + "=" * 20)
            logging.info("=" * 20 + "中继已连接" + "=" * 20)
            disconnect()
            try:
                scan_connect(WIFI_NAME, WIFI_PWD)
            except Exception as e:
                showinfo("扫描中继测试fail:{}".format(e))
                logging.info("扫描中继测试fail:{}".format(e))
                try:
                    input_connect(WIFI_NAME, WIFI_PWD)
                except Exception as e:
                    showinfo("输入中继测试fail:{}".format(e))
                    logging.info("输入中继测试fail:{}".format(e))
            time.sleep(30)

def reboot_check():
    global rbcheck_status
    try:
        rbcheck_status = "true"
        time.sleep(2)
        b = browser.find_element(By.XPATH, "//span[@class='iconfont icon-reboot']")
        ActionChains(browser).move_to_element(b).perform()
        browser.find_element(By.XPATH, "//span[@class='iconfont icon-reboot']").click()
        time.sleep(5)
        browser.find_element(By.XPATH, "//button[@class='gl-btn dialog-btn abort-type oval-round is-capitalize']").click()
        time.sleep(10)
        WebDriverWait(browser, 120, 0.5).until(
            lambda browser: browser.find_element(By.XPATH, "//input[@type='password']"))
        try:
            login()
            time.sleep(60)
        except Exception as e:
            showinfo("登入WEB失败:{}".format(e))
            status_label.configure(text="程序运行失败", bg="red")
        try:
            check_status()
        except Exception as e:
            showinfo("检查设备中继状态失败:{}".format(e))
            logging.info("检查设备中继状态失败:{}".format(e))
            status_label.configure(text="程序运行失败", bg="red")
        if sta == "disconnected":
            showinfo("=" * 20 + "中继未连接,测试fail" + "=" * 20)
            logging.info("=" * 20 + "中继未连接,测试fail" + "=" * 20)
        else:
            showinfo("=" * 20 + "中继已连接" + "=" * 20)
            logging.info("=" * 20 + "中继已连接" + "=" * 20)
            time.sleep(30)
    except Exception as e:
        rbcheck_status="fail"
        showinfo("重启设备检查自动中继失败:{}".format(e))
        logging.info("重启设备检查自动中继失败:{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")

def repeater():
    try:
        logging.getLogger().setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        for h in root_logger.handlers:
            root_logger.removeHandler(h)
        current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        logging.basicConfig(filename=os.path.join(os.getcwd(), "反复重启中继测试" + current_time + '.log.txt'),
                            level=logging.DEBUG)
        WEBshowinfo_info()
        UUTPWDshowinfo_info()
        WIFINAMEshowinfo_info()
        WIFIPSWDshowinfo_info()
        COUNTTshowinfo_info()
        INTERVALTshowinfo_info()
        WEB_Input.configure(state=DISABLED)
        UUTPWD_Input.configure(state=DISABLED)
        WIFIName_Input.configure(state=DISABLED)
        WIFIPWD_Input.configure(state=DISABLED)
        COUNTT_Input.configure(state=DISABLED)
        INTERVALT_Input.configure(state=DISABLED)
        Start.configure(state=DISABLED)
        global WEB_AD,WEB_pwd,WIFI_NAME,WIFI_PWD,COUNT,INTERVALT
        status_label.configure(text="程序进行中", bg="yellow")
        WEB_AD = WEB.pop()
        WEB_pwd = UUTPWD.pop()
        WIFI_NAME = WIFINAME.pop()
        WIFI_PWD = WIFIPWD.pop()
        COUNT = int(COUNTT.pop())
        INTERVALT = int(INTERVAL.pop())
        showinfo("网页IP: {}".format(WEB_AD))  # 显示在text中的内容
        logging.info("网页IP: {}".format(WEB_AD))  # 显示在log中的内容
        showinfo("网页登入密码 :{}".format(WEB_pwd))
        logging.info("网页登入密码 :{}".format(WEB_pwd))
        showinfo("中继wifi名称 :{}".format(WIFI_NAME))
        logging.info("中继wifi名称 :{}".format(WIFI_NAME))
        showinfo("中继wifi密码 :{}".format(WIFI_PWD))
        logging.info("中继wifi密码 :{}".format(WIFI_PWD))
        showinfo("运行次数：{}".format(COUNT))
        logging.info("运行次数：{}".format(COUNT))
        showinfo("每次循环间隔时间：{}".format(INTERVALT))
        logging.info("每次循环间隔时间：{}".format(INTERVALT))
        check_UUTstatus(WEB_AD)
        success_count = 0
        status_label.configure(text="程序进行中    循环次数: 0", bg="yellow")
        open_web(WEB_AD)
        connect_rep()
        if connect_reps == "True":
            showinfo("已首次中继成功，正在进行设备重启")
            logging.info("已首次中继成功，正在进行设备重启")
            for i in range(COUNT):
                status_label.configure(text="程序进行中    循环次数: {}".format(i + 1), bg="yellow")
                showinfo("=" * 25 + "{}".format(i + 1) + "=" * 25)
                reboot_check()
                if rbcheck_status == "true":
                    if i + 1 < COUNT:
                        success_count += 1
                        showinfo("=" * 20 + "重启自动中继成功,次數:{}".format(success_count) + "=" * 20)
                        logging.info("=" * 20 + "重启自动中继成功,次數:{}".format(success_count) + "=" * 20)
                        showinfo(
                            "=" * 20 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 20)
                        logging.info(
                            "=" * 30 + "The {} loop ends,Waiting {} S sleep time".format(i + 1, INTERVALT) + "=" * 30)
                        time.sleep(INTERVALT)
                        continue
                    else:
                        browser.close()
                        success_count += 1
                        showinfo("重启自动中继成功,次數:{}".format(success_count))
                        logging.info("重启自动中继成功,次數:{}".format(success_count))
                        end.set(value=time.strftime('%m%d %H:%M:%S'))
                        showinfo("程序运行完毕！！！")
                        logging.info("程序运行完毕！！！")
                        status_label.configure(text="程序运行完毕", bg="green")
                        break
                else:
                    showinfo("重启后自动中继失败！")
                    logging.info("重启后自动中继失败！")
                    status_label.configure(text="程序运行失败", bg="red")
                    WEB_Input.configure(state=NORMAL)
                    UUTPWD_Input.configure(state=NORMAL)
                    WIFIName_Input.configure(state=NORMAL)
                    WIFIPWD_Input.configure(state=NORMAL)
                    COUNTT_Input.configure(state=NORMAL)
                    INTERVALT_Input.configure(state=NORMAL)
                    Start.configure(state=NORMAL)
                    break
        else:
            showinfo("中继测试失败")
            logging.info("中继测试失败")
            status_label.configure(text="程序运行失败", bg="red")
            WEB_Input.configure(state=NORMAL)
            UUTPWD_Input.configure(state=NORMAL)
            WIFIName_Input.configure(state=NORMAL)
            WIFIPWD_Input.configure(state=NORMAL)
            COUNTT_Input.configure(state=NORMAL)
            INTERVALT_Input.configure(state=NORMAL)
            Start.configure(state=NORMAL)
    except Exception as e:
        showinfo("中继测试失败：{}".format(e))
        logging.info("中继测试失败：{}".format(e))
        status_label.configure(text="程序运行失败", bg="red")
        WEB_Input.configure(state=NORMAL)
        UUTPWD_Input.configure(state=NORMAL)
        WIFIName_Input.configure(state=NORMAL)
        WIFIPWD_Input.configure(state=NORMAL)
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
        WIFIName_Input.configure(state=NORMAL)
        WIFIPWD_Input.configure(state=NORMAL)
        COUNTT_Input.configure(state=NORMAL)
        INTERVALT_Input.configure(state=NORMAL)
        Start.configure(state=NORMAL)



Start = Button(frm2, text="开始测试", command=lambda: MyThread(repeater))
Start.grid(row=1, column=1, sticky="E")
Start.place(width=100, height=30, x=10, y=350)


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