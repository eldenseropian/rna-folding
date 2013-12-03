import unittest

import parse

class ParseTests(unittest.TestCase):

    def testEqual(self):
        parsedSeq = parse.parse('RNAseqs', 1)[0]
        trueSeq = "GAGGAAAGUCCGGGCUCCAUAGGGCAAAGUGCCAGGUAACGCCUGGGAGGCGU" \
                  "GAGCCUACGGAAAGUGCCACAGAAAAUAACCGCCUAAGCGCUUCGGCGCCGGUA" \
                  "AGGGUGAAAAGGUGCGGUAAGAGCGCACCGCACGGCUGGCAACAGUUCGUGGCU" \
                  "AGGUAAACCCCACUUGGAGCAAGACCAAAUAGGGAUCCAUCGGCGUGGCCCGCG" \
                  "CUGGAUCCGGGUAGGUUGCUAGAGGCGGUCAGCGAUGGCCGUCGUAGAGGAAUGG" \
                  "CUGUCCUCGACAGAACCCGGCUUA"
        self.assertEqual(parsedSeq, trueSeq)
        
