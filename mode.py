#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import gensim
import pickle
import pandas as pd
from conf.paths import MODEL_HOME, RESOURCE_HOME
from conf.paths import corpus_path, dictionary_path, df_tokens_path
from conf.config import all_models
from libs.segment import tokenizer
from model.tfidf import TF_IDF
from model.lsi import LSI
from model.word2vec import Word2Vector
from model.doc2vec import Doc2Vector
from libs.wrapper import costime
from libs.logger import get_logger

logger = get_logger(_file_=__file__)
original_csv = os.path.join(RESOURCE_HOME, "accountant_qa_dataset.csv")    #


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
        df = pd.read_csv(original_csv, header=None, names=["id", "question", "answer"])
        # df = pd.read_csv(original_csv)
        logger.debug("load dataframe: '%s', size: %d" % (original_csv, df.shape[0]))
        df = df[["id", "question"]].drop_duplicates().reset_index(drop=True)
        logger.debug("after drop duplicates, size: %d" % df.shape[0])
        df["tokens"] = df["question"].map(lambda x: tokenizer.cut(x, pregex=True))

        # build dictionary/corpus
        dictionary = gensim.corpora.Dictionary(df["tokens"])
        corpus = [dictionary.doc2bow(tokens) for tokens in df["tokens"]]
        logger.debug("build dictionary and corpus. dictionary size: %d" % (len(dictionary.token2id)))

        # build models
        self.models = build_models(df, dictionary, corpus, model="all")
        if self.mode == "train":
            self.check_model(*all_models)
        # dump df/dictionary/corpus/models
        dump(dictionary=dictionary, corpus=corpus, dataframe=df, models=self.models)
        #
        return df, dictionary, corpus

    @costime("test mode", msg="running total")
    def test(self):
        if not os.path.exists(MODEL_HOME) or len(os.listdir(MODEL_HOME)) <= 0:
            df, dictionary, corpus = self.train()
        else:
            df, dictionary, corpus = load_corpus()
            # build model if it not existed
        if len(self.models) == 0:
            self.models = build_models(df, dictionary, corpus, model="all", load=True)
        self.check_model(*all_models)

    def check_model(self, *args):
        question = "KTV开发票明细能不能开服务费？"
        que_tokens = tokenizer.cut(question)
        logger.debug(question)
        logger.debug(" ".join(que_tokens))
        for name in args:
            model = self.models.get(name)
            logger.debug("%s %s %s" % ("="*20, name.upper(), "="*20))
            logger.debug(model.nearest(que_tokens) if model is not None else "None")


def _check_model_name(mod_names):
    _model = set()
    mod_names = [mod_names, ] if isinstance(mod_names, str) else list(mod_names)
    for name in mod_names:
        if name == "all":
            return all_models
        if name not in all_models:
            logger.info("'%s' model not existed" % name)
        else:
            _model.add(name)
    return list(_model)


def load_corpus():
    # load dataframe from csv
    logger.debug("load dataframe: '%s'" % df_tokens_path)
    df = pd.read_csv(df_tokens_path, index_col=0)
    df["tokens"] = df["tokens"].map(lambda x: str(x).split())
    # load dictionary/corpus
    logger.debug("load dictionary: '%s'" % dictionary_path)
    with open(dictionary_path, "rb") as fopen:
        dictionary = pickle.load(fopen)
    logger.debug("load corpus: '%s'" % corpus_path)
    corpus = gensim.corpora.MmCorpus(corpus_path)
    return df, dictionary, corpus


def build_models(dataframe, dictionary, corpus, model="all", load=False):
    models = dict()
    model_names = _check_model_name(model)
    for name in model_names:
        if name == "tfidf":
            models[name] = TF_IDF(dictionary, corpus, dataframe=dataframe, load=load)
        elif name == "lsi":
            models[name] = LSI(dictionary, corpus, dataframe=dataframe, load=load)
        elif name == "word2vec":
            models[name] = Word2Vector(dataframe=dataframe, load=load)
        elif name == "doc2vec":
            models[name] = Doc2Vector(dataframe=dataframe, load=load)
    return models


def dump(dictionary=None, corpus=None, dataframe=None, models=None):
    if dictionary is not None:
        logger.debug("dump dictionary to '%s'" % dictionary_path)
        with open(dictionary_path, "wb") as fopen:
            pickle.dump(dictionary, fopen)
    if corpus is not None:
        logger.debug("dump corpus to '%s'" % corpus_path)
        gensim.corpora.MmCorpus.serialize(corpus_path, corpus)
    if dataframe is not None:
        logger.debug("write dataframe to '%s'" % df_tokens_path)
        dataframe["tokens"] = dataframe["tokens"].map(lambda x: " ".join(x))
        dataframe.to_csv(df_tokens_path)
    if models is not None:
        for name in models:
            if models.get(name) is not None:
                models[name].dump()

