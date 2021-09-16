import datetime
import time
from random import randint
import logging
import requests

log = logging.getLogger('apscheduler.executors.default')


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


def get_content():
    log.debug("获取双语文本地址：http://sentence.iciba.com")
    return day_iciba()
