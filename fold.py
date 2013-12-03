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
    if length % 2 == 1:
      # If there are an odd number of bps in the partition, the odd one
      # can go in the first or second half, doubling the number of partitions.
      # There is one overlap partition between the two placements.
      num_odd_parts = num_even_parts - 1
    partitions = [[seq[i] for i in range(length/2)]
                  for _ in range(num_even_parts)] + \
                 [[seq[i] for i in range(length/2 + 1)]
                  for _ in range(num_odd_parts)]

    # The odd base goes in the second half of the partition
    for i in range(num_even_parts):
      for j in range(i + length/2, i + length):
        partitions[i].append(seq[j])

    if length% 2 == 1:
      # Add the odd base going in the first half
      for i in range(1, num_even_parts):
        for j in range(i + length/2 + 1, i + length):
          partitions[i + num_even_parts - 1].append(seq[j])
    return partitions


"""
Takes in an RNA sequence and computes its best folding using partitions of
specified length.
"""
def Fold(seq, partition_length):
  RNA = nussinov.MakeSeq(seq)
  folding = []
  while len(RNA) > partition_length:
    best_score = -1
    best_pairing = None
    parts = _Partition(RNA, partition_length)

    for part in parts:
      score, pairing = nussinov.FoldAndScore(part)
      if score > best_score:
        best_score = score
        best_pairing = pairing

    folding.extend(best_pairing)
    used_bases = set([])
    for pair in best_pairing:
      used_bases.add(pair[0])
      used_bases.add(pair[1])
    RNA = [base for base in RNA if base not in used_bases]

  # Fold the last part of the sequence
  score, pairing = nussinov.FoldAndScore(RNA)
  folding.extend(pairing)
  return folding

if __name__ == '__main__':
  x = Fold('AGTCGGCTTGA', 5)
  for a in x:
    print a
