#!/usr/bin/env python
# -*- coding:utf-8 -*-
from libs.segment import tokenizer
from libs.wrapper import costime
from libs.logger import get_logger
from libs.score import bleu, cosine

logger = get_logger(_file_=__file__)


class SimBaseModel(object):
    def __init__(self, name="", dataframe=None, tokenize=None):
        self.name = name  # model name
        self.dataframe = dataframe
        self.model = None
        self.tokenize = tokenizer.cut if tokenize is None else tokenize
        self._print_tokens = True           # if true, return the tokens when nearest query

    def _ready_df_model(self):
        if self.dataframe is None or self.model is None:
            logger.error("please load the csv data and train model firstly.")
            return False
        return True

    def _to_tokens(self, text):
        tokens = text
        if isinstance(text, str):
            tokens = self.tokenize(text)
        return tokens

    @costime("sim", msg="query nearest")
    def nearest(self, text, topn=5, score=False):
        if not self._ready_df_model():
            return None
        return []

    def _query_rlt(self, row, similarity):
        rlt = {"text": row["question"], "similarity": str(round(similarity, 4))}
        if self._print_tokens:
            rlt["tokens"] = " ".join(row["tokens"])
        return rlt

    @staticmethod
    def _score(text1, text2, vec1, vec2):
        _bleu_ = bleu(text1, text2)[0]
        similarity = 0.0
        if vec1 is not None and vec2 is not None:
            similarity = cosine(vec1, vec2)
        return {"bleu": "%.4f" % _bleu_, "cosine": "%.4f" % similarity, "score": "%.4f" % (_bleu_+similarity)}

    def build(self, load=False):
        pass

    def dump(self):
        pass

