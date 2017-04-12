#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A python script to segment chinese phrases and attach pinyin rubys. It can be
# used to produce ruby-annotated phrases for use in html5 documents.
#

import re
import jieba
from pypinyin import pinyin

matcher = re.compile(u'(\S+) (\S+) \[([^\]]+)\] /(.*)/')

def parse_dictionary_line(line):
    m = matcher.match(line)
    return (m.group(1), m.group(4).split('/'))

# Download dictionary from https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz
def read_dictionary():
    f = open("cedict_1_0_ts_utf-8_mdbg.txt", "r")

    # A map of character -> english meaning
    entries = {}

    lines = f.readlines()
    for line in lines:
        line = line.decode("utf-8")

        # Skip comments.
        if line.startswith(("#")):
            continue

        character, meaning = parse_dictionary_line(line)
        entries[character] = meaning
    return entries


def pinyin_for_word(word):
    return "".join(v[0] for v in pinyin(word))


def pinyin_for_phrase(phrase):
    # Segment the phrase into its constituent words.
    words = [word for word in jieba.cut(phrase, HMM=False)]

    pinyin_words = [pinyin_for_word(word) for word in words]

    # Exclude punctuation from the pinyin representation.
    pinyin_words = [x if (x != u'。') else u'' for x in pinyin_words]

    return zip(words, pinyin_words)


def print_ruby(x):
    character, pinyin = x
    return u'<rb>%s</rb><rt>%s</rt>' % (character, pinyin)


def print_ruby_with_english(x, dictionary):
    character, pinyin = x
    meaning = dictionary.get(character, [u''])[0]
    return u'<rb><ruby>%s</ruby></rb><rt class=eng>%s</rt>' % (print_ruby(x), meaning)


def print_rubys(phrase, dictionary=None):
    pinyin = pinyin_for_phrase(phrase)

    if dictionary != None:
        elements = map(lambda x: print_ruby_with_english(x, dictionary), pinyin)
    else:
        elements = map(lambda x: print_ruby(x), pinyin)

    return u'<ruby>' + u''.join(elements) + u'</ruby>'
