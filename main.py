__author__ = "Lily Seropian"

from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys

import fold
import nussinov
import parse
<<<<<<< HEAD
import pairingScorer
import csv
##import matplotlib

'''
both mainPartioned and mainNoPartiition return a tuple (score, fold)
where score is an integer and fold is a list of tuples of tuples
ex: [(tuple base1, tuple base2),...,(tuple baseX, tuple baseY)]
where each base-tuple is (string letter, int position)
altogether, something of the form (1,[((b,2),(d,3)),...,((f,4),(h,5))])
'''
def mainPartitioned(numSeqs, partition_length):
    totalScore = 0
    with open('partitioned.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        seqList = parse.parse('RNAseqs', numSeqs)
        scoredFolded = []
        for RNA in seqList:
            if len(RNA) != 0:
                x = fold.Fold(RNA, partition_length)
                totalScore += x[0]
                scoredFolded += [x]
        aveScore = totalScore/float(numSeqs)
        writer.writerow([partition_length, aveScore])
    return scoredFolded

def mainNoPartition(numSeqs):
    seqList = parse.parse('RNAseqs', numSeqs)
    scoredFolded = []
    for RNA in seqList:
        if len(RNA) != 0:
          scoredFolded += [nussinov.FoldAndScore(nussinov.MakeSeq(RNA))] 
    return scoredFolded


##[mainPartitioned(4500, p) for p in range (1, 30, 1)]

##if __name__ == '__main__':
##    import timeit
##    sequences = 1
##    t = timeit.Timer(stmt = "mainNoPartition(" + str(sequences) + ")", setup = "from main import mainNoPartition")
##    u = timeit.Timer(stmt = "mainPartitioned(" + str(sequences) + ", " + str(100) + ")", setup = "from main import mainPartitioned")
##    tests = [timeit.Timer(stmt = "mainPartitioned(" + str(sequences) + ", " + str(p) + ")", setup = "from main import mainPartitioned") for p in range(4, 50, 2)]
##    trials = 5
##    print 'Without partitioning:', min([t.timeit(1) for x in xrange(1)])
##    print 'With threading:', min([u.timeit(1) for x in xrange(trials)])
##    for num, test in enumerate(tests):
##        print 'Partition size ' + str(4 + 2*num) + ': ', test.timeit(trials)
=======


# Contains a list of times followed by a list of lengths for unpartitioned
# results
TIME_V_LENGTH = 'time_v_length_no_part.txt'
TIME_V_LENGTH_GRAPH = 'time_v_length.png'

# Contains a list of times followed by a list of lengths for partitioned
# results with part_size
TIME_V_LENGTH_PARTED = 'time_v_length_part_{}.txt'
PART_V_TIME_GRAPH = 'part_size_v_time.png'

# Contains a list of average scores, followed by a list of partition sizes,
# followed by the average unpartitioned score.
ACCURACY = 'accuracy.txt'
PART_V_SIZE_GRAPH = 'part_size_v_score.png'

# Contains all results computed by our algorithms for a given sequence.
RESULTS = '{}_results.txt'

PART_SIZES = [10, 25, 50, 75, 100, 150, 200]

COLORS = {10: 'red', 25: 'orange', 50: 'yellow', 75: 'green', 100: 'cyan',
          150: 'blue', 200: 'purple'}

SEQ_DATA_STRING = 'Sequence: {}\nSequence Length: {}'
UNPARTITIONED_STRING = '\nUNPARTITIONED\nScore: {}\nTime: {}\nFolding: {}'
PARTITION_STRING = '\nPARTITIONED\nPartition Size: {}\nScore: {}\nTime: {}\nFolding: {}'

CALLING_ERROR = 'Use \'compute\' to run the algorithm and \'graph\' to graph the results'

def parse_float_vector(vector):
  return [float(elt) for elt in vector[1:len(vector)-1].split(', ')]

def parse_int_vector(vector):
  return [int(elt) for elt in vector[1:len(vector)-1].split(', ')]

def parse_time_v_length(filename):
  with open(filename) as f:
    contents = f.read().splitlines()
    times = parse_float_vector(contents[0])
    lengths = parse_int_vector(contents[1])
    return (times, lengths)

def move_legend(ax, percent):
  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * percent, box.width,
                   box.height * (1 - percent)])

def graph_results():
  ##################################
  # Sequence Length V Folding Time #
  ##################################
  plt.figure(1)
  ax = plt.subplot(111)
  plt.title('Sequence Length Versus Folding Time')
  plt.xlabel('Sequence Length (bp)')
  plt.ylabel('Folding Time (sec)')

  (unparted_times, lengths) = parse_time_v_length(TIME_V_LENGTH)
  graphs = [plt.scatter(lengths, unparted_times, c='k')]

  parted_times = []
  for part_size in PART_SIZES:
    (times, lengths) = parse_time_v_length(
        TIME_V_LENGTH_PARTED.format(part_size))
    graphs.append(plt.scatter(lengths, times, c=COLORS[part_size],
        edgecolor=COLORS[part_size]))
    parted_times.append(times)
 
  move_legend(ax, .2) 
  ax.legend(graphs, ['Unpartitioned', 'Length = 10', 'Length = 25',
      'Length = 50', 'Length = 75', 'Length = 100', 'Length = 150',
      'Length = 200'], loc='upper center', bbox_to_anchor=(.5, -.1), ncol=3)
  plt.savefig(TIME_V_LENGTH_GRAPH)

  #########################################
  # Partition Size V Average Folding Time #
  #########################################
  average_unparted = sum(unparted_times)/float(len(unparted_times))
  average_parted = [sum(times)/float(len(times)) for times in parted_times]
  plt.figure(2)
  ax = plt.subplot(111)
  plt.title('Partition Size Versus Average Folding Time')
  plt.xlabel('Partition Size (bp)')
  plt.ylabel('Average folding time (sec)')
  line = plt.axhline(y=average_unparted, c='red')
  scatter = plt.scatter(PART_SIZES, average_parted)
  move_legend(ax, .15)
  ax.legend([line, scatter], ['Unpartitioned Average', 'Partitioned'],
      loc='upper center', bbox_to_anchor=(.5, -.1))
  plt.savefig(PART_V_TIME_GRAPH)

  ##########################################
  # Partition Size V Average Folding Score #
  ##########################################
  contents = None
  with open(ACCURACY) as f:
    contents = f.read().splitlines()
  average_score_parted = parse_float_vector(contents[0])
  average_score_unparted = float(contents[2])
  plt.figure(3)
  ax = plt.subplot(111)
  plt.title('Partition Size Versus Average Folding Score')
  plt.xlabel('Partition Size(bp)')
  plt.ylabel('Average Folding Score (Nussinov Folding Criterion)')
  line = plt.axhline(y=average_score_unparted, c='red')
  scatter = plt.scatter(PART_SIZES, average_score_parted)
  move_legend(ax, .15)
  ax.legend([line, scatter], ['Unpartitioned Average', 'Partitioned'],
      loc='upper center', bbox_to_anchor=(.5, -.1))
  plt.savefig(PART_V_SIZE_GRAPH)
  

def compute_results():
  seqs = parse.parse('RNAseqs', 2)

  timing_unpartitioned = open(TIME_V_LENGTH, 'w')
  seq_lengths = []
  unpartitioned_times = []
  avg_unpartitioned_score = 0
  partitioned_times = {size : [] for size in PART_SIZES}
  partitioned_scores = {size: 0 for size in PART_SIZES}

  for (seq, filename) in seqs:
    print filename

    length = len(seq)
    seq_lengths.append(length)
    seq_data = SEQ_DATA_STRING.format(seq, length)

    start = datetime.now()
    unpartitioned_score, unpartitioned_folding = nussinov.FoldAndScore(
        nussinov.MakeSeq(seq))
    end = datetime.now()

    time_unpartitioned = (end - start).total_seconds()
    unpartitioned_times.append(time_unpartitioned)
    avg_unpartitioned_score += unpartitioned_score

    seq_data += UNPARTITIONED_STRING.format(unpartitioned_score,
        time_unpartitioned, unpartitioned_folding)

    for part_size in PART_SIZES:
      start = datetime.now()
      partitioned_score, partitioned_folding = fold.Fold(seq, part_size)    
      end = datetime.now()

      time_partitioned = (end - start).total_seconds()
      partitioned_times[part_size].append(time_partitioned)
      partitioned_scores[part_size] += partitioned_score

      seq_data += PARTITION_STRING.format(part_size, partitioned_score,
          time_partitioned, partitioned_folding)

    with open(RESULTS.format(filename[:len(filename)-3]), 'w') as f:
      f.write(seq_data)

  avg_unpartitioned_score /= float(len(unpartitioned_times))
  avg_partitioned_scores = [0]*len(PART_SIZES)
  for i in range(len(PART_SIZES)):
    avg_partitioned_scores[i] = partitioned_scores[PART_SIZES[i]]/float(len(
        partitioned_times[PART_SIZES[i]]))

  with open(TIME_V_LENGTH, 'w') as f:
    f.write(str(unpartitioned_times) + '\n' + str(seq_lengths))

  for part_size in PART_SIZES:
    with open(TIME_V_LENGTH_PARTED.format(part_size), 'w') as f:
      f.write(str(partitioned_times[part_size]) + '\n' + str(seq_lengths))

  with open(ACCURACY, 'w') as f:
    f.write(str(avg_partitioned_scores) + '\n' + str(PART_SIZES) + '\n' + \
        str(avg_unpartitioned_score))

if __name__ == '__main__':
  if len(sys.argv) == 2:
    if sys.argv[1] == 'compute':
      compute_results()
    elif sys.argv[1] == 'graph':
      graph_results()
    else:
      print CALLING_ERROR 
      sys.exit(1)
  else:
    print CALLING_ERROR
    sys.exit(1)
>>>>>>> b67652dad8d784722abfd870be14b965674b689d
