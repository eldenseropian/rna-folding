__author__ = "Lily Seropian"

import unittest

import fold
import length_data

class PartitionTests(unittest.TestCase):
  def setUp(self):
    self.test_elt = length_data.LEGAL_ELEMENTS[0]

  # Tests use lambda mocks of the _GetLength method, which is used to
  # probabilistically determine a sequence length

  def testEqual(self):
    # length = len(seq)
    parts = fold._Partition('AGTCA', self.test_elt, lambda elt: 5)
    self.assertEqual(parts, [[[(0, 5), (5, 5)], 'AGTCA']])

  def testBigger(self):
    # length > len(seq)
    parts = fold._Partition('AGTCA', self.test_elt, lambda elt: 6)
    self.assertEqual(parts, [[[(0, 5), (5, 5)], 'AGTCA']])

  def testSmallerEven(self):
    # length < len(seq), length is even
    parts = fold._Partition('AGTCA', self.test_elt, lambda elt: 2)
    self.assertEqual(parts, [[[(0, 1), (1, 2)], 'AG'],
                             [[(0, 1), (2, 3)], 'AT'],
                             [[(0, 1), (3, 4)], 'AC'],
                             [[(0, 1), (4, 5)], 'AA']])

  def testSmallerOdd(self):
    # length < len(seq). length is odd
    parts = fold._Partition('AGTCA', self.test_elt, lambda elt: 3)
    self.assertEqual(parts, [[[(0, 1), (1, 3)], 'AGT'],
                             [[(0, 1), (2, 4)], 'ATC'],
                             [[(0, 1), (3, 5)], 'ACA'],
                             [[(0, 2), (3, 4)], 'AGC'],
                             [[(0, 2), (4, 5)], 'AGA']])
  def testOne(self):
    # length = 1
    parts = fold._Partition('AGTCA', self.test_elt, lambda elt: 1)
    self.assertEqual(parts, [[[(0, 1), (1, 1)], 'A']])

  def testZero(self):
    # length = 0
    self.assertRaises(fold.IllegalLengthException, fold._Partition, 'AGTCA',
        self.test_elt, lambda elt: 0)

  def testNegative(self):
    # length is negative
    self.assertRaises(fold.IllegalLengthException, fold._Partition, 'AGTCA',
        self.test_elt, lambda elt: -5)

  def testRealNumber(self):
    # length is a real number
    self.assertRaises(fold.IllegalLengthException, fold._Partition, 'AGTCA',
        self.test_elt, lambda elt: 1.1)

if __name__ == '__main__':
  unittest.main(verbosity=2)
