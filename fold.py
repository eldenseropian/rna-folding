__author__ = "Lily Seropian"

import nussinov

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
def _Partition(seq, length):
  if type(seq) == str:
    raise ValueError("You forgot to run MakeSeq on the input")
  N = len(seq)
  
  if length <= 0 or type(length) != int:
    raise ValueError(str(length) + ' is not a legal length')
  elif length == 1:
    return [[seq[0]]]
  elif length >= N:
    return [seq]
  else:
    num_even_parts = N - length + 1
    num_odd_parts = 0
    is_odd = length % 2 == 1
    if is_odd:
      # If there are an odd number of bps in the partition, the odd one
      # can go in the first or second half, doubling the number of
      # partitions. There is one overlap partition between the two
      # placements.
      num_odd_parts = num_even_parts - 1
    return [seq[:length/2] + seq[i + length/2 : i + length]
            for i in range(num_even_parts)] + \
           [seq[:length/2 + 1] + seq[i + length/2 + 2 : i + 1 + length]
            for i in range(num_odd_parts)]


"""
Takes in an RNA sequence and computes its best folding using partitions of
specified length.
"""
def Fold(seq, partition_length):
  RNA = nussinov.MakeSeq(seq)
  folding = []
  total_score = 0
  while len(RNA) > partition_length:
    best_score = -1
    best_pairing = None
    parts = _Partition(RNA, partition_length)

    for part in parts:
      score, pairing = nussinov.FoldAndScore(part)
      if score > best_score:
        best_score = score
        best_pairing = pairing

    total_score += best_score
    folding.extend(best_pairing)
    for pair in best_pairing:
      if pair[0] != (None, None):
        RNA.remove(pair[0])
      if pair[1] != (None, None):
        RNA.remove(pair[1])

  # Fold the last part of the sequence
  score, pairing = nussinov.FoldAndScore(RNA)
  folding.extend(pairing)
  return total_score, folding

if __name__ == '__main__':
  x = Fold('AGTCGGCTTGA', 5)
  for a in x:
    print a
