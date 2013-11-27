__author__ = "Lily Seropian"

import unittest

from nussinov import *

class NussinovTests(unittest.TestCase):

  def testSingleNucleotide(self):
    self.Test('A', 0, [(('A', 0), (None, None))])

  def testNoMatching(self):
    self.Test('AG', 0, [(('A', 0), (None, None)), (('G', 1), (None, None))])

  def testPerfectMatchingSmall(self):
    self.Test('GAUC', 2, [(('G', 0), ('C', 3)), (('A', 1), ('U', 2))])

  def testPerfectMatchingLarge(self):
    self.Test('CGACGGAUCUGUUG', 7, [(('C', 0), ('G', 13)),
        (('G', 1), ('U', 12)), (('A', 2), ('U', 11)),
        (('C', 3), ('G', 10)), (('G', 4), ('U', 9)),
        (('G', 5), ('C', 8)), (('A', 6), ('U', 7))])

  def testImperfectMatchingCenterSmall(self):
    self.Test('GACUC', 2, [(('G', 0), ('C', 4)), (('A', 1), ('U', 3)),
        (('C', 2), (None, None))])

  def testImperfectMatchingEndSmall(self):
    self.Test('GAUCA', 2, [(('G', 0), ('C', 3)), (('A', 1), ('U', 2)),
        (('A', 4), (None, None))])

  def testLoop(self):
    self.Test('GGGGAAAACCCC', 4,
        [(('G', 0), ('C', 11)), (('G', 1), ('C', 10)), (('G', 2), ('C', 9)),
         (('G', 3), ('C', 8)), (('A', 4), (None, None)),
         (('A', 5), (None, None)), (('A', 6), (None, None)),
         (('A', 7), (None, None))])

  def testBulge(self):
    self.Test('AAACCCAACCCUUCCCCUUU', 5,
        [(('A', 0), ('U', 19)), (('A', 1), ('U', 18)), (('A', 2), ('U', 17)),
         (('C', 3), (None, None)), (('C', 4), (None, None)),
         (('C', 5), (None, None)), (('C', 13), (None, None)),
         (('C', 14), (None, None)), (('C', 15), (None, None)),
         (('C', 16), (None, None)), (('C', 8), (None, None)),
         (('C', 9), (None, None)), (('C', 10), (None, None)),
         (('A', 6), ('U', 12)), (('A', 7), ('U', 11))])

  def Test(self, seq, expected_score, expected_pairs, debug=False):
    (actual_score, actual_pairs) = FoldAndScore(seq, debug=debug)
    self.assertEqual(expected_score, actual_score)
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
