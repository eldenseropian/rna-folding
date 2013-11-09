import random

class LengthDistribution:

  def __init__(self):
    self.dist = {}

  # Update the number of times length (int) has been seen
  def UpdateProbability(self, length):
    self.dist[length] = self.dist[length] + 1 if length in self.dist else 1

  # Sample the distribution
  # Returns None if the distribution is empty
  # Returns a length (int) otherwise
  def Sample(self):
    if not self.dist:
      return None
    lengths = self.dist.keys()
    probs = [self.dist[lengths[0]]]
    for i in range(1, len(lengths)):
      probs.append(self.dist[lengths[i]] + probs[i-1])
    probs = [prob/float(sum(self.dist.itervalues())) for prob in probs]
    r = random.random()
    for i in range(len(probs)):
      if r < probs[i]:
        return lengths[i]

  def _GetDistribution(self):
    return self.dist
