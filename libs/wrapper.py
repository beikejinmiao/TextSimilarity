#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import traceback
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


def costime(func):
    def wrapper(*args, **kwargs):
        startime = time.time()
        try:
            return func(*args, **kwargs)
        except:
            logger.error(traceback.format_exc())
            return None
        finally:
            logger.debug("Cost time: %.2fs" % (time.time() - startime))
    return wrapper

