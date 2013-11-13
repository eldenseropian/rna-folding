import length_data
import classifier

"""
Takes in an RNA sequence and computes its best folding.
"""
def Fold(seq):
  folding = []
  while len(seq) > 0:
    best_score = 0
    best_elt = None
    best_part = None
    for elt in length_data.LEGAL_ELEMENTS:
      parts = Partition(seq, elt)
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
def Partition(seq, elt):
  length = _GetLength(elt)
  if length >= len(seq):
    return [[[(0, len(seq)), (len(seq), len(seq))], seq]]
  partitions = [[[(0, length/2 + 1)], seq[:length/2 + 1]]
                for _ in range(len(seq) - length)]
  for i in range(len(seq) - length):
    partitions[i][0].append((i + length/2 + 1, i + length))
    partitions[i][1] += seq[i + length/2 + 1 : i + length]
  return partitions

def _GetLength(elt):
  if elt not in length_data.LEGAL_ELEMENTS:
    raise UnknownStructuralElement(elt)
  return length_data.Sample(elt)

class UnknownStructuralElement(Exception):
  def __init__(self, elt):
    self.elt = elt

  def __str__(self):
    return str(self.elt) + ' is an unknown type. Valid elements are' + \
        ' partition.BULGE, partition.HAIRPIN, partition.INTERNAL_LOOP,' + \
        ' partition.MULTI_LOOP, and partition.STEM'

x = Fold('AGTCGGCTTGA')
for a in x:
  print a[0], a[1]
