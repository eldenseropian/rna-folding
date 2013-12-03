import nussinov
import fold
import parse
import matplotlib

def mainPartitioned(partition_length):
    seqList = parse.parse('RNAseqs', 20)
    folded = []
    for RNA in seqList:
        if len(RNA) != 0:
          folded += [fold.Fold(RNA, partition_length)] #with partition, run with different lengths
    return folded

def mainNoPartition():
    seqList = parse.parse('RNAseqs', 20)
    scoredFolded = []
    for RNA in seqList:
        if len(RNA) != 0:
          scoredFolded += [nussinov.FoldAndScore(nussinov.MakeSeq(RNA))] #without partition
    return scoredFolded

def scorePartitioned(folded):
    pass




if __name__ == '__main__':
    import timeit
    t = timeit.Timer(stmt = "mainNoPartition()", setup = "from main import mainNoPartition")
    u = timeit.Timer(stmt = "mainPartitioned(20)", setup = "from main import mainPartitioned")
    print 'Without partioning:', t.timeit(3)
    print 'With partitioning:', u.timeit(3)
