import nussinov
import fold
import parse
import pairingScorer
import matplotlib

def mainPartitioned(numSeqs, partition_length):
    seqList = parse.parse('RNAseqs', numSeqs)
    folded = []
    for RNA in seqList:
        if len(RNA) != 0:
          folded += [fold.Fold(RNA, partition_length)] #with partition, run with different lengths
    return folded

def mainNoPartition(numSeqs):
    seqList = parse.parse('RNAseqs', numSeqs)
    scoredFolded = []
    for RNA in seqList:
        if len(RNA) != 0:
          scoredFolded += [nussinov.FoldAndScore(nussinov.MakeSeq(RNA))] #without partition
    return scoredFolded

def scorePartitioned(folded):
    return pairingScorer.score(folded)




if __name__ == '__main__':
    import timeit
    sequences = 1
    t = timeit.Timer(stmt = "mainNoPartition(" + str(sequences) + ")", setup = "from main import mainNoPartition")
    u = timeit.Timer(stmt = "mainPartitioned(" + str(sequences) + ", " + str(100) + ")", setup = "from main import mainPartitioned")
    tests = [timeit.Timer(stmt = "mainPartitioned(" + str(sequences) + ", " + str(p) + ")", setup = "from main import mainPartitioned") for p in range(150, 250, 20)]
    trials = 5
    print 'Without partioning:', min([t.timeit(1) for x in xrange(1)])
##    print 'With threading:', min([u.timeit(1) for x in xrange(trials)])
    for num, test in enumerate(tests):
        print 'Partition size ' + str(150 + 20*num) + ': ', test.timeit(trials)
