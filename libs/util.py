#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import OrderedDict


class SortedDict(object):
    @staticmethod
    def to_orderd(d, reverse=True):
        return OrderedDict(sorted(d.items(), key=lambda d: d[1], reverse=reverse))

    @staticmethod
    def to_list(d, reverse=True):
        return sorted(d.items(), key=lambda d: d[1], reverse=reverse)


def reader(path, strip="\r\n ", skip_blank=True):
    lines = []
    with open(path, "r", encoding="utf-8") as fopen:
        while True:
            line = fopen.readline()
            if not line:
                break
            line = line.strip(strip)
            # check the line whether is blank or not
            if skip_blank and not line:
                continue
            lines.append(line)
    return lines



