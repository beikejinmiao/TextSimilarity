#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import traceback
from functools import wraps
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


def costime(name, msg=""):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            startime = time.time()
            try:
                return func(*args, **kwargs)
            except:
                logger.error(traceback.format_exc())
                return None
            finally:
                logger.debug("%s%s cost time: %.2fs" % (name, " "+msg if msg else msg, time.time() - startime))
        return wrapper
    return decorate
