# -*- coding: UTF-8 -*-
import win32api
import win32gui
import win32con
import win32clipboard as clipboard
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import random
from random import randint
from random import choice


###############################
#  微信发送
###############################
def send_m(win):
    # 以下为“CTRL+V”组合键,回车发送，（方法一）
    win32api.keybd_event(17, 0, 0, 0)  # 有效，按下CTRL
    time.sleep(1)  # 需要延时
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, 86, 0)  # V
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开CTRL
    time.sleep(1)  # 缓冲时间
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 回车发送
    return


def txt_ctrl_v(txt_str):
    # 定义文本信息,将信息缓存入剪贴板
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, txt_str)
    clipboard.CloseClipboard()
    return


# 随机日期
def rand_time():
    localtime = time.localtime(time.time())
    date = datetime.date(randint(2010, localtime.tm_year), randint(1, localtime.tm_mon), randint(1, localtime.tm_mday))
    print date
    return date


def day_iciba():
    # curl "http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=2020-04-23" | python -m json.tool
    while True:
        dai = rand_time()
        url = "http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=%s" % dai
        r = requests.get(url)
        if r.status_code != 200:
            continue
        if r.json()['errno'] != 0:
            continue
        content = r.json()['content']
        note = r.json()['note']
        content = u'双语——英语：\n\r"' + content + u'"\n\r"' + note + u'"'
        return content


def day_hitokoto():
    maps = {'a': u'动画', 'b': u'漫画', 'c': u'游戏', 'd': u'文学', 'e': u'原创', 'f': u'来自网络', 'g': u'其他', 'h': u'影视',
            'i': u'诗词', 'j': u'网易云', 'k': u'哲学', '  l': u'抖机灵'}
    mi = choice(maps.keys())
    # 一言 ：https://hitokoto.cn/
    url = "https://v1.hitokoto.cn/?c=%s&encode=json" % mi
    r = requests.get(url)
    content = maps[mi] + u':\n\r"' + r.json()['hitokoto'] + u'"'
    return content


def get_content(num=0):
    if not num:
        num = random.randint(0, 2)

    print "num=%s" % num
    if num and num == 1:
        return day_hitokoto()
    if num and num == 2:
        return day_iciba()
    return day_hitokoto()


def get_window(className, titleName):
    # FindWindow('WeCaht')
    pHwnd = win32gui.FindWindow('ChatWnd', None)

    # 强行显示界面后才好截图
    win32gui.ShowWindow(pHwnd, win32con.SW_RESTORE)
    # win32gui.ShowWindow(pHwnd, win32con.SW_SHOWMINIMIZED)

    # 将窗口提到最前
    # win32gui.SetForegroundWindow(pHwnd)

    # 使窗体最大化
    # win32gui.ShowWindow(win, win32con.SW_MAXIMIZE)
    # win = win32gui.FindWindow(className, titleName)
    # print("找到【%s】这个人句柄：%x" % (titleName, pHwnd))
    if pHwnd != 0:
        left, top, right, bottom = win32gui.GetWindowRect(pHwnd)
        print(left, top, right, bottom)  # 最小化为负数
        win32gui.SetForegroundWindow(pHwnd)  # 获取控制
        time.sleep(0.5)
    else:
        print('请注意：找不到【%s】这个人（或群），请激活窗口！' % titleName)
    return pHwnd


#######################发送过程=================
n_time = 1


def sendTaskLog():
    # 查找微信小窗口
    win = get_window('WeCaht', '叶云云')
    # 读取远程文本
    content = get_content()
    content = content + u'\n\r\t\t\t\t------小东东机器人[Grin]'
    # print content
    txt_ctrl_v(content)
    send_m(win)
    global n_time
    n_time = n_time + 1
    print n_time


scheduler = BlockingScheduler()
# 5小时一次
scheduler.add_job(sendTaskLog, 'interval', hours=1)
# scheduler.add_job(sendTaskLog, 'interval', seconds=3600)
scheduler.add_job(sendTaskLog, 'cron', day_of_week='mon-fri', hour=7, minute=31, second='10', misfire_grace_time=30)
# scheduler.add_job(sendTaskLog, 'cron', day_of_week='mon-fri', hour=6, minute=55, second='10', misfire_grace_time=30)
try:
    sendTaskLog()
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
