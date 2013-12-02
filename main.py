import nussinov
import fold
import parse
import matplotlib


def mainPartitioned(partition_length):
    seqList = parse.parse(r'C:\Users\LLP-student\Documents\GitHub\rna-folding\RNAseqs', 20)
    folded = []
    for RNA in seqList:
        folded += [fold.Fold(RNA, partition_length)] #with partition, run with different lengths
    return folded

def mainNoPartition():
    seqList = parse.parse(r'C:\Users\LLP-student\Documents\GitHub\rna-folding\RNAseqs', 20)
    scoredFolded = []
    for RNA in seqList:
        scoredFolded += [nussinov.FoldAndScore(RNA)] #without partition
    return scoredFolded

def scorePartitioned(folded):
    pass




if __name__ == '__main__':
    import timeit
    t = timeit.Timer(stmt = "mainNoPartition()", setup = "from main import mainNoPartition")
    u = timeit.Timer(stmt = "mainPartitioned(20)", setup = "from main import mainPartitioned")
    print t.timeit(3)
    print u.timeit(3)
