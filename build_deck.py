#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import genanki
import random
import ruby
import re

def build_deck():
    # A Model defines the fields and cards for a type of Note.
    sentences = genanki.Model(
	1342696647976,
	'iKnow! Sentences',
	fields=[
	    {'name': 'Expression'},
	    {'name': 'Meaning'},
	    {'name': 'Pinyin'},
	    {'name': 'Reading'},
	    {'name': 'Audio'},
	    {'name': 'Image_URI'},
	    {'name': 'iKnowID'},
	    {'name': 'iKnowType'},
	],
	css = """
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.trans {}
.entry { text-align: left; font-size: x-large; }
.def { text-align: left; font-size: medium; }
.reading {font-size: small;}
.card1 { background-color: #FFFFFF; }
.card2 { background-color: #FFFFFF; }""",
	templates=[
	    {
		'name': 'Listening',
		'qfmt': '{{Audio}}',
		'afmt': '{{Audio}}<hr id=answer>{{Pinyin}}<br><div class=reading>{{Reading}}</div><br>{{Meaning}}',
	    },
	    {
		'name': 'Reading',
		'qfmt': '{{Expression}}',
		'afmt': '{{Pinyin}}<br><div class=reading>{{Reading}}</div><br>{{Meaning}}<br>{{Audio}}',
	    },
	]
    )

    vocab = genanki.Model(
	1342696647980,
	'iKnow! Vocabulary',
	fields=[
	    {'name': 'Expression'},
	    {'name': 'Meaning'},
	    {'name': 'Pinyin'},
	    {'name': 'Reading'},
	    {'name': 'Audio'},
	    {'name': 'Image_URI'},
	    {'name': 'iKnowID'},
	    {'name': 'iKnowType'},
	],
	css = """
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.trans {}
.entry { text-align: left; font-size: x-large; }
.def { text-align: left; font-size: medium; }
.card1 { background-color: #FFFFFF; }
.card2 { background-color: #FFFFFF; }""",
	templates=[
	    {
		'name': 'Listening',
		'qfmt': '{{Audio}}',
		'afmt': '{{Audio}}<hr id=answer>{{Pinyin}}<br>{{Meaning}}',
	    },
	    {
		'name': 'Production',
		'qfmt': '{{Pinyin}}<br>{{Audio}}',
		'afmt': '{{FrontSide}}<hr id=answer>{{Meaning}}<br>{{Audio}}',
	    },
	    {
		'name': 'Reading',
		'qfmt': '{{Expression}}',
		'afmt': '{{Pinyin}}<br>{{Meaning}}<br>{{Audio}}',
	    },
	]
    )

    my_deck = genanki.Deck(
      1342696648231,
      'Mastering Chinese Characters 01 (Listening Sentence & Vocab)')

    notes = []

    # Now iterate through the spreadsheet and add all of the data.
    f = open("mcc1-new.tsv", "r")
    lines = f.readlines()
    print("Read %d lines" % len(lines))

    inputheader = lines[0].rstrip().split('\t')
    header = {}
    for idx,column in enumerate(inputheader):
        header[column] = idx

    for line in lines[1:]:

        cols = line.rstrip().split('\t')

        id = cols[header['id']]
        guid = cols[header['guid']]
        mid = cols[header['mid']]

        model = None
        if mid == '1342696647980':
            model = vocab
        elif mid == '1342696647976':
            model = sentences
        else:
            raise('Unknown mid')

        # TODO(simon): Iterate these based on the model.
        Expression = cols[header['Expression']]
        Meaning = cols[header['Dictionary']]
        Reading = cols[header['Reading']]
        Audio = cols[header['Audio']]
        Image_URI = cols[header['Image_URI']]
        iKnowID = cols[header['iKnowID']]
        iKnowType = cols[header['iKnowType']]
        Pinyin = cols[header['Pinyin']]

        print("Creating note for %s" % Expression)
        my_note = genanki.Note(
            model = model,
            guid = guid,
            fields = [
                Expression,
                Meaning,
                Pinyin,
                Reading,
                Audio,
                Image_URI,
                iKnowID,
                iKnowType
            ]
        )
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('output.apkg')

if __name__ == "__main__":
    build_deck()
