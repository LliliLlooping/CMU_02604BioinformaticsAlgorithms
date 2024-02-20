from CycloSpectrum import CycloSpectrum
from LinearSpectrum import LinearSpectrum


def SimilarityScore(spectrum1, spectrum2):
    score = 0
    uniqueSpec1 = list(set(spectrum1))
    for spec in uniqueSpec1:
        count1, count2 = spectrum1.count(spec), spectrum2.count(spec)
        score += min(count1, count2)

    return score


def CyclopeptideScoring(peptide, spectrum):

    # Turn the peptide into a spetrum
    cycloSpectrum = CycloSpectrum(peptide)

    # Score the peptide's spectrum against the input spectrum
    score = SimilarityScore(cycloSpectrum, spectrum)

    return score


def LinearpeptideScoring(peptide, spectrum):

    # Turn the peptide into a spetrum
    linearSpectrum = LinearSpectrum(peptide)

    # Score the peptide's spectrum against the input spectrum
    score = SimilarityScore(linearSpectrum, spectrum)

    return score


######################################################################
########################## Debugging Runs ############################
######################################################################


# peptide = 'VKLFPWFNQY'
# spectrum = CycloSpectrum(peptide)
# print(len(spectrum))
# spectrum = [0, 97, 97, 129, 129, 194, 203, 226,
#             226, 258, 323, 323, 323, 355, 403, 452]

# spectrum = [0, 99, 113, 114, 128, 227, 257, 299, 355, 356, 370, 371, 484]

# spectrum = [0, 57, 71, 71, 71, 104, 131,
#             202, 202, 202, 256, 333, 333, 403, 404]

# peptide = 'RKCEYRPFFSQQGHMFMQVWHIYIAAVVWDMITAKRALSVQD'
# with open('input.txt', 'r') as file:
#     data = file.readline()
# spectrum = [eval(i) for i in data.split(' ')]
# print(spectrum[0], spectrum[-1])

# print(LinearpeptideScoring(peptide, spectrum))
# print(CyclopeptideScoring(peptide, spectrum))
