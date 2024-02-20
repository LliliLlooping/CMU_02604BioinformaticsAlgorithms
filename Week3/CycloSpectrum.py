
MolecularMass = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'L': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'Q': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}


def CycloSpectrum(peptide):
    """
        Code Challenge: Implement LinearSpectrum.

        Input: An amino acid string Peptide.
        Output: The linear spectrum of Peptide.
    """

    # The input peptide could be a list of integers (mass), or a peptide string.
    # Turn into list of integers.
    massList = []
    if isinstance(peptide, str):
        massList = [MolecularMass[p] for p in peptide]
    else:
        massList = peptide

    prefixMass = [0]
    for i in range(len(peptide)):
        prefixMass.append(prefixMass[i] + massList[i])

    peptideMass = prefixMass[-1]

    CycloSpectrum = [0]
    for i in range(0, len(peptide)):
        for j in range(i+1, len(peptide)+1):
            CycloSpectrum.append(prefixMass[j] - prefixMass[i])
            if i > 0 and j < len(peptide):
                CycloSpectrum.append(
                    peptideMass - (prefixMass[j] - prefixMass[i]))

    return sorted(CycloSpectrum)

######################################################################
########################## Debugging Runs ############################
######################################################################


# peptide = 'NQEL'
# peptide = 'FHYLKVNTQPKIWE'
# results = CycloSpectrum(peptide)
# assert len(results) == len(peptide) * (len(peptide) - 1) + 2
# print(results)


# s = ''
# for result in results:
#     s += str(result) + ' '
# print(s[:-1])
