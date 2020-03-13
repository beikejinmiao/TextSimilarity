#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import jieba
# from libs.resource import stopwords, lexicon
from libs.resource import StopWords, Lexicon
from libs.singleton import Singleton

url_regex = re.compile(r'(http|https)://[a-zA-Z0-9_\.@&/#!#\?]+', re.VERBOSE | re.IGNORECASE)
date_regex = re.compile(u"""
        \d+年[度]? |
        \d+月[份]? |
        \d+[日|号] |
        [上下这本]?周[一二三四五六日]
    """, re.VERBOSE)


def regex_change(text):
    # 替换ASCII控制字符
    text = re.sub(r'[\x00-\x1F\x7f]+', ' ', text)
    # 将整形数格式化为0
    text = re.sub("\d+", "0", text)
    # 将 1.2.3 格式的数据替换为0. 常见于版本,IP
    text = re.sub("(\d+\.)+\d+", "0", text)
    # 删除日期
    text = date_regex.sub(r"", text)
    # 删除URL
    text = url_regex.sub(r"", text)
    # 换行符/tab/多个空格  --> single space
    text = re.sub("\s+", " ", text)
    return text


class JieBa(object):
    __metaclass__ = Singleton

    def __init__(self, stopws_type="hit", lexn_type=None):
        """
        tokenize the text based on 'jieba'
        :param stopws:
        :param lexn_type:
        """
        self.stopws_type = stopws_type
        self.lexn_type = lexn_type
        self.stop_words = None
        self.lexicon = None
        self._is_add_lexn = False          # for load the lexicon lazily

    def add_words(self, words):
        if isinstance(words, (list, tuple, set)):
            for word in words:
                jieba.add_word(word)
        else:
            jieba.add_word(words)

    def add_lexicon(self, lexn_type=None):
        self._is_add_lexn = True
        if self.lexicon is None:
            self.lexicon = Lexicon()

        if lexn_type == "all":
            for x in self.lexicon:
                self.add_words(self.lexicon[x])
        elif lexn_type in self.lexicon:
            self.add_words(self.lexicon[lexn_type])

    def cut(self, text, pregex=False, stopws=True, self_stopws=True):
        """
        tokenize by 'jieba'
        :param text:
        :param pregex: if true, replace by regex that defined firstly
        :param stopws: if true, filter the word that in stop words
        :param self_stopws: if true, filter the word that in self stop words
        :return:
        """
        # load stop_words and lexicon when needed
        if self.lexn_type and self._is_add_lexn is False:
            self.add_lexicon(lexn_type=self.lexn_type)
        if (stopws is True or self_stopws is True) and self.stop_words is None:
            self.stop_words = StopWords()
        #
        text = str(text).lower()
        if pregex is True:
            text = regex_change(text)
        words = jieba.lcut(text)    # 精确模式,返回list
        if stopws is True:
            words = [word for word in words if len(word.strip()) > 0 and word not in self.stop_words[self.stopws_type]]
        if self_stopws is True:
            words = [word for word in words if word not in self.stop_words["self"]]
        return words


tokenizer = JieBa(stopws_type="hit", lexn_type="all")


