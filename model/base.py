#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.segment import tokenizer
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class SimBaseModel(object):
    def __init__(self, name="", dataframe=None, tokenize=None):
        self.name = name  # model name
        self.dataframe = dataframe
        self.model = None
        self.tokenize = tokenizer.cut if tokenize is None else tokenize

    def _ready_df_model(self):
        if self.dataframe is None or self.model is None:
            logger.error("please load the csv data and train model firstly.")
            return False
        return True

    def _tokens(self, text):
        tokens = text
        if isinstance(text, str):
            tokens = self.tokenize(text)
        return tokens

    @staticmethod
    def _json_rlt(text, similarity, tokens=None):
        rlt = {"text": text, "similarity": str(round(similarity, 4))}
        if tokens:
            rlt["tokens"] = tokens if isinstance(tokens, str) else " ".join(tokens)
        return rlt

    @costime("sim", msg="query nearest")
    def nearest(self, text, topn=5, field="question"):
        if not self._ready_df_model():
            return None
        return []

    def build(self, load=False):
        pass

    def dump(self):
        pass

