__author__ = "Lily Seropian"

'''
BAND: part of pseudoknot stuff
BULGE_AND_INTERNAL_LOOP: element
CONNECTION: connection between structures
ELEM_STR_SEQUENCE_FEATURES: properties of sequence
EXTERNAL_AND_MULTI_LOOP: element
EXTERNAL_AND_MULTI_LOOP_BRANCH: element
EXTERNAL_SOURCE: external sources of data
HAIRPIN_LOOP: element
HAIRPIN_MOTIF: element?
MOLECULE: RNA molecule
NON_CANONICAL_BP: BP that's not Watson-Crick or wobble
PKNOT_LOOP: pseudoknot stuff
PSEUDOKNOT: pseudoknot stuff
PSEUDOKNOT_TYPE: pseudoknot stuff
RNA_TYPE: info about RNA type
STEM: element
TMP_MOLECULE: dummy molecule
'''

import _mysql
import MySQLdb as mdb
import sys

# Bands/pseudoknots not considered
ELTS = ('BULGE_AND_INTERNAL_LOOP', 'EXTERNAL_AND_MULTI_LOOP',
        'EXTERNAL_AND_MULTI_LOOP_BRANCH', 'HAIRPIN_LOOP', 'HAIRPIN_MOTIF',
        'STEM')

def Read():
  con = None
  try:
    con = mdb.connect('localhost', 'testuser', 'test623', 'sstrand_2_0')
    cur = con.cursor()
    for elt in ELTS:
      cur.execute("SELECT * FROM " + elt)
      data = cur.fetchall()
      cols = cur.description
      print 'There are', len(data), 'datapoints about', elt
      print 'The information available about', elt, 'is:'
      print "- %s\n"*len(cols) % tuple([c[0] for c in cols])
  except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
  finally:
    if con:
      con.close()

if __name__ == "__main__":
  Read()
