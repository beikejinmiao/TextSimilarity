#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import gensim
import pickle
import pandas as pd
from conf.paths import RESOURCE_HOME, MODEL_HOME
from conf.paths import corpus_path, dictionary_path
from libs.segment import tokenizer
from model.tfidf import TF_IDF
from model.lsi import LSI
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)
original_csv = os.path.join(RESOURCE_HOME, "question_1k.csv")    # accountant_qa_dataset.csv
df_tokens_path = os.path.join(RESOURCE_HOME, "df_que_tokens.csv")


class IQAMode(object):
    def __init__(self, mode, tokenize=None):
        self.mode = mode
        logger.debug("running mode is: %s" % self.mode)
        self.tokenize = lambda x: tokenizer.cut(x, pregex=True) if tokenize is None else tokenize
        self.models = dict()

    def train(self):
        if not os.path.exists(MODEL_HOME):
            os.makedirs(MODEL_HOME)
        # load original data
        # df = pd.read_csv(df_tokens_path,header=None, names=["id", "question", "answer"])
        df = pd.read_csv(original_csv)
        logger.debug("load dataframe: '%s', size: %d" % (original_csv, df.shape[0]))
        df = df[["id", "question"]].drop_duplicates().reset_index(drop=True)
        logger.debug("after drop duplicates, size: %d" % df.shape[0])
        df["tokens"] = df["question"].map(lambda x: tokenizer.cut(x, pregex=True))

        # build dictionary/corpus
        dictionary = gensim.corpora.Dictionary(df["tokens"])
        corpus = [dictionary.doc2bow(tokens) for tokens in df["tokens"]]
        logger.debug("build dictionary and corpus. dictionary size: %d" % (len(dictionary.token2id)))

        # build model
        logger.debug("build tfidf model")
        self.models["tfidf"] = TF_IDF(dictionary, corpus, dataframe=df, tokenize=self.tokenize)
        logger.debug("build lsi model")
        self.models["lsi"] = LSI(dictionary, corpus, dataframe=df, tokenize=self.tokenize)
        if self.mode == "train":
            self.check_model("tfidf", "lsi")

        # dump df/dictionary/corpus
        logger.debug("dump dataframe to '%s'" % df_tokens_path)
        df["tokens"] = df["tokens"].map(lambda x: " ".join(x))
        df.to_csv(df_tokens_path)
        logger.debug("dump dictionary to '%s'" % dictionary_path)
        pickle.dump(dictionary, open(dictionary_path, "wb"))
        logger.debug("dump corpus to '%s'" % corpus_path)
        gensim.corpora.MmCorpus.serialize(corpus_path, corpus)
        #
        return df, dictionary, corpus

    @costime
    def test(self):
        if not os.path.exists(MODEL_HOME) or len(os.listdir(MODEL_HOME)) <= 0:
            df, dictionary, corpus = self.train()
        else:
            # load dataframe from csv
            logger.debug("load dataframe: '%s'" % df_tokens_path)
            df = pd.read_csv(df_tokens_path, index_col=0)
            df["tokens"] = df["tokens"].map(lambda x: str(x).split())
            # load dictionary/corpus
            logger.debug("load dictionary: '%s'" % dictionary_path)
            dictionary = pickle.load(open(dictionary_path, "rb"))
            logger.debug("load corpus: '%s'" % corpus_path)
            corpus = gensim.corpora.MmCorpus(corpus_path)
        # build model if it not existed
        if self.models.get("tfidf") is None:
            logger.debug("build tfidf model")
            self.models["tfidf"] = TF_IDF(dictionary, corpus, dataframe=df, tokenize=self.tokenize)
        if self.models.get("lsi") is None:
            logger.debug("build lsi model")
            self.models["lsi"] = LSI(dictionary, corpus, dataframe=df, tokenize=self.tokenize)
        self.check_model("tfidf", "lsi")

    def server(self):
        pass

    def check_model(self, *args):
        question = "KTV开发票明细能不能开服务费？"
        logger.debug(question)
        for name in args:
            model = self.models.get(name)
            logger.debug("%s %s %s" % ("="*20, name.upper(), "="*20))
            logger.debug(model.nearest(question) if model is not None else "None")


