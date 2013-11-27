__author__ = "Lily Seropian"

import unittest

import fold
from nussinov import *

class PartitionTests(unittest.TestCase):

  def testEqual(self):
    # length = len(seq)
    parts = fold._Partition(MakeSeq('AGTCA'), 5)
    self.assertEqual(parts, [[('A', 0), ('G', 1), ('T', 2), ('C', 3),
        ('A', 4)]])

  def testBigger(self):
    # length > len(seq)
    parts = fold._Partition(MakeSeq('AGTCA'), 6)
    self.assertEqual(parts, [[('A', 0), ('G', 1), ('T', 2), ('C', 3),
      ('A', 4)]])

  def testSmallerEven(self):
    # length < len(seq), length is even
    parts = fold._Partition(MakeSeq('AGTCA'), 2)
    self.assertEqual(parts, [[('A', 0), ('G', 1)],
                             [('A', 0), ('T', 2)],
                             [('A', 0), ('C', 3)],
                             [('A', 0), ('A', 4)]])

  def testSmallerOdd(self):
    # length < len(seq). length is odd
    parts = fold._Partition(MakeSeq('AGTCA'), 3)
    self.assertEqual(parts, [[('A', 0), ('G', 1), ('T', 2)],
                             [('A', 0), ('T', 2), ('C', 3)],
                             [('A', 0), ('C', 3), ('A', 4)],
                             [('A', 0), ('G', 1), ('C', 3)],
                             [('A', 0), ('G', 1), ('A', 4)]])

  def testOne(self):
    # length = 1
    parts = fold._Partition(MakeSeq('AGTCA'), 1)
    self.assertEqual(parts, [[('A', 0)]])

  def testZero(self):
    # length = 0
    self.assertRaises(ValueError, fold._Partition, 
        MakeSeq('AGTCA'), 0)

  def testNegative(self):
    # length is negative
    self.assertRaises(ValueError, fold._Partition,
        MakeSeq('AGTCA'), -5)

  def testRealNumber(self):
    # length is a real number
    self.assertRaises(ValueError, fold._Partition,
        MakeSeq('AGTCA'), 1.1)

if __name__ == '__main__':
  unittest.main(verbosity=2)
