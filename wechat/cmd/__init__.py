# -*- coding: UTF-8 -*-

import logging
import sys

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.DEBUG)  # DEBUG
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
han = logging.StreamHandler(sys.stdout)
han.setFormatter(fmt)
log.addHandler(han)
