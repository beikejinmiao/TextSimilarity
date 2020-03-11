#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import OrderedDict
from scipy import spatial
from nltk.translate.bleu_score import sentence_bleu


gram_weights = OrderedDict()
gram_weights["1-gram"] = (1, 0, 0, 0)
gram_weights["2-gram"] = (0.5, 0.5, 0, 0)
gram_weights["3-gram"] = (0.33, 0.33, 0.33, 0)
gram_weights["4-gram"] = (0.25, 0.25, 0.25, 0.25)


def bleu(reference, candidate):
    # https://cloud.tencent.com/developer/article/1042161
    # https://www.cnblogs.com/by-dream/p/7679284.html
    if not isinstance(reference, (list, tuple)):
        reference = [[x for x in reference]]
    if not isinstance(candidate, (list, tuple)):
        candidate = [x for x in candidate]

    return [sentence_bleu(reference, candidate, weights=w) for w in gram_weights.values()]


def bleuprint(reference, candidate):
    scores = bleu(reference, candidate)
    print("N-gram BLEU between \n  %s\n  %s" % (reference, candidate))
    print('1-gram: %f' % scores[0])
    print('2-gram: %f' % scores[1])
    print('3-gram: %f' % scores[2])
    print('4-gram: %f' % scores[3])


def cosine(x, y):
    """
    the cosine distance of x,y
    :param x:
    :param y:
    :return:
    """
    return 1 - spatial.distance.cosine(x, y)

