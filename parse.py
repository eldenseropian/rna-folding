import os

bases = {'g':1, 'a':1, 't':1, 'c':1, 'G':1, 'A':1, 'T':1, 'C':1}
lowercase = {'g':1, 'a':1, 't':1, 'c':1}

"""
Takes in a path to a directory, then opens each file in the
directory (presumed to be a in .dp format) and parses out the RNA
sequence. Returns a list of all RNA sequences as strings.
"""
def parse(path, numRNA):
    ##finds all files in directory
    data = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            data += [dir_entry_path]

    ##opens each file and parses for RNA sequence
    seqList = []
    for theFile in data[:numRNA]:
        h = open(theFile)
        k = 0
        seq = []
        for line in h:
            if line[0] in bases:
                for letter in line:
                    if letter in lowercase:
                        seq += [letter.capitalize()]
                    else:
                        seq += [letter]
            strSeq = ''.join(seq)
        seqList += [strSeq]
    return seqList
