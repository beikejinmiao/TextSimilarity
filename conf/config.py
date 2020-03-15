#!/usr/bin/env python
# -*- coding:utf-8 -*-
import multiprocessing

cpu_count = multiprocessing.cpu_count()
all_models = ["tfidf", "lsi", "word2vec", "doc2vec"]

