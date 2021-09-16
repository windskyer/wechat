# -*- coding: UTF-8 -*-

from __future__ import print_function
from wechat.wx import cron
import argparse

"""wx auto chat"""

Version = "v1.0.0"
Name = "文件传输助手"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wechat for argparse')
    parser.add_argument('--name', '-n', help='好友名称，必要参数', required=True)
    args = parser.parse_args()
    cron.start(args.name)
