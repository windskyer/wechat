# -*- coding: UTF-8 -*-

import logging
import requests
from random import choice

log = logging.getLogger('apscheduler.executors.default')


# 获取一言文库
def day_hitokoto():
    maps = {'a': u'动画', 'b': u'漫画', 'c': u'游戏', 'd': u'文学', 'e': u'原创', 'f': u'来自网络', 'g': u'其他', 'h': u'影视',
            'i': u'诗词', 'j': u'网易云', 'k': u'哲学', '  l': u'抖机灵'}
    mi = choice(maps.keys())
    # 一言 ：https://hitokoto.cn/
    url = "https://v1.hitokoto.cn/?c=%s&encode=json" % mi
    r = requests.get(url)
    content = maps[mi] + u':\n\r"' + r.json()['hitokoto'] + u'"'
    return content


def get_content():
    log.debug("获取双语文本地址：https://v1.hitokoto.cn")
    return day_hitokoto()
