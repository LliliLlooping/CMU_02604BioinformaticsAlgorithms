import numpy as np
from typing import List


class Scoring:
    def __init__(self):
        self.alphabets = ['A', 'T', 'C', 'G']

    def consensus_score(self, motifs: List[str]):
        consensusList = []
        for i in range(len(motifs[0])):

            # Extract a column
            tokens = [motifs[j][i] for j in range(len(motifs))]

            # Count 'A', 'T', 'C', 'G' in the column
            tokenCounts = [tokens.count(s)
                           for s in self.alphabets if s in tokens]

            # Count the number of outliers in the column
            consensusList.append(np.sum(tokenCounts) - np.max(tokenCounts)
                                 )
        return np.mean(consensusList)
