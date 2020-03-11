#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gensim import models, similarities
from libs.segment import tokenizer
from libs.util import SortedDict
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class TF_IDF(object):
    def __init__(self, dictionary, corpus, dataframe=None, tokenize=None):
        self.dataframe = dataframe
        self.dictionary = dictionary
        self.corpus = corpus
        num_features = len(dictionary.token2id)
        self.model = models.TfidfModel(corpus)
        self.index = similarities.SparseMatrixSimilarity(self.model[corpus], num_features=num_features)
        self.tokenize = tokenizer.cut if tokenize is None else tokenize

    def query(self, text, topn=5, field="question"):
        if self.dataframe is None:
            logger.error("please load the csv data firstly.")
            return

        results = list()
        text_bow = self.dictionary.doc2bow(self.tokenize(text))
        sims = self.index[self.model[text_bow]]
        sorted_sims = SortedDict.to_list(dict(enumerate(sims)))
        for ix, prob in sorted_sims[0:topn]:
            # ix: document_number
            results.append((self.dataframe.iloc[ix][field], prob))
        return results

    def dump(self):
        pass

