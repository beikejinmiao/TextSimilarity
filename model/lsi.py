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


class LSI(SimBaseModel):
    model_path = os.path.join(MODEL_HOME, "lsi.m")
    index_path = os.path.join(MODEL_HOME, "lsi.index")

    def __init__(self, dictionary, corpus, dataframe=None, num_topics=200, load=False):
        super(LSI, self).__init__(name="lsi", dataframe=dataframe)
        self.dictionary = dictionary
        self.corpus = corpus
        self.index = None
        self.num_topics = num_topics
        self.build(load=load)

    @costime("lsi", msg="model query nearest")
    def nearest(self, text, topn=5, score=False):
        if not self._ready_df_model():
            return None

        results = list()
        text_bow = self.dictionary.doc2bow(self._to_tokens(text))
        doc = self.model[text_bow]
        sims = self.index[doc]
        sorted_sims = SortedDict.to_list(dict(enumerate(sims)))
        for ix, prob in sorted_sims[0:topn]:
            # ix: document_number
            row = self.dataframe.iloc[ix]
            rlt = self._query_rlt(row, prob)
            if score is True:
                que, tok = row["question"], row["tokens"]
                rlt["score"] = self._score(text, que, self._vector(doc), self._vector(self.model[self.dictionary.doc2bow(tok)]))
            results.append(rlt)
        return results

    def _vector(self, doc):
        return [vec for i, vec in doc]

    def build(self, load=False):
        if load is True and os.path.exists(LSI.model_path) and os.path.exists(LSI.index_path):
            self.model = models.LsiModel.load(LSI.model_path)
            self.index = similarities.MatrixSimilarity.load(LSI.index_path)
        else:
            self.model = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.model[self.corpus])
        logger.debug("build model '%s' successfully" % self.name)

    def dump(self):
        self.model.save(LSI.model_path)
        self.index.save(LSI.index_path)

