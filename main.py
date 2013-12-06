import nussinov
import fold
import parse
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
