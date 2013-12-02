import nussinov
import fold
import timeit
import parse
import matplotlib


def mainPartitioned(partition_length):
    seqList = parse.parse(r'C:\Users\LLP-student\Documents\GitHub\rna-folding\RNAseqs')
    folded = []
    for RNA in seqList:
        folded += [fold.Fold(RNA, partition_length)] #with partition, run with different lengths
    return folded

def mainNoPartition():
    seqList = parse.parse(r'C:\Users\LLP-student\Documents\GitHub\rna-folding\RNAseqs')
    scoredFolded = []
    for RNA in seqList:
        scoredFolded += [nussinov.FoldAndScore(RNA)]      #without partition
    return scoredFolded

def scorePartitioned(folded):
    pass


mainNoPartition()
