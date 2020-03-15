#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle
import numpy as np
from gensim.models.word2vec import Word2Vec
from sklearn.neighbors import KDTree
from conf.paths import MODEL_HOME
from conf.config import cpu_count
from model.base import SimBaseModel
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class Word2Vector(SimBaseModel):
    model_path = os.path.join(MODEL_HOME, "word2vec.m")
    kdtree_path = os.path.join(MODEL_HOME, "word2vec_kdtree.pkl")

    def __init__(self, dataframe=None, load=False):
        super(Word2Vector, self).__init__(name="word2vec", dataframe=dataframe)
        self.kdtree = None
        self.build(load=load)

    def avg_doc_vector(self, tokens):
        # function to average all words vectors in a given paragraph
        doc_vec = np.zeros((self.model.wv.vector_size,), dtype='float32')
        n_words = 0
        for word in tokens:
            if word in self.model.wv:
                n_words += 1
                doc_vec = np.add(doc_vec, self.model.wv[word])
        if n_words > 0:
            doc_vec = np.divide(doc_vec, n_words)
        return doc_vec.tolist()

    def _kd_tree(self):
        X = list()
        for tokens in self.dataframe["tokens"]:
            X.append(self.avg_doc_vector(tokens))
        return KDTree(np.array(X), leaf_size=50)

    @costime("word2vec", msg="model query nearest")
    def nearest(self, text, topn=5, field="question"):
        if self.dataframe is None or self.model is None or self.kdtree is None:
            logger.error("please load the csv data and train model firstly.")
            return False

        results = list()
        dists, indices = self.kdtree.query(np.array(self.avg_doc_vector(self._tokens(text))).reshape(1, -1), k=topn)
        dist_sum = np.sum(dists)
        for i, dist in enumerate(dists[0]):
            # ix: document_number
            ix = indices[0][i]
            row = self.dataframe.iloc[ix]
            results.append(self._json_rlt(row[field], 1-dist/dist_sum, tokens=row["tokens"]))
        return results

    def build(self, load=False):
        if load is True and os.path.exists(Word2Vector.model_path) and os.path.exists(Word2Vector.kdtree_path):
            self.model = Word2Vec.load(Word2Vector.model_path)
            with open(Word2Vector.kdtree_path, "rb") as pkl_file:
                self.kdtree = pickle.load(pkl_file)
        else:
            self.model = Word2Vec(sentences=self.dataframe["tokens"], min_count=2, iter=1000, workers=cpu_count)
            self.kdtree = self._kd_tree()
        logger.debug("build model '%s' successfully" % self.name)

    def dump(self):
        self.model.save(Word2Vector.model_path)
        with open(Word2Vector.kdtree_path, "wb") as pkl_file:
            pickle.dump(self.kdtree, pkl_file)
