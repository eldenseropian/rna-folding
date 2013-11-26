__author__ = "Lily Seropian"

import unittest

from nussinov import *

class NussinovTests(unittest.TestCase):

  def testPerfectMatchingSmall(self):
    self.Test('GAUC', 2, [(('G', 0), ('C', 3)), (('A', 1), ('U', 2))])

  def testPerfectMatchingLarge(self):
    self.Test('CGACGGAUCUGUUG', 7, [(('C', 0), ('G', 13)),
        (('G', 1), ('U', 12)), (('A', 2), ('U', 11)),
        (('C', 3), ('G', 10)), (('G', 4), ('U', 9)),
        (('G', 5), ('C', 8)), (('A', 6), ('U', 7))])

  def testImperfectMatchingSmall(self):
    self.Test('GACUC', 2, [(('G', 0), ('C', 4)), (('A', 1), ('U', 3)),
        (('C', 2), (None, None))])

  def Test(self, seq, expected_score, expected_pairs):
    (actual_score, paths) = FoldAndScore(seq)
    self.assertEqual(expected_score, actual_score)
    actual_pairs = Traceback(MakeSeq(seq), paths)
    try:
      self.assertEqual(self.Settify(expected_pairs),
          self.Settify(actual_pairs))
    except AssertionError as e:
      print '\n\nExpected', expected_pairs
      print '\nReceived', actual_pairs, '\n'
      raise e

  def Settify(self, list_of_pairs):
    return set([frozenset(pair) for pair in list_of_pairs])

if __name__ == '__main__':
  unittest.main(verbosity=2)
