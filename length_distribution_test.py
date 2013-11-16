__author__ = "Lily Seropian"

import length_distribution
import unittest

class LengthDistributionTests(unittest.TestCase):

  def setUp(self):
    self.test_distro = length_distribution.LengthDistribution()

  def testUpdateProbability(self):
    self.assertEqual({}, self.test_distro._GetDistribution())

    self.test_distro.UpdateProbability(6)
    self.assertEqual({6 : 1}, self.test_distro._GetDistribution())

    self.test_distro.UpdateProbability(3)
    self.assertEqual({6 : 1, 3 : 1}, self.test_distro._GetDistribution())

    self.test_distro.UpdateProbability(6)
    self.assertEqual({6 : 2, 3 : 1}, self.test_distro._GetDistribution())

  def testSample(self):
    self.assertEqual(None, self.test_distro.Sample())
  
    self.test_distro.UpdateProbability(4)
    self.assertEqual(4, self.test_distro.Sample())

    self.test_distro.UpdateProbability(3)
    self._TestSampleHelper('{3: 500, 4: 500}')

    self.test_distro.UpdateProbability(4)
    self._TestSampleHelper('{3: 333, 4: 666}')

  def _TestSampleHelper(self, expected):
    results = {}
    for _ in range(1000):
      result = self.test_distro.Sample()
      results[result] = results[result] + 1 if result in results else 1
    print
    print
    print 'Expected ratio:', expected
    print 'Actual ratio:', results

if __name__ == '__main__':
  unittest.main(verbosity=2)
