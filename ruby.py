#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A python script to segment chinese phrases and attach pinyin rubys. It can be
# used to produce ruby-annotated phrases for use in html5 documents.
#

import jieba
from pypinyin import pinyin


def pinyin_for_word(word):
    return "".join(v[0] for v in pinyin(word))


def pinyin_for_phrase(phrase):
    # Segment the phrase into its constituent words.
    words = [word for word in jieba.cut(phrase)]

    pinyin_words = [pinyin_for_word(word) for word in words]

    # Exclude punctuation from the pinyin representation.
    pinyin_words = [x if (x != u'。') else u'' for x in pinyin_words]

    return zip(words, pinyin_words)


def print_rubys(phrase):
    pinyin = pinyin_for_phrase(phrase)

    elements = map(lambda x: "<rb>%s</rb><rt>%s</rt>" % x, pinyin)

    return "<ruby>" + "".join(elements) + "</ruby>"
