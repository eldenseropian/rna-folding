__author__ = "Lily Seropian"

import length_data
import classifier

"""
Returns a probabilistically selected length for a given structural element.
"""
def _GetLength(elt):
  if elt not in length_data.LEGAL_ELEMENTS:
    raise UnknownStructuralElement(elt)
  return length_data.Sample(elt)

"""
Takes in an RNA sequence and a structural element, and returns a list of
partitions of the sequence. The structural element is one of the constants
defined at the top of this file. The RNA sequence is a list of bases.
This method chooses a length for the sequences to return from a probability
distribution over the lengths of sequences representing the specified
structure, then returns a list of the partitions. The partitions are lists.
The first element in the list is a list of tuples representing the start and
end indices of both halves of the partition (e.g. [(0, 4), (8, 12)]). The second
element is the first half of the partition taken from the beginning of the
sequence, concatenated with a possible end half.
"""
def _Partition(seq, elt, GetLength=_GetLength):
  l = GetLength(elt)
  
  if l <= 0 or type(l) != int:
    raise IllegalLengthException
  elif l == 1:
    return [[[(0, 1), (1, 1)], seq[0]]]
  elif l >= len(seq):
    return [[[(0, len(seq)), (len(seq), len(seq))], seq]]
  else:
    num_even_parts = len(seq) - l + 1
    num_odd_parts = 0
    if l % 2 == 1:
      # If there are an odd number of bps in the partition, the odd one
      # can go in the first or second half, doubling the number of partitions.
      # There is one overlap partition between the two placements.
      num_odd_parts = num_even_parts - 1
    partitions = [[[(0, l/2)], seq[:l/2]] for _ in range(num_even_parts)] + \
                 [[[(0, l/2+1)], seq[:l/2+1]] for _ in range(num_odd_parts)]

    # The odd base goes in the second half of the partition
    for i in range(num_even_parts):
      partitions[i][0].append((i + l/2, i + l))
      partitions[i][1] += seq[i + l/2 : i + l]

    if l% 2 == 1:
      # Add the odd base going in the first half
      for i in range(1, num_even_parts):
        partitions[i + num_even_parts - 1][0].append((i + l/2 + 1, i + l))
        partitions[i + num_even_parts - 1][1] += seq[i + l/2 + 1: i + l]
    return partitions

"""
Takes in an RNA sequence and computes its best folding.
"""
def Fold(seq, Partition=_Partition):
  folding = []
  while len(seq) > 0:
    best_score = 0
    best_elt = None
    best_part = None
    for elt in length_data.LEGAL_ELEMENTS:
      parts = _Partition(seq, elt)
      for part in parts:
        score = classifier.score(part[1], elt)
        if score > best_score:
          best_score = score
          best_elt = elt
          best_part = part
    folding.append((best_part[1], best_elt))
    start, end = best_part[0][0], best_part[0][1]
    old_seq = seq[:]
    seq = seq[:start[0]] + \
          seq[start[1] : end[0]] + \
          seq[end[1] :]
  return folding

class UnknownStructuralElement(Exception):
  def __init__(self, elt):
    self.elt = elt

  def __str__(self):
    return str(self.elt) + ' is an unknown type. Valid elements are' + \
        ' partition.BULGE, partition.HAIRPIN, partition.INTERNAL_LOOP,' + \
        ' partition.MULTI_LOOP, and partition.STEM'

class IllegalLengthException(Exception):
  pass

if __name__ == '__main__':
  x = Fold('AGTCGGCTTGA')
  for a in x:
    print a[0], a[1]
