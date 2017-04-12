#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Reads an Anki deck from an .apkg file and outputs the notes it contains in
# tsv format.
#
# Example usage: python3 read_apkg.py > mcc1.tsv
#

import sys
import os
import tempfile
import sqlite3
import zipfile
import json


class Package:
  def __init__(self):
    self.decks = []

  def read_from_file(self):
    # Create a temporary file for the sqllite db.
    dbfile, dbfilename = tempfile.mkstemp()

    # Unzip the db to the temporary file.
    with zipfile.ZipFile('mcc1.apkg', 'r') as inputzip:
      data = inputzip.read('collection.anki2')
      os.write(dbfile, data)
    os.close(dbfile)

    # Now open the db using sqllite.
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
  
    self.read_from_db(cursor)
  
    conn.close()
  
  def read_from_db(self, cursor):

    # Read a list of fields for each model.
    cursor.execute('SELECT models FROM col')
    all_cols = cursor.fetchall()

    fields_by_model = {}
    for collection in all_cols:
        for model in collection:
            m = json.loads(model)
            for mid in m:
                fields_for_model = []
                flds = m[mid]['flds']
                for field in flds:
                    fields_for_model.append(field['name'])
                fields_by_model[int(mid)] = fields_for_model

    s = 'SELECT * FROM notes'
    cursor.execute(s)
    all_rows = cursor.fetchall()

    print_header = True

    for note in all_rows:
      id = note[0]
      guid = note[1] # globally unique id for the note
      mid = note[2]  # model id
      flds = note[6] # field content separated by \x1f

      # Print the header row of the tsv.
      if print_header:
        print("%s" % ("\t".join(["id", "guid", "mid"]+fields_by_model[mid])))
        print_header = False

      fields = flds.split(u'\x1f')

      line = (u'%s\t%s\t%s\t%s\n' % (id, guid, mid, u'\t'.join(fields)))
      sys.stdout.write(line)

if __name__ == "__main__":
    p = Package()
    p.read_from_file()
