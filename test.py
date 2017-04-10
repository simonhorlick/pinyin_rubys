#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from pypinyin import pinyin
from ruby import pinyin_for_word, pinyin_for_phrase, print_rubys


def test_tone_change_with_different_meaning():
    assert (pinyin_for_word(u'当')) == u'dāng'
    assert (pinyin_for_word(u'当真')) == u'dàngzhēn'


def test_segment_and_convert():
    assert (pinyin_for_phrase(u'我明白了。')) == [(u'我', u'wǒ'), (u'明白', u'míngbái'),
                                             (u'了', u'le'), (u'。', u'')]


def test_html_output():
    assert (
        print_rubys(u'我明白了。')
    ) == u'<ruby><rb>我</rb><rt>wǒ</rt><rb>明白</rb><rt>míngbái</rt><rb>了</rb><rt>le</rt><rb>。</rb><rt></rt></ruby>'
