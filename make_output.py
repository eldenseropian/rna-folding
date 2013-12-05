__author__ = "Lily Seropian"

from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys

import fold
import nussinov
import parse


'''
time_v_length_part_[part_size].txt contains an array of times followed by an array of lengths for partitioned wth part_size
time_v_length_no_part.txt contains the above for the unpartitioned version

accuracy.txt contains tuples of (unpartitioned_score, partitioned_score, difference, partition_size, seq_size)
'''

PART_SIZES = [10, 25, 50, 75, 100, 150, 200]
COLORS = {10: 'red', 25: 'orange', 50: 'yellow', 75: 'green', 100: 'cyan',
          150: 'blue', 200: 'purple'}

def parse_float_vector(vector):
  return [float(elt) for elt in vector[1:len(vector)-1].split(', ')]

def parse_int_vector(vector):
  return [int(elt) for elt in vector[1:len(vector)-1].split(', ')]

def parse_time_length_graph(filename):
  with open(filename) as f:
    contents = f.read().splitlines()
    times = parse_float_vector(contents[0])
    lengths = parse_int_vector(contents[1])
    return (times, lengths)

def move_legend(ax, percent):
  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * percent, box.width,
                   box.height * (1 - percent)])

def make_graphs():
  plt.figure(1)
  ax = plt.subplot(111)
  plt.title('Sequence Length Versus Folding Time')
  plt.xlabel('Sequence Length (bp)')
  plt.ylabel('Folding Time (sec)')

  (unparted_times, lengths) = parse_time_length_graph('time_v_length_no_part.txt')
  graphs = [plt.scatter(lengths, unparted_times, c='k')]

  parted_times = []
  for part_size in PART_SIZES:
    (times, lengths) = parse_time_length_graph(
        'time_v_length_part_' + str(part_size) + '.txt')
    graphs.append(plt.scatter(lengths, times, c=COLORS[part_size],
        edgecolor=COLORS[part_size]))
    parted_times.append(times)
 
  move_legend(ax, .2) 
  ax.legend(graphs, ['Unpartitioned', 'Length = 10', 'Length = 25',
      'Length = 50', 'Length = 75', 'Length = 100', 'Length = 150',
      'Length = 200'], loc='upper center', bbox_to_anchor=(.5, -.1), ncol=3)
  plt.savefig('time_v_length.png')

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
  plt.savefig('part_size_v_time.png')

  contents = None
  with open('accuracy.txt') as f:
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
  plt.savefig('part_size_v_score.png')
  

NUM_SEQS = 2

if __name__ == '__main__':
  if len(sys.argv) > 1:
    make_graphs()
    sys.exit(0)

  seqs = parse.parse('RNAseqs', NUM_SEQS)

  timing_unpartitioned = open('time_v_length_no_part.txt', 'w')
  seq_lengths = []
  unpartitioned_times = []
  avg_unpartitioned_score = 0
  partitioned_times = {size : [] for size in PART_SIZES}
  partitioned_scores = {size: 0 for size in PART_SIZES}

  for (seq, filename) in seqs[:NUM_SEQS]:
    print filename
    seq_data = seq

    length = len(seq)
    seq_lengths.append(length)
    seq_data += '\n' + str(length)

    start = datetime.now()
    unpartitioned_score, unpartitioned_folding = nussinov.FoldAndScore(
        nussinov.MakeSeq(seq))
    end = datetime.now()

    time_unpartitioned = (end - start).total_seconds()
    unpartitioned_times.append(time_unpartitioned)
    avg_unpartitioned_score += unpartitioned_score

    seq_data += '\nUNPARTITIONED'
    seq_data += '\nScore:\t' +  str(unpartitioned_score)
    seq_data += '\nTime:\t' + str(time_unpartitioned)
    seq_data += '\nFolding:\t' + str(unpartitioned_folding)

    for part_size in PART_SIZES:
      start = datetime.now()
      partitioned_score, partitioned_folding = fold.Fold(seq, part_size)    
      end = datetime.now()

      time_partitioned = (end - start).total_seconds()
      partitioned_times[part_size].append(time_partitioned)
      partitioned_scores[part_size] += partitioned_score

      seq_data += '\nPARTITIONED'
      seq_data += '\nPartition Size:\t' + str(part_size)
      seq_data += '\nScore:\t' + str(partitioned_score)
      seq_data += '\nTime:\t' + str(time_partitioned)
      seq_data += '\nFolding:\t' + str(partitioned_folding)
    with open(filename[:len(filename)-3] + '_results.txt', 'w') as f:
      f.write(seq_data)

  avg_unpartitioned_score /= float(len(unpartitioned_times))
  avg_partitioned_scores = [0]*len(PART_SIZES)
  for i in range(len(PART_SIZES)):
    avg_partitioned_scores[i] = partitioned_scores[PART_SIZES[i]]/float(len(
        partitioned_times[PART_SIZES[i]]))

  with open('time_v_length_no_part.txt', 'w') as f:
    f.write(str(unpartitioned_times) + '\n' + str(seq_lengths))

  for part_size in PART_SIZES:
    with open('time_v_length_part_' + str(part_size) + '.txt', 'w') as f:
      f.write(str(partitioned_times[part_size]) + '\n' + str(seq_lengths))

  with open('accuracy.txt', 'w') as f:
    f.write(str(avg_partitioned_scores) + '\n' + str(PART_SIZES) + '\n' + \
        str(avg_unpartitioned_score))
