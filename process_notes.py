#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import ruby
import re
import sys

def print_dictionary(translation, dictionary, definitions):
    defs = []
    for definition in definitions:
        defs.append("<li>%s</li>" % definition)

    return "<div class=trans>%s</div><div class=entry>%s</div><ul class=def>%s</ul>" % (translation, dictionary, "".join(defs))

def process_notes():
    # Iterate through the spreadsheet and add all of the data.
    f = open("mcc1.tsv", "r")
    lines = f.readlines()

    inputheader = lines[0].rstrip().split('\t')
    header = {}
    for idx,column in enumerate(inputheader):
        header[column] = idx

    output = []
    outputheader = inputheader + ['Pinyin', 'Dictionary']

    for line in lines[1:]:
        cols = line.rstrip().split('\t')

        Expression = cols[header['Expression']]

        mandarin = Expression

        # For sentences we have both the tranditional and simplified
        # translations, regex the simplified one and use that.
        # trad: <b>我</b>是老師。<br />hans: <b>我</b>是老师。
        m = re.search(u'.*hans: (.*)', Expression)
        if m != None:
            mandarin = m.group(1)

        # TODO(simon): These are important, add them back in.
        mandarin = mandarin.replace('<b>','')
        mandarin = mandarin.replace('</b>','')

        # Meaning comes with an optional translation, followed by the
        # dictionary entry for that character.
        Meaning = cols[header['Meaning']]
        translation = ""
        dictionary = ""
        definition = ""
        m = re.search(u'([^<]*)<br />(.*) -- (.*)', Meaning)
        if m != None:
            translation = m.group(1)
            dictionary = m.group(2)
            simplified_matcher = re.search(u'.*hans: (.*)', dictionary)
            if simplified_matcher != None:
                dictionary = simplified_matcher.group(1)
            definition = m.group(3).split('♦')
        else:
            definition = Meaning.split('♦')

        definition = list(filter(None, definition))
        definition = list(map(str.strip, definition))

        output.append(cols + [ruby.print_rubys(mandarin), print_dictionary(translation, dictionary, definition)])

    sys.stdout.write('\t'.join(outputheader) + '\n')
    for cols in output:
        sys.stdout.write('\t'.join(cols) + '\n')

if __name__ == "__main__":
    process_notes()
