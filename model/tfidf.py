#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from gensim import models, similarities
from conf.paths import MODEL_HOME
from libs.util import SortedDict
from model.base import SimBaseModel
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class TF_IDF(SimBaseModel):
    model_path = os.path.join(MODEL_HOME, "tfidf.m")
    index_path = os.path.join(MODEL_HOME, "tfidf.index")

    def __init__(self, dictionary, corpus, dataframe=None, load=False):
        super(TF_IDF, self).__init__(name="tfidf", dataframe=dataframe)
        self.dictionary = dictionary
        self.corpus = corpus
        self.index = None
        self.build(load=load)

    @costime("tfidf", msg="model query nearest")
    def nearest(self, text, topn=5, score=False):
        if not self._ready_df_model():
            return None

        results = list()
        text_bow = self.dictionary.doc2bow(self._to_tokens(text))
        sims = self.index[self.model[text_bow]]
        sorted_sims = SortedDict.to_list(dict(enumerate(sims)))
        for ix, prob in sorted_sims[0:topn]:
            # ix: document_number
            row = self.dataframe.iloc[ix]
            rlt = self._query_rlt(row, prob)
            if score is True:
                que, tok = row["question"], row["tokens"]
                rlt["score"] = self._score(text, que, None, None)
            results.append(rlt)
        return results

    def build(self, load=False):
        if load is True and os.path.exists(TF_IDF.model_path) and os.path.exists(TF_IDF.index_path):
            self.model = models.TfidfModel.load(TF_IDF.model_path)
            self.index = similarities.MatrixSimilarity.load(TF_IDF.index_path)
        else:
            self.model = models.TfidfModel(self.corpus)
            self.index = similarities.SparseMatrixSimilarity(self.model[self.corpus],
                                                             num_features=len(self.dictionary.token2id))
        logger.debug("build model '%s' successfully" % self.name)

    def dump(self):
        self.model.save(TF_IDF.model_path)
        self.index.save(TF_IDF.index_path)


