# -*- coding: UTF-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from wechat.wx import wind
from wechat.wx import send
from wechat import content
import sys


def task(title_name):
    # 查找微信小窗口
    wp = wind.open_window(title_name)
    if wp == 0:
        sys.exit(1)
    # 读取远程文本
    send.ctrl_v(content.get_content())
    send.send_m(wp)
    wind.close_window(wp)
    sys.stdout.flush()


def start(title_name):
    # 文件传输助手
    # 叶云云
    # title_name = '文件传输助手'
    # title_name = '叶云云'
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
