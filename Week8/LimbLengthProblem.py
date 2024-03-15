
class LimbLengthProblem:
    def __init__(self):
        pass

    def solve_limb_length(self, j, DistMatrix):
        n = len(DistMatrix)
        if n <= 1:
            return 0
        elif n == 2:
            return DistMatrix[0][1]
        possibilities = []
        for p in range(n):
            if p == j:
                continue
            for q in range(p+1, n):
                if q == j:
                    continue
                possibilities.append(
                    DistMatrix[j][p] + DistMatrix[j][q] - DistMatrix[p][q])
        return min(possibilities) // 2
