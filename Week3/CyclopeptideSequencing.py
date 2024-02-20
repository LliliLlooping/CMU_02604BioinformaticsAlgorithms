from CycloSpectrum import CycloSpectrum
from LinearSpectrum import LinearSpectrum
from copy import deepcopy
from PeptideScoring import LinearpeptideScoring

EighteenAminoAcidMass = [57, 71, 87, 97, 99, 101, 103, 113, 114,
                         115, 128, 129, 131, 137, 147, 156, 163, 186]


def Expand(candidates, alphabets):
    newCandidates = []
    for candidateList in candidates:
        for alphabet in alphabets:
            newCandidates.append(deepcopy(candidateList))
            newCandidates[-1].append(alphabet)
    return newCandidates


def Mass(peptide):
    return sum(peptide)


def ParentMass(spectrum):
    return max(spectrum)


def Consistent(cycloSpectrum, spectrum):
    cSpecCount = {s: cycloSpectrum.count(s) for s in set(cycloSpectrum)}
    specCount = {s: spectrum.count(s) for s in set(spectrum)}
    uniqueSpectrum = set(specCount.keys())
    for cSpec in cSpecCount.keys():
        if cSpec not in uniqueSpectrum or cSpecCount[cSpec] > specCount[cSpec]:
            return False
    return True


def CyclopeptideSequencing(spectrum, alphabets=EighteenAminoAcidMass):
    finalPeptides = []
    candidates = [[]]
    massSpectrum = ParentMass(spectrum)
    while len(candidates) > 0:
        candidates = Expand(candidates, alphabets)
        peptides = deepcopy(candidates)
        for peptide in peptides:
            massPeptide = Mass(peptide)
            if massPeptide == massSpectrum:
                if CycloSpectrum(peptide) == spectrum and peptide not in finalPeptides:
                    finalPeptides.append(peptide)
                    candidates.remove(peptide)
            elif Consistent(LinearSpectrum(peptide), spectrum) == False:
                candidates.remove(peptide)
    return finalPeptides

######################################################################
########################## Debugging Runs ############################
######################################################################


# print(Expand([[], [57]]))
# print([1, 2, 3] == [1, 2])

# spectrum = [0, 113, 128, 186, 241, 299, 314, 427]
# spectrum = [0, 71, 114, 128, 156, 185, 227, 242, 284, 313, 341, 355, 398, 469]


# with open('input.txt', 'r') as file:
#     data = file.readline()
# spectrum = [eval(i) for i in data.split(' ')]
# # print(len(spectrum), spectrum[0], spectrum[-1])

# output = ""
# results = CyclopeptideSequencing(spectrum)
# print(results)
# for result in results:
#     print(result, LinearpeptideScoring(result, spectrum))
# for resultList in results:
#     for i in range(len(resultList) - 1):
#         output += str(resultList[i]) + '-'
#     output += str(resultList[-1]) + ' '
# print(output[:-1])
