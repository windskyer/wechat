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
import logging
import sys

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.DEBUG)  # DEBUG
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
han = logging.StreamHandler(sys.stdout)
han.setFormatter(fmt)
log.addHandler(han)


# 获取双语文库
def day_iciba():
    # curl "http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=2020-04-23" | python -m json.tool
    while True:
        # 随机日期
        localtime = time.localtime(time.time())
        date = datetime.date(randint(2018, localtime.tm_year), randint(1, localtime.tm_mon),
                             randint(1, localtime.tm_mday))
        url = "http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=%s" % date
        r = requests.get(url)
        if r.status_code != 200:
            continue
        if r.json()['errno'] != 0:
            continue
        content = r.json()['content']
        note = r.json()['note']
        content = u'双语——英语：\n\r"' + content + u'"\n\r"' + note + u'"'
        return content


# 获取一言文库
def day_hitokoto():
    maps = {'a': u'动画', 'b': u'漫画', 'c': u'游戏', 'd': u'文学', 'e': u'原创', 'f': u'来自网络', 'g': u'其他', 'h': u'影视',
            'i': u'诗词', 'j': u'网易云', 'k': u'哲学', '  l': u'抖机灵'}
    mi = choice(maps.keys())
    # 一言 ：https://hitokoto.cn/
    url = "https://v1.hitokoto.cn/?c=%s&encode=json" % mi
    while True:
        try:
            r = requests.get(url)
        except requests.ConnectionError:
            continue
        else:
            content = maps[mi] + u':\n\r"' + r.json()['hitokoto'] + u'"'
            return content


# 随机选择文库
def get_content(num=0):
    if not num:
        num = random.randint(0, 2)
    if num and num == 1:
        content = day_hitokoto()
    elif num and num == 2:
        content = day_iciba()
    else:
        content = day_hitokoto()
    log.info(u"获取到的文本信息：\n\r%s", content)
    return content + u'\n\r\t\t\t\t------小东东机器人[Grin]'


###############################
#  微信发送
###############################
def send_m(wind):
    # 以下为“CTRL+V”组合键,回车发送，（方法一）
    win32api.keybd_event(17, 0, 0, 0)  # 有效，按下CTRL
    time.sleep(1)  # 需要延时
    win32gui.SendMessage(wind, win32con.WM_KEYDOWN, 86, 0)  # V
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开CTRL
    time.sleep(1)  # 缓冲时间
    win32gui.SendMessage(wind, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 回车发送
    return


def ctrl_v(txt_str):
    # 定义文本信息,将信息缓存入剪贴板
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, txt_str)
    clipboard.CloseClipboard()
    return


def open_window(class_name, title_name):
    # FindWindow('WeCaht')
    # FindWindow('ChatWnd')
    wp = win32gui.FindWindow(class_name, title_name.decode('utf-8').encode('gbk'))

    # 使窗体最大化
    # win32gui.ShowWindow(win, win32con.SW_MAXIMIZE)
    # win = win32gui.FindWindow(className, titleName)
    # print("找到【%s】这个人句柄：%x" % (titleName, pHwnd))
    if wp != 0:
        left, top, right, bottom = win32gui.GetWindowRect(wp)
        print(left, top, right, bottom)  # 最小化为负数
        # 将窗口提到最前
        # 强行显示界面后才好截图
        win32gui.ShowWindow(wp, win32con.SW_RESTORE)
        # win32gui.ShowWindow(wp, win32con.SW_SHOWMINIMIZED)
        win32gui.SetForegroundWindow(wp)  # 获取控制
        time.sleep(0.5)
        log.debug(u"发送开始")
    else:
        log.error('请注意：找不到【%s】这个人（或群），请激活窗口！' % title_name)
    return wp


# 最小化窗口
def close_window(wp):
    time.sleep(0.5)
    win32gui.ShowWindow(wp, win32con.SW_MINIMIZE)
    log.debug(u"发送完成")


# ######################发送过程=================
def task(title_name):
    # 查找微信小窗口
    class_name = "ChatWnd"
    wp = open_window(class_name, title_name)
    if wp == 0:
        sys.exit(1)
    # 读取远程文本
    # print content
    ctrl_v(get_content())
    send_m(wp)
    close_window(wp)
    sys.stdout.flush()


def main():
    # 文件传输助手
    # 叶云云
    # title_name = '文件传输助手'
    title_name = '叶云云'
    scheduler = BlockingScheduler()
    # 马上执行
    scheduler.add_job(task, args=[title_name])
    # 1小时一次
    scheduler.add_job(task, 'interval', hours=1, args=[title_name])
    # 每天早上执行
    scheduler.add_job(task, 'cron', day_of_week='0-6', hour=7, minute=52, second=12,
                      misfire_grace_time=30, args=[title_name])
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
