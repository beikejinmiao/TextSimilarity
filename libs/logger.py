#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import json
import logging
import logging.config
from conf.paths import WORK_NAME, MAIN_HOME, LOGGING_CFG_FILE
LOGGING_CFG = json.load(open(LOGGING_CFG_FILE))
filename = LOGGING_CFG["handlers"]["file"]["filename"]
LOGGING_CFG["handlers"]["file"]["filename"] = os.path.join(MAIN_HOME, filename)


def get_logger(_file_=None, logger=None, level=None):
    """
    Build and return the logger.
    :param _file_:  the file name of python script(like: __file__)
    :param logger:  the specified logger name that defined in `logging.yaml`
    :param level:   logging level
    :return:
    """
    if logger is None:
        _name = _logger_name(_file_=_file_)
    else:
        _name = logger
    _logger = logging.getLogger(_name)
    logging.config.dictConfig(LOGGING_CFG)

    # used by some script separately
    if level is not None:
        _logger.setLevel(level)
        _logger.propagate = 1
        if _logger.parent:
            _logger.parent.setLevel(level)
            _logger.parent.propagate = 1

    return _logger


def _logger_name(_file_=None):
    """
    get logger name from "__file__" for separate file
    :param _file_:
    :return: the logger name for separate file
    """
    _name = WORK_NAME
    if _file_:
        file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(_file_), os.path.pardir)), _file_)
        _name = re.sub("\.py[c]?$", "", file_path.replace(MAIN_HOME, WORK_NAME)).replace(os.path.sep, ".")
    if not _name.startswith(WORK_NAME):
        _name = WORK_NAME
    return _name


