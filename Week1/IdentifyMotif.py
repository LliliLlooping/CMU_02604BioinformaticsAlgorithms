from typing import List, Dict
from MotifSearchTools import MotifSearchTools


class IdentifyMotif:

    def __init__(self):
        self.motif_search_tools = MotifSearchTools()

    def profile_most_probable_kmer(self, text, k, profile):
        """
            Identifies the most probable k-mer according to a given profile matrix.

            The profile matrix is represented as a list of columns, where the i-th element is a map
            whose keys are strings ("A", "C", "G", and "T") and whose values represent the probability
            associated with this symbol in the i-th column of the profile matrix.
        Args:
            text (str): A string consists of 'A', 'T', 'C', and 'G'
            k (int): The k-mer length
            profile (dict[k]): {'A': Pa, 'T': Pt, 'C': Pc, 'G': 1-Pa-Pt-Pc}
        Returns:
            window (str): The most probable k-mer.
        """

        # Initializes 'bestProb' and 'bestWindow'
        bestWindow = text[0: k]
        bestProb = self.motif_search_tools.calculate_prob(bestWindow, profile)

        # Iterate over possible windows
        for idx in range(1, len(text) - k + 1):

            window = text[idx: idx + k]
            windowProb = self.motif_search_tools.calculate_prob(
                window, profile)

            # If finds better window, updates 'bestProb' and 'bestWindow'
            if windowProb > bestProb:
                bestProb = windowProb
                bestWindow = window

        return bestWindow

    def find_best_motifs(self, profile: List[Dict[str, float]], dnas: List[str]) -> List[str]:
        """
            Find motif for multiple dnas.
        """
        motifs = []
        for i in range(len(dnas)):
            motif = self.profile_most_probable_kmer(
                dnas[i], len(profile), profile)
            motifs.append(motif)
        return motifs

    def test(self):
        text = 'ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT'
        k = 5
        profile = [
            {'A': 0.2, 'C': 0.4, 'G': 0.3, 'T': 0.1},
            {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2},
            {'A': 0.3, 'C': 0.1, 'G': 0.5, 'T': 0.1},
            {'A': 0.2, 'C': 0.5, 'G': 0.2, 'T': 0.1},
            {'A': 0.3, 'C': 0.1, 'G': 0.4, 'T': 0.2}
        ]
        bestWindow = self.profile_most_probable_kmer(text, k, profile)
        assert bestWindow == 'CCGAG'
