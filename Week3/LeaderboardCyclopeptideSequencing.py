from copy import deepcopy
from PeptideScoring import CyclopeptideScoring, LinearpeptideScoring
from CyclopeptideSequencing import ParentMass, Expand, Mass, EighteenAminoAcidMass


def TrimLeaderboard(candidates, spectrum, N):
    scores, results = [], []
    for candidate in candidates:
        scores.append(LinearpeptideScoring(candidate, spectrum))
    descendingScores = sorted(scores)[::-1]
    cutoffScore = descendingScores[:N][-1]
    for i in range(len(scores)):
        if scores[i] >= cutoffScore:
            results.append(candidates[i])
    return results


def LeaderboardCyclopeptideSequencing(spectrum, N, alphabets=EighteenAminoAcidMass):
    candidates = [[]]
    leaderPeptide = []
    leaderboard = []
    leaderScore = -1
    massSpectrum = ParentMass(spectrum)
    while len(candidates) > 0:
        candidates = Expand(candidates, alphabets)
        peptides = deepcopy(candidates)
        for peptide in peptides:
            massPeptide = Mass(peptide)
            if massPeptide == massSpectrum:
                score = CyclopeptideScoring(peptide, spectrum)
                if score >= leaderScore:
                    leaderboard.append((peptide, score))
                    leaderScore = score
                    leaderPeptide = peptide
                    candidates.remove(peptide)
            elif massPeptide > massSpectrum:
                candidates.remove(peptide)
        if len(candidates) > 0:
            candidates = TrimLeaderboard(candidates, spectrum, N)
    leaderboard = sorted(leaderboard, key=lambda x: x[1])[::-1]
    return leaderPeptide, leaderboard

######################################################################
########################## Debugging Runs ############################
######################################################################


# with open('input.txt', 'r') as file:
#     data = file.readline()
# spectrum = [eval(i) for i in data.split(' ')]
# # print(len(spectrum))

# N = 1000

# results, _ = LeaderboardCyclopeptideSequencing(spectrum, N)


# s = ''
# for result in results:
#     for i in range(len(result) - 1):
#         s += str(result[i]) + '-'
#     s += str(result[len(result) - 1]) + ' '

# print(s[:-1])
