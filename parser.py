import os
path = r'C:\Users\LLP-student\Documents\6.047\RNAseqs'
data = []
for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        data += [dir_entry_path]

bases = {'g':1, 'a':1, 't':1, 'c':1, 'G':1, 'A':1, 'T':1, 'C':1}

seqList = []
for theFile in data:
    h = open(theFile)
    k = 0
    seq = ""
    for line in h:
        if line[0] in bases:
            seq += line
    seqList += [seq]

