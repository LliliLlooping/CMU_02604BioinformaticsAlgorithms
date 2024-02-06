from typing import List, Dict
import numpy as np


class MotifSearchTools:
    def __init__(self):
        pass

    def calculate_prob(self, window: str, profile: List[Dict[str, float]]) -> float:
        """_summary_

        Args:
            window (str): A string consists of 'A', 'T', 'C', and 'G'.
            profile (dict[k]): {'A': Pa, 'T': Pt, 'C': Pc, 'G': 1-Pa-Pt-Pc}
        Returns:
            prob (float): The probability of this window based on the profile.
        """
        # Get the list of probability for each character in the window
        probList = [profile[i][window[i]] for i in range(len(window))]

        prob = np.prod(probList)

        return prob

    def random_initiate_motifs(self, dnas: List[str], k: int) -> List[str]:

        # Generate a starting random posision for the motif in each ena
        indices = [np.random.randint(low=0, high=len(
            dnas[i]) - k + 1, size=1)[0] for i in range(len(dnas))]

        # Slice the dnas to get the motifs
        result = [dnas[n][idx:idx+k] for n, idx in enumerate(indices)]

        return result

    def generate_profile(self, motifs: List[str]) -> List[Dict[str, float]]:

        numMotif, lenMotif = len(motifs), len(motifs[0])

        # Sets unit increament, given a pseudocount for A, T, C, and G
        u = 1 / (numMotif + 4)

        profile = []
        for i in range(lenMotif):

            # Initialize with pseudocounts
            dic = {'A': u, 'T': u, 'G': u, 'C': u}

            # Count the elements in a column
            for j in range(numMotif):
                dic[motifs[j][i]] += u

            profile.append(dic)

        return profile
