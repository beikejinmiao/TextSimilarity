#!/usr/bin/env python
# -*- coding:utf-8 -*-
import multiprocessing

cpu_count = multiprocessing.cpu_count()
all_models = ["tfidf", "lsi", "word2vec", "doc2vec"]
web_host = "127.0.0.1"
web_port = 8080

