from LimbLengthProblem import LimbLengthProblem
from typing import List, Dict


class AdditivePolygeny2:
    def __init__(self):
        self.limb = LimbLengthProblem()

    def construct_simple_tree_from_distance_matrix(self, input_dist_matrix: List[List[int]]):

        # the idx of the next auxiliary node / internal node
        next_internal_node = len(input_dist_matrix)

        # recording current edges
        current_adjacency_list: Dict[int, int[2]] = {}

        self._construct_simple_tree_from_distance_matrix_util(
            input_dist_matrix, current_adjacency_list, next_internal_node)

        result = [(ori, des, weight) for (ori, [des, weight]) in sorted(
            current_adjacency_list.items(), key=lambda x: x[0]) if ori < des]

        return result

    def _construct_simple_tree_from_distance_matrix_util(self, input_dist_matrix, current_adjacency_list, next_internal_node):

        n = len(input_dist_matrix)

        if n == 2:
            self._add_edge(current_adjacency_list, 0,
                           1, input_dist_matrix[0][1])
            return next_internal_node

        limb_length = self.limb.solve_limb_length(n-1, input_dist_matrix)

        (i, k, distance_from_i) = self._find_two_leaves(
            input_dist_matrix, n, limb_length)

        input_dist_matrix = [input_dist_matrix[i][:-1]
                             for i in range(len(input_dist_matrix) - 1)]

        next_internal_node = self._construct_simple_tree_from_distance_matrix_util(
            input_dist_matrix, current_adjacency_list, next_internal_node)

        i_hanger, k_hanger = current_adjacency_list[i][0], current_adjacency_list[k][0]

        limb_length_i = current_adjacency_list[i][1]
        if limb_length_i > distance_from_i:
            self._add_edge(current_adjacency_list, i,
                           next_internal_node, distance_from_i)
            self._add_edge(current_adjacency_list, i_hanger,
                           next_internal_node, limb_length_i - distance_from_i)
        else:
            self._add_edge(current_adjacency_list, k_hanger,
                           next_internal_node, current_adjacency_list[k][1] - (input_dist_matrix[i][k] - distance_from_i))
            self._add_edge(current_adjacency_list, k,
                           next_internal_node, input_dist_matrix[i][k] - distance_from_i)

        self._add_edge(current_adjacency_list, n-1,
                       next_internal_node, limb_length)

        return next_internal_node + 1

    def _find_two_leaves(self, input_dist_matrix, n, limb_length):

        for j in range(n-1):
            input_dist_matrix[j][n-1] -= limb_length
            input_dist_matrix[n-1][j] = input_dist_matrix[j][n-1]

        i = 0
        flag = False

        while i < n-2:

            k = i + 1
            while k < n-1:

                if input_dist_matrix[i][k] == input_dist_matrix[i][n-1] + input_dist_matrix[k][n-1]:
                    flag = True
                    break

                k += 1

            if flag:
                break

            i += 1

        distance_from_i = input_dist_matrix[i][n-1]

        for j in range(n-1):
            input_dist_matrix[j][n-1] += limb_length
            input_dist_matrix[n-1][j] = input_dist_matrix[j][n-1]

        return (i, k, distance_from_i)

    def _sorted_tuple(self, node_1, node_2):
        if node_1 < node_2:
            return (node_1, node_2)
        else:
            return (node_2, node_1)

    def _add_edge(self, adjacency_list, node_1, node_2, weight):

        adjacency_list[node_1] = [node_2, weight]

        adjacency_list[node_2] = [node_1, weight]

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
