__author__ = "Lily Seropian"

import length_distribution

def TestUpdateProbability():
  print 'Testing UpdateProbability'
  test_distro = length_distribution.LengthDistribution()
  assert({} == test_distro._GetDistribution())
  test_distro.UpdateProbability(6)
  assert({6 : 1} == test_distro._GetDistribution())
  test_distro.UpdateProbability(3)
  assert({6 : 1, 3 : 1} == test_distro._GetDistribution())
  test_distro.UpdateProbability(6)
  assert({6 : 2, 3 : 1} == test_distro._GetDistribution())
  print 'All UpdateProbability tests passed.'

def TestSample():
  print 'Testing Sample'
  test_distro = length_distribution.LengthDistribution()
  assert(None == test_distro.Sample())
  
  test_distro.UpdateProbability(4)
  assert(4 == test_distro.Sample())

  test_distro.UpdateProbability(3)
  _TestSampleHelper(test_distro, '{3: 500, 4: 500}')

  test_distro.UpdateProbability(4)
  _TestSampleHelper(test_distro, '{3: 333, 4: 666}')
  print 'All Sample tests passed.'

def _TestSampleHelper(distro, expected):
  results = {}
  for _ in range(1000):
    result = distro.Sample()
    results[result] = results[result] + 1 if result in results else 1
  print 'Expected ratio:', expected
  print 'Actual ratio:', results

if __name__ == '__main__':
  print
  TestUpdateProbability()
  print
  TestSample()
  print
