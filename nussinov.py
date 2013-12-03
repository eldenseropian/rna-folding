__author__ = "Lily Seropian"

BASES = frozenset(['A', 'C', 'U', 'G', 'T'])
MATCHES = frozenset([('A', 'U'), ('U', 'A'), ('A', 'T'), ('T', 'A'),\
                     ('G', 'U'), ('U', 'G'), ('G', 'T'), ('T', 'G'),\
                     ('G', 'C'), ('C', 'G')])

# Directions refer to the dynamic programming matrix used by Nussinov's
# algorithm. These constants are used to traceback the pairing that yields
# the optimum score.
class PTR_NONE:
  pass
class PTR_LEFT:
  pass
class PTR_DOWN:
  pass
class PTR_USE:
  pass

"""
Uses Nussinov's algorithm to compute the optimal folding for an RNA sequence.

RNA is a list of tuples, where the first element in each tuple is a base
and the second element is the index of that base in the original sequence.
For example, for the sequence AGCU, RNA would be
    [('A', 0), ('G', 1), ('C', 2), ('U', 3)]
This is in order to support folding noncontiguous subsequences. If you have
a complete sequence you would like to fold, you can use the MakeSeq method
to turn the sequence into this format.

Returns a tuple of the score of the optimal folding, and the optimal folding
as a list of tuples, where each tuple contains 2 tuples representing bases
in the same format as the input. If a base is not paired with anything, the
corresponding tuple is (None, None). An example folding for 'CUAC':
    [(('C', 0), (None, None)), (('U', 1), ('A', 2)), (('C', 3), (None, None))]
"""
def FoldAndScore(RNA, debug=False):
  if len(RNA) == 0 or type(RNA) != list or type(RNA[0]) != tuple:
    raise ValueError('Invalid input to FoldAndScore: ' + str(RNA) + '.')
  N = len(RNA)

  score_matrix = [[0 for _ in range(N)] for _ in range(N)]
  paths = [[PTR_NONE for _ in range(N)] for _ in range(N)]

  # The scoring matrix uses the upper diagonal of the grid, and traverses
  # down a diagonal of negative slope before moving up/right to the next
  # diagonal.
  for i in range(N-1):
    for j in range(N-i-1):
      row, col = j, j + i + 1
      left = score_matrix[row][col - 1]
      down = score_matrix[row + 1][col]
      use = score_matrix[row + 1][col - 1]
      if (RNA[row][0], RNA[col][0]) in MATCHES:
        use += 1
      if use > down and use > left:
        score_matrix[row][col] = use
        paths[row][col] = PTR_USE
      elif left > down and left > use:
        score_matrix[row][col] = left
        paths[row][col] = PTR_LEFT
      else:
        score_matrix[row][col] = down
        paths[row][col] = PTR_DOWN

  if debug:
    _PrintScores(score_matrix)
    _PrintPaths(paths)

  return score_matrix[0][N-1], _Traceback(RNA, paths)

"""
Takes in a matrix of constants detailing what decisions the algorithm made,
and traces those decisions back to construct the folding.
RNA is the same as the input to FoldAndScore. path is a square matrix with
side length equal to the length of the RNA sequence, containing the constants
defined at the top of this file.
"""
def _Traceback(RNA, path):
  if len(RNA) == 1:
    return [(RNA[0], (None, None))]

  pairs = []
  row = 0
  col = len(RNA) - 1

  while col >= row and row < len(RNA) and col > 0:
    if path[row][col] == PTR_USE:
      pairs.append((RNA[row], RNA[col]))
      row += 1
      col -= 1
    elif path[row][col] == PTR_LEFT:
      pairs.append((RNA[col], (None, None)))
      col -= 1
    elif path[row][col] == PTR_DOWN:
      pairs.append((RNA[row], (None, None)))
      row += 1
    elif row == col:
      pairs.append((RNA[row], (None, None)))
      break
    else:
      raise ValueError
  return pairs

"""
Convert an RNA sequence represented as a string into the format described
in the FoldAndScore spec.
"""
def MakeSeq(seq):
  if len(seq) == 0:
    raise ValueError('Sequence of length 0')
  for i in range(len(seq)):
    if seq[i] not in BASES:
      raise ValueError('Unknown character ' + str(seq[i]) + ' found in sequence.') 
  return [(seq[i], i) for i in range(len(seq))]

""" Print the score matrix. Used for debugging. """
def _PrintScores(scores):
  for row in scores:
    out = ''
    for elt in row:
      out += str(elt) + ' '
    print out.strip()

""" Print the traceback matrix. Used for debugging. """
def _PrintPaths(paths):
  for row in paths:
    out = ''
    for elt in row:
      if elt == PTR_NONE:
        out += 'PTR_NONE '
      elif elt == PTR_LEFT:
        out += 'PTR_LEFT '
      elif elt == PTR_DOWN:
        out += 'PTR_DOWN '
      elif elt == PTR_USE:
        out += 'PTR_USE  '
    print out.strip()
