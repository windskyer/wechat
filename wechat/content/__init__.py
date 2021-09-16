# -*- coding: UTF-8 -*-

import random
import logging
from wechat.content import hitokoto
from wechat.content import iciba

log = logging.getLogger('apscheduler.executors.default')


# 随机选择文库
def get_content(num=0):
    if not num:
        num = random.randint(0, 2)
    if num and num == 1:
        content = hitokoto.get_content()
    elif num and num == 2:
        content = iciba.get_content()
    else:
        content = hitokoto.get_content()
    log.info(u"获取到的文本信息：\n\r%s", content)
    return content + u'\n\r\t\t\t\t------小东东机器人[Grin]'
