#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

MAIN_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # 返回项目根目录
WORK_NAME = MAIN_HOME.split(os.path.sep)[-1].lower()  # iqa

RESOURCE_HOME = os.path.join(MAIN_HOME, "resources")
MODEL_HOME = os.path.join(RESOURCE_HOME, "model")
LOGGING_CFG_FILE = os.path.join(MAIN_HOME, "conf", "logger.json")


stopws_home = os.path.join(RESOURCE_HOME, "stopwords")
stopaths = {
    "cn": os.path.join(stopws_home, "cn_stopwords.txt"),
    "hit": os.path.join(stopws_home, "hit_stopwords.txt"),
    "baidu": os.path.join(stopws_home, "baidu_stopwords.txt"),
    "scu": os.path.join(stopws_home, "scu_stopwords.txt"),
    "july": os.path.join(stopws_home, "july_stopwords.txt"),
    "self": os.path.join(stopws_home, "self_stopwords.txt")
}


lexicon_home = os.path.join(RESOURCE_HOME, "lexicon")
lexiconpaths = {
    "accountant": os.path.join(lexicon_home, "accountant.txt"),
    "finance": os.path.join(lexicon_home, "finance.txt"),
    "self": os.path.join(lexicon_home, "self_lexicon.txt")
}



