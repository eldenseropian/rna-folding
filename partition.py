import length_data

"""
Takes in an RNA sequence and a structural element, and returns a list of
partitions of the sequence. The structural element is one of the constants
defined at the top of this file. The RNA sequence is a list of bases.
This method chooses a length for the sequences to return from a probability
distribution over the lengths of sequences representing the specified
structure, then returns a list of the first half of the partition taken
from the beginning of the sequence, concatenated with all possible end halves
to the partition.
"""
def Partition(seq, elt):
  length = _GetLength(elt)
  if length >= len(seq):
    return seq
  partitions = [seq[:length/2]]*(len(seq) - length)
  for i in range(len(seq) - length):
    partitions[i] += seq[i + length/2: i + length]
  print partitions
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

Partition('AGTCGGATTAGGATCTCTGA', length_data.STEM)
