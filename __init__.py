# import time
#
# import paramiko
#
#
# def dial():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname="192.168.11.1",
#                 username="root",
#                 port="22",
#                 password="123456")
#     send_command = ssh.invoke_shell()
#     send_command.send(r"uci set network.modem_0001.disabled=0" + '\n')
#     send_command.send(r"/etc/init.d/network reload" + '\n')
#     time.sleep(5)
#     ssh.close()
#
# def fial():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname="192.168.11.1",
#                 username="root",
#                 port="22",
#                 password="123456")
#     send_command = ssh.invoke_shell()
#     send_command.send(r"uci set network.modem_0001.disabled=1" + '\n')
#     send_command.send(r"/etc/init.d/network reload" + '\n')
#     time.sleep(5)
#     ssh.close()
#
# def check_online():
#     for i in range(5):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(hostname="192.168.11.1",
#                     username="root",
#                     port="22",
#                     password="123456")
#         stdin, stdout, stderr = ssh.exec_command("tmp=`/sbin/ifstatus modem_0001_4 | grep up`;echo $tmp")
#         err_list = stderr.readlines()
#         if len(err_list) > 0:
#             print('ssh 执行命令 [%s] 错误: %s' % ("reboot", err_list[0]))
#             SSH_Result = False
#         else:
#             buff = stdout.read().decode('utf-8')
#             if "true" in buff:
#                 print(buff)
#                 time.sleep(5)
#                 ssh.close()
#                 break
#             else:
#                 print(buff)
#                 time.sleep(5)
#                 ssh.close()
#                 continue
#
#
# def test():
#     dial()
#     check_online()
#     fial()
#
#
# # test()
# driver_version="1231321"
# chrome_version="5464645"
#

import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *

# ---------------------以下代码负责绘制GUI界面---------------------
mytitle='漏洞扫描器'
global textMess

#建立主窗口
root=tk.Tk()
root.title(mytitle)
# 通过geometry函数来设置窗口的宽和高,移动窗口在屏幕上的位置
root.geometry('{}x{}+{}+{}'.format(750, 650, 400, 75))

# 输入框
frame=tk.Frame(root)
frame.pack()

label_1 = Label(frame, width=13, text="请输入IP地址:", font=("黑体",11))
label_1.pack(side=LEFT, padx=0, pady=10)

entry_1 = Entry(frame, width=20, font=("Consolas",11))
entry_1.pack(side=LEFT, after=label_1, padx=10, pady=10, fill=X)

label_2 = Label(frame, width=6, text="端口号:", font=("黑体",11))
label_2.pack(side=LEFT, after=entry_1, padx=10, pady=10)

entry_2 = Entry(frame, width=10, font=("Consolas",11))
entry_2.pack(side=LEFT, after=label_2, padx=0, pady=10, fill=X)

label_3 = Label(frame, width=8, text="timeout:", font=("Consolas",11))
label_3.pack(side=LEFT, after=entry_2, padx=10, pady=10)

timeout=tk.IntVar(value=3)
entry_3 = Entry(frame, width=5, textvariable=timeout, font=("Consolas",11))
# print(type(timeout.get()))
entry_3.pack(side=LEFT, after=label_3, padx=0, pady=10, fill=X)

# start按钮
button=tk.Button(frame,text='start', font=("Consolas",11))
button.pack(side=LEFT, after=entry_3, ipadx=10, padx=20)

button['command']=lambda:start()

# 点击按钮开始进行扫描


def start():
    size = 1000
    if entry_1.get() == '':
        entry_1.set("1-65535")
    # scanner(verbose, timeout, dst, port, ping, syn, size, ssh, os_ttl, os_nmap)
    scanner(verbose=checkbut_v.get(), timeout=entry_3.get(), dst=entry_1.get(),
            port=entry_2.get(), ping=checkbut_ping.get(), syn=checkbut_syn.get(),
            size=size, ssh=checkbut_ssh.get(), os_ttl=checkbut_ttl.get(),
            os_nmap=checkbut_nmap.get())


# 复选框
frame1=tk.Frame(root)
frame1.pack()

checkbut_v=BooleanVar()
checkbtn_1=Checkbutton(frame1, width=10,text="verbose",variable=checkbut_v, font=("Consolas",11))
checkbtn_1.pack(side=LEFT)

checkbut_ping=BooleanVar(value=True)
checkbtn_2=Checkbutton(frame1, width=10,text="ping",variable=checkbut_ping,state='disabled', font=("Consolas",11))
checkbtn_2.pack(side=LEFT, after=checkbtn_1)

checkbut_syn=BooleanVar()
checkbtn_3=Checkbutton(frame1, width=10, text="syn",variable=checkbut_syn, font=("Consolas",11))
checkbtn_3.pack(side=LEFT, after=checkbtn_2)

checkbut_ssh=BooleanVar()
checkbtn_4=Checkbutton(frame1, width=10, text="ssh",variable=checkbut_ssh, font=("Consolas",11))
checkbtn_4.pack(side=LEFT, after=checkbtn_3)

checkbut_ttl=BooleanVar()
checkbtn_5=Checkbutton(frame1, width=10, text="os_ttl",variable=checkbut_ttl, font=("Consolas",11))
checkbtn_5.pack(side=LEFT, after=checkbtn_4)

checkbut_nmap=BooleanVar()
checkbtn_6=Checkbutton(frame1, width=10, text="os_nmap",variable=checkbut_nmap, font=("Consolas",11))
checkbtn_6.pack(side=LEFT, after=checkbtn_5)

# 显示help信息
frame2=tk.LabelFrame(root,text='Help',height=7,font=("consolas",11))
frame2.pack(fill=tk.BOTH, expand=0)

textMess_2= ScrolledText(frame2,bg='white', height=7,font=("consolas",11))
textMess_2.pack(fill=tk.BOTH, expand=1)

textMess_2.insert(tk.END,"IP: The IP address you want to scan\n")
textMess_2.insert(tk.END,"Port: Port ranges, example: 22 or 1-1024 (default 1-65535)\n")
textMess_2.insert(tk.END,"Ping: ICMP ping before scan\n")
textMess_2.insert(tk.END,"SYN: TCP SYN scan\n")
textMess_2.insert(tk.END,"SSH: If SSH service is open, scan ssh version and detect weak password or not\n")
textMess_2.insert(tk.END,"OS_TTL: Use the parameter ttl to scan the type of OS\n")
textMess_2.insert(tk.END,"OS_Nmap: Use the tool nmap to scan the type of OS\n")
textMess_2.insert(tk.END,"Timeout: How much time to wait after the last packet has been sent\n")

# 为信息框设置一个容器
frame3=tk.LabelFrame(root,text='信息框',height=10, font=("黑体",11))
frame3.pack(fill=tk.BOTH, expand=1)

# 放置一个文本框作为信息输出窗口
textMess= ScrolledText(frame3,bg='white', height=10,font=("consolas",11))
textMess.pack(fill=tk.BOTH, expand=YES)

# 输出信息
def myprint(txt):
    global textMess
    if textMess != None :
        textMess.insert(tk.END, txt)
        textMess.insert(tk.END, '\n')
        textMess.see(tk.END)

# 输出回车
def myprint_n():
    global textMess
    textMess.insert(tk.END, '\n')
    textMess.see(tk.END)

# 输出彩色信息
def colorprint(txt,color):
    global textMess
    if textMess != None :
        if color!='black':
            textMess.tag_config(color, foreground=color)
        textMess.insert(tk.END, txt,color)
        textMess.insert(tk.END, '\n')
        textMess.see(tk.END)

# 进入Tkinter消息循环
root.mainloop()
