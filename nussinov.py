import random

MATCHES = (('A', 'U'), ('U', 'A'),\
           ('G', 'U'), ('U', 'G'),\
           ('G', 'C'), ('C', 'G'))
PTR_NONE, PTR_LEFT, PTR_BELOW, PTR_USE = 0, 1, 2, 3

def FoldAndScore(RNA, debug=False):
  N = len(RNA)
  score_matrix = [[0 for _ in range(N)] for _ in range(N)]
  paths = [[PTR_NONE for _ in range(N)] for _ in range(N)]

  for i in range(N-1):
    for j in range(N-i-1):
      row, col = j, j + i + 1
      left = score_matrix[row][col - 1]
      below = score_matrix[row + 1][col]
      use = score_matrix[row + 1][col - 1]
      if (RNA[row][0], RNA[col][0]) in MATCHES:
        use += 1
      if use > below and use > left:
        score_matrix[row][col] = use
        paths[row][col] = PTR_USE
      elif left > below and left > use:
        score_matrix[row][col] = left
        paths[row][col] = PTR_LEFT
      else:
        score_matrix[row][col] = below
        paths[row][col] = PTR_BELOW

  if debug:
    PrintScores(score_matrix)
    PrintPaths(paths)
  return score_matrix[0][N-1], Traceback(MakeSeq(RNA), paths)


def Traceback(RNA, path):
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
    elif path[row][col] == PTR_BELOW:
      pairs.append((RNA[row], (None, None)))
      row += 1
    elif row == col:
      pairs.append((RNA[row], (None, None)))
      break
    else:
      raise ValueError
  return pairs

def MakeSeq(seq):
  return [(seq[i], i) for i in range(len(seq))]

def PrintScores(scores):
  for row in scores:
    out = ''
    for elt in row:
      out += str(elt) + ' '
    print out.strip()

def PrintPaths(paths):
  for row in paths:
    out = ''
    for elt in row:
      if elt == PTR_NONE:
        out += 'PTR_NONE '
      elif elt == PTR_LEFT:
        out += 'PTR_LEFT '
      elif elt == PTR_BELOW:
        out += 'PTR_BELOW '
      elif elt == PTR_USE:
        out += 'PTR_USE '
    print out.strip()


FoldAndScore('GACUC')
