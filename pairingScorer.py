bDict = {'A':0, 'T':1, 'C':2, 'G':3}

bondScore = [[0, 0, 0, 1],
             [0, 0, 1, 1],
             [0, 1, 0, 0],
             [1, 1, 0, 0]]

def score(partition):
    firstTuple, secondTuple, seq = partition[0][0], partition[0][1], partition[1]
    score = 0
    secondHalf = xrange(secondTuple[0], secondTuple[1])
    j = -1
    for i in xrange(firstTuple[0], firstTuple[1]):
        score += bondScore[bDict[seq[i]]][bDict[seq[secondHalf[j]]]]
        j -= 1
    return score


                                

    
