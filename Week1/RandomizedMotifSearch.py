from typing import List
import numpy as np
from MotifSearchTools import MotifSearchTools
from IdentifyMotif import IdentifyMotif
from Scoring import Scoring


class RandomizedMotifSearch:
    def __init__(self, epochs=1000):
        self.epochs = epochs
        self.motif_search_tools = MotifSearchTools()
        self.identify_motif = IdentifyMotif()
        self.scoring = Scoring()

    def randomized_motif_searches(self, dnas: str, k: int, t: int) -> List[str]:
        """

        Args:
            dna (str): A string consists of 'A', 'T', 'C', and 'G'
            k (int): k-mer length
            t (_type_): Run the full RMS algorithm for t times

        Returns:
            bestMotif: a list of motifs
        """

        # Initializes 'bestMotif', 'bestLoss' with one RMS run
        bestMotif, bestLoss = self._randomized_motif_search(dnas, k)

        for _ in range(self.epochs - 1):

            motif, loss = self._randomized_motif_search(dnas, k)

            # If finds smaller loss in this run, updates it.
            if loss < bestLoss:
                bestMotif = motif
                bestLoss = loss

        return bestMotif

    def _randomized_motif_search(self, dnas: str, k: int) -> (List[str], float):

        # Initializes 'motifs', 'bestMotifs', and 'bestLoss'
        motifs = self.motif_search_tools.random_initiate_motifs(dnas, k)
        bestMotifs, bestLoss = motifs, self.scoring.consensus_score(motifs)

        while True:

            # Generate profile based on current motifs
            profile = self.motif_search_tools.generate_profile(motifs)

            # Finds best motifs based on current profile
            motifs = self.identify_motif.find_best_motifs(profile, dnas)

            # Calculates the loss for curent best motifs
            loss = self.scoring.consensus_score(motifs)

            # Updates the best, or exits.
            if loss < bestLoss:
                bestLoss = loss
                bestMotifs = motifs
            else:
                return (bestMotifs, bestLoss)

    def test(self):
        k = 8
        t = 5
        dnas = [
            'CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA',
            'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
            'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
            'TAGATCAAGTTTCAGGTGCACGTCGGTGAACCAA',
            'TCCACCAGCTCCACGTGCAATGTTGGCCTA'
        ]
        motifs = self.randomized_motif_searches(dnas, k, t)
        assert sorted(motifs) == sorted(['TCTCGGGG', 'CCAAGGTG',
                                         'TACAGGCG', 'TTCAGGTG', 'TCCACGTG'])
        return
