from LimbLengthProblem import LimbLengthProblem


class AdditivePolygeny:
    def __init__(self):
        self.limb = LimbLengthProblem()

    def construct_simple_tree_from_distance_matrix(self, DistMatrix):
        weightedEdges = {}
        next_auxiliary_node = len(DistMatrix)
        leaf_hanger = {}
        _ = self.construct_simple_tree_from_distance_matrix_util(
            DistMatrix, weightedEdges, next_auxiliary_node, leaf_hanger)
        return [(ori, des, weight) for ((ori, des), weight) in sorted(weightedEdges.items(), key=lambda x: x[0][0])]

    def construct_simple_tree_from_distance_matrix_util(self, DistMatrix, weightedEdges, next_auxiliary_node, leaf_hanger):
        n = len(DistMatrix)
        if n == 2:
            leaf_hanger[0] = 1
            leaf_hanger[1] = 0
            weightedEdges[(0, 1)] = DistMatrix[0][1]
            return next_auxiliary_node
        limb_length = self.limb.solve_limb_length(n-1, DistMatrix)
        for j in range(n-1):
            DistMatrix[j][n-1] -= limb_length
            DistMatrix[n-1][j] = DistMatrix[j][n-1]
        i = 0
        flag = False
        while i < n-2:
            k = i + 1
            while k < n-1:
                if DistMatrix[i][k] == DistMatrix[i][n-1] + DistMatrix[k][n-1]:
                    flag = True
                    break
                k += 1
            if flag:
                break
            i += 1
        x = DistMatrix[i][n-1]
        for j in range(n-1):
            DistMatrix[j][n-1] += limb_length
            DistMatrix[n-1][j] = DistMatrix[j][n-1]
        DistMatrix = [DistMatrix[i][:-1]for i in range(len(DistMatrix) - 1)]
        next_auxiliary_node = self.construct_simple_tree_from_distance_matrix_util(
            DistMatrix, weightedEdges, next_auxiliary_node, leaf_hanger)

        if weightedEdges[self._sorted_tuple(i, leaf_hanger[i])] > x:
            weightedEdges[self._sorted_tuple(i, next_auxiliary_node)] = x
            weightedEdges[self._sorted_tuple(
                leaf_hanger[i], next_auxiliary_node)] = weightedEdges[self._sorted_tuple(i, leaf_hanger[i])] - x
            del weightedEdges[self._sorted_tuple(i, leaf_hanger[i])]
            if leaf_hanger[i] in leaf_hanger:
                leaf_hanger[leaf_hanger[i]] = next_auxiliary_node
            leaf_hanger[i] = next_auxiliary_node
        else:
            weightedEdges[self._sorted_tuple(k, next_auxiliary_node)
                          ] = DistMatrix[i][k] - x
            weightedEdges[self._sorted_tuple(leaf_hanger[k], next_auxiliary_node)] = weightedEdges[self._sorted_tuple(
                k, leaf_hanger[k])] - weightedEdges[self._sorted_tuple(k, next_auxiliary_node)]
            del weightedEdges[self._sorted_tuple(k, leaf_hanger[k])]
            if leaf_hanger[k] in leaf_hanger:
                leaf_hanger[leaf_hanger[k]] = next_auxiliary_node
            leaf_hanger[k] = next_auxiliary_node
        weightedEdges[self._sorted_tuple(
            n-1, next_auxiliary_node)] = limb_length
        leaf_hanger[n-1] = next_auxiliary_node
        return next_auxiliary_node + 1

    def _sorted_tuple(self, node_1, node_2):
        if node_1 < node_2:
            return (node_1, node_2)
        else:
            return (node_2, node_1)

    def test(self):
        # D = [
        #     [0, 2],
        #     [2, 0]
        # ]
        # D = [
        #     [0, 13, 21, 22],
        #     [13, 0, 12, 13],
        #     [21, 12, 0, 13],
        #     [22, 13, 13, 0]
        # ]
        # D = [
        #     [0, 2, 3, 3],
        #     [2, 0, 3, 3],
        #     [3, 3, 0, 2],
        #     [3, 3, 2, 0]
        # ]
        D = [
            [0, 3, 7, 16],
            [3, 0, 8, 17],
            [7, 8, 0, 13],
            [16, 17, 13, 0]
        ]
        print(self.construct_simple_tree_from_distance_matrix(D))
