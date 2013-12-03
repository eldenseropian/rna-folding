import nussinov
import fold
import parse
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
    pass




if __name__ == '__main__':
    import timeit
    t = timeit.Timer(stmt = "mainNoPartition(20)", setup = "from main import mainNoPartition")
    u = timeit.Timer(stmt = "mainPartitioned(20, 10)", setup = "from main import mainPartitioned")
    print 'Without partioning:', t.timeit(3)
    print 'With partitioning:', u.timeit(3)
