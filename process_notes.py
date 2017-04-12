#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import ruby
import re
import sys

def process_notes():
    # Iterate through the spreadsheet and add all of the data.
    f = open("mcc1.tsv", "r")
    lines = f.readlines()

    inputheader = lines[0].rstrip().split('\t')
    header = {}
    for idx,column in enumerate(inputheader):
        header[column] = idx

    output = []
    outputheader = inputheader + ['Pinyin']

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

        output.append(cols + [ruby.print_rubys(mandarin)])

    sys.stdout.write('\t'.join(outputheader) + '\n')
    for cols in output:
        sys.stdout.write('\t'.join(cols) + '\n')

if __name__ == "__main__":
    process_notes()
