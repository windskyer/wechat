# -*- coding: UTF-8 -*-
import win32gui
import win32con
import logging
import time

log = logging.getLogger('apscheduler.executors.default')


def open_window(class_name, title_name):
    # FindWindow('WeCaht')
    # FindWindow('ChatWnd')
    wind = win32gui.FindWindow(class_name, title_name.decode('utf-8').encode('gbk'))

    # 使窗体最大化
    # win32gui.ShowWindow(win, win32con.SW_MAXIMIZE)
    # win = win32gui.FindWindow(className, titleName)
    # print("找到【%s】这个人句柄：%x" % (titleName, pHwnd))
    if wind != 0:
        left, top, right, bottom = win32gui.GetWindowRect(wind)
        print(left, top, right, bottom)  # 最小化为负数
        # 强行显示界面后才好截图
        win32gui.ShowWindow(wind, win32con.SW_RESTORE)
        # win32gui.ShowWindow(pHwnd, win32con.SW_SHOWMINIMIZED)
        # 将窗口提到最前
        win32gui.SetForegroundWindow(wind)  # 获取控制
        time.sleep(0.5)
        log.debug(u"发送开始")
    else:
        log.error('请注意：找不到【%s】这个人（或群），请激活窗口！' % title_name)
    return wind


# 最小化窗口
def close_window(wind):
    time.sleep(0.5)
    win32gui.ShowWindow(wind, win32con.SW_MINIMIZE)
    log.debug(u"发送完成")
