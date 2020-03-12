#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import jieba
from libs.resource import stopwords, lexicon
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

    def __init__(self, stopws="hit", lexn=None):
        """
        tokenize the text based on 'jieba'
        :param lexn:
        :param stopws:
        """
        self.stop_words = stopwords[stopws]
        self.self_stop_words = stopwords["self"]
        self.add_lexicon(lexn=lexn)

    def add_words(self, words):
        if isinstance(words, (list, tuple, set)):
            for word in words:
                jieba.add_word(word)
        else:
            jieba.add_word(words)

    def add_lexicon(self, lexn=None):
        if lexn == "all":
            for x in lexicon:
                self.add_words(lexicon[x])
        elif lexn in lexicon:
            self.add_words(lexicon[lexn])

    def cut(self, text, pregex=False, stopws=True, self_stopws=True):
        """
        tokenize by 'jieba'
        :param text:
        :param pregex: if true, replace by regex that defined firstly
        :param stopws: if true, filter the word that in stop words
        :param self_stopws: if true, filter the word that in self stop words
        :return:
        """
        text = str(text).lower()
        if pregex is True:
            text = regex_change(text)
        words = jieba.lcut(text)    # 精确模式,返回list
        if stopws is True:
            words = [word for word in words if len(word.strip()) > 0 and word not in self.stop_words]
        if self_stopws is True:
            words = [word for word in words if word not in self.self_stop_words]
        return words


tokenizer = JieBa(stopws="hit", lexn="all")
