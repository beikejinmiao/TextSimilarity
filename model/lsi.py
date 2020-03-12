#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gensim import models, similarities
from libs.segment import tokenizer
from libs.util import SortedDict
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class LSI(object):
    def __init__(self, dictionary, corpus, dataframe=None, tokenize=None, topic=200):
        self.dataframe = dataframe
        self.dictionary = dictionary
        self.corpus = corpus
        self.model = models.LsiModel(corpus, id2word=dictionary, num_topics=topic)
        self.index = similarities.MatrixSimilarity(self.model[corpus])
        self.tokenize = tokenizer.cut if tokenize is None else tokenize

    def nearest(self, text, topn=5, field="question"):
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


