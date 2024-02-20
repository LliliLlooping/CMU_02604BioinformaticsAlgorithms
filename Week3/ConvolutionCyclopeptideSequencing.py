from SpectralConvolution import SpectralConvolution
from LeaderboardCyclopeptideSequencing import LeaderboardCyclopeptideSequencing


def ConvolutionCyclopeptideSequencing(M, N, spectrum):
    convolution = SpectralConvolution(spectrum)
    uniqueConvolution = set(convolution)
    convolutionCount = {}
    for s in uniqueConvolution:
        if s >= 57 and s <= 200:
            convolutionCount[s] = convolution.count(s)
    convolutionCount = sorted(convolutionCount.items(),
                              key=lambda x: x[1])[::-1]
    cutoffScore = convolutionCount[M-1][1]
    alphabet = []
    for pair in convolutionCount:
        if pair[1] >= cutoffScore:
            alphabet.append(pair[0])
    alphabet = sorted(alphabet)

    result, leaderboard = LeaderboardCyclopeptideSequencing(
        spectrum, N, alphabet)

    return result, leaderboard


######################################################################
########################## Debugging Runs ############################
######################################################################
# with open('input.txt', 'r') as file:
#     data = file.readline()
# spectrum = [eval(i) for i in data.split(' ')]

# result, leaderboard = ConvolutionCyclopeptideSequencing(20, 1000, spectrum)


# leaderboard = leaderboard[:86]
# print(len(leaderboard))

# for i, l in enumerate(leaderboard):
#     print(i, l)

# s = ''
# for l in leaderboard:
#     for i in range(len(l[0]) - 1):
#         s += str(l[0][i]) + '-'
#     s += str(l[0][len(l[0]) - 1]) + ' '

# print(s[:-1])
