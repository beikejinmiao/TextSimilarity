#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import gensim
import pandas as pd
from config import RESOURCE_HOME
from libs.segment import tokenizer
from model.tfidf import TF_IDF


MODE = "train"


if MODE == "train":

    # df = pd.read_csv(os.path.join(RESOURCE_HOME, "accountant_qa_dataset.csv"),
    #                  header=None, names=["id", "question", "answer"])
    df = pd.read_csv(os.path.join(RESOURCE_HOME, "question_1k.csv"))
    df = df[["id", "question"]].drop_duplicates().reset_index(drop=True)
    df["tokens"] = df["question"].map(lambda x: tokenizer.cut(x, pregex=True))
    # #save to csv
    # df["tokens"] = df["tokens"].map(lambda x: " ".join(x))
    # df.to_csv(os.path.join(RESOURCE_HOME, "df_que_tokens.csv"))
    # #load from csv
    # df = pd.read_csv(os.path.join(RESOURCE_HOME, "df_que_tokens.csv"), index_col=0)
    # df["tokens"] = df["tokens"].map(lambda x: str(x).split())

    #
    dictionary = gensim.corpora.Dictionary(df["tokens"])
    corpus = [dictionary.doc2bow(tokens) for tokens in df["tokens"]]
    #
    tfidf = TF_IDF(dictionary, corpus, dataframe=df, tokenize=tokenizer.cut)
    question = "KTV开发票明细能不能开服务费？"
    print(question)
    print(tfidf.query(question))

elif MODE == "test":
    pass

elif MODE == "server":
    pass
