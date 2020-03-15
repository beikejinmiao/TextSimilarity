#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from conf.paths import MODEL_HOME
from conf.config import cpu_count
from model.base import SimBaseModel
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)


class Doc2Vector(SimBaseModel):
    # https://radimrehurek.com/gensim/models/doc2vec.html#usage-examples
    model_path = os.path.join(MODEL_HOME, "doc2vec.m")

    def __init__(self, dataframe=None, load=False):
        super(Doc2Vector, self).__init__(name="doc2vec", dataframe=dataframe)
        # 暂不dump/load corpus, dataframe索引必须保持不变
        self.corpus = [TaggedDocument(doc, [i]) for i, doc in enumerate(self.dataframe["tokens"])]
        self.build(load=load)

    @costime("doc2vec", msg="model query nearest")
    def nearest(self, text, topn=5, field="question"):
        if not self._ready_df_model():
            return None

        results = list()
        inferred_vector = self.model.infer_vector(self._tokens(text))
        sorted_sims = self.model.docvecs.most_similar([inferred_vector], topn=topn)
        for ix, prob in sorted_sims:
            # ix: document_number
            results.append((self.dataframe.iloc[ix][field], prob))
        return results

    def build(self, load=False):
        if load is True and os.path.exists(Doc2Vector.model_path):
            self.model = Doc2Vec.load(Doc2Vector.model_path)
        else:
            self.model = Doc2Vec(vector_size=100, min_count=2, epochs=1000, workers=cpu_count)
            self.model.build_vocab(documents=self.corpus)
            self.model.train(documents=self.corpus, total_examples=self.model.corpus_count, epochs=self.model.epochs)
            # after finished training a model (=no more updates, only querying, reduce memory usage)
            self.model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
        logger.debug("build model '%s' successfully" % self.name)

    def dump(self):
        self.model.save(Doc2Vector.model_path)
