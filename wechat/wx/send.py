# -*- coding: UTF-8 -*-
import win32api
import win32gui
import win32con
import win32clipboard as clipboard
import logging
import time

log = logging.getLogger('apscheduler.executors.default')


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
