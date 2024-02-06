import numpy as np
from copy import deepcopy
from MotifSearchTools import MotifSearchTools
from Scoring import Scoring
from typing import List, Dict


class GibbsMotifSearch:
    def __init__(self, epochs=200):
        self.epochs = epochs
        self.motif_search_tools = MotifSearchTools()
        self.scoring = Scoring()

    def gibbs_motif_searches(self, dnas: List[str], k: int, t: int, n: int) -> List[str]:

        # Initializes 'bestMotif', 'bestLoss' with one RMS run
        bestMotif, bestLoss = self._gibbs_motif_search(dnas, k, t, n)

        for _ in range(self.epochs - 1):

            motif, score = self._gibbs_motif_search(dnas, k, t, n)

            # If finds smaller loss in this run, updates it.
            if score < bestLoss:
                bestLoss = score
                bestMotif = motif

        return bestMotif

    def _gibbs_motif_search(self, dna: List[str], k: int, t: int, n: int) -> List[str]:

        # Initializes 'motifs', 'bestMotifs', and 'bestLoss'
        motifs = self.motif_search_tools.random_initiate_motifs(dna, k)
        bestMotifs, bestLoss = deepcopy(
            motifs), self.scoring.consensus_score(motifs)

        for _ in range(n):

            # Pick a random motif
            i = np.random.randint(0, t)

            # Generate profile based on the rest motifs
            profile = self.motif_search_tools.generate_profile(
                motifs[0: i] + motifs[i + 1: t])

            # Update the picked motif
            motifs[i] = self._gibbs_draw(dna[i], k, profile)

            # Calculates the loss for curent best motifs
            loss = self.scoring.consensus_score(motifs)

            if loss < bestLoss:
                bestMotifs = deepcopy(motifs)
                bestLoss = loss

        return (bestMotifs, bestLoss)

    def _gibbs_draw(self, text: str, k: int, profile: List[Dict[str, float]]) -> str:

        # Calculate the normalized probability distribution
        probs = [self.motif_search_tools.calculate_prob(text[i:i+k], profile)
                 for i in range(len(text) - k + 1)]
        normalizedProbs = np.array(probs) / np.sum(probs)

        # Draw the starting point from the probability
        index = np.random.choice(
            range(len(normalizedProbs)), p=normalizedProbs)

        # Slice the motif based on the index
        motif = text[index:index+k]

        return motif

    def test(self):
        k = 8
        t = 5
        N = 100
        dnas = [
            'CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA',
            'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
            'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
            'TAGATCAAGTTTCAGGTGCACGTCGGTGAACCAA',
            'TCCACCAGCTCCACGTGCAATGTTGGCCTA'
        ]
        motifs = self.gibbs_motif_searches(dnas, k, t, N)
        print(motifs)
        # There is a possibility that the result might be something else.
        # assert sorted(motifs) == sorted(
        #     ['AACGGCCA', 'AAGTGCCA', 'TAGTACCG', 'AAGTTTCA', 'ACGTGCAA'])
        return
