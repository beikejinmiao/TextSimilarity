#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from conf.paths import stopaths, lexiconpaths
from libs.util import reader
from libs.singleton import Singleton
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class AttrDict(object):
    def __init__(self, init=None):
        if init is not None:
            self.__dict__.update(init)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __iter__(self):
        for key in self.__dict__:
            yield key


class Lexicon(AttrDict):
    __metaclass__ = Singleton

    def __init__(self):
        super(Lexicon, self).__init__()
        self.accountant = reader(lexiconpaths["accountant"])
        self.finance = reader(lexiconpaths["finance"])
        self.self = reader(lexiconpaths["self"])
        logger.debug("load lexicon '%s' successfully" %
                     ",".join([os.path.basename(path) for path in lexiconpaths.values()]))


class StopWords(AttrDict):
    __metaclass__ = Singleton

    def __init__(self):
        super(StopWords, self).__init__()
        self.cn = reader(stopaths["cn"])
        self.hit = reader(stopaths["hit"])
        self.baidu = reader(stopaths["baidu"])
        self.scu = reader(stopaths["scu"])
        self.july = reader(stopaths["july"])
        self.self = reader(stopaths["self"])
        logger.debug("load stop_words '%s' successfully" %
                     ",".join([os.path.basename(path) for path in stopaths.values()]))


# init stop_words and lexicon when needed rather than import python
# lexicon = Lexicon()
# stopwords = StopWords()

