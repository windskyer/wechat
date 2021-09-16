# -*- coding: UTF-8 -*-

from __future__ import print_function
from wechat.wx import cron

"""wx auto chat"""

Version = "v1.0.0"
Name = "文件传输助手"

if __name__ == '__main__':
    cron.start(Name)
