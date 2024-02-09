from typing import List, Dict


class AdjacencyList:
    def __init__(self):
        pass

    def construct_from_kmers(self, kmers: List[str]) -> Dict[str, str]:

        # Initializes the dictionary
        adjacency_list = {}

        # Iterates over all input kmers
        for kmer in kmers:

            # Slices the prefix and suffix
            prefix, suffix = kmer[:-1], kmer[1:]

            # Adds the prefix as a starting node
            if prefix not in adjacency_list:
                adjacency_list[prefix] = []

            # Stores the edge 'prefix -> suffix;
            adjacency_list[prefix].append(suffix)

        return adjacency_list

    def count_edges(self, adjacency_list: Dict[any, List[any]]) -> int:

        # Guaranteed no independent node.

        num_edges = sum([len(v)for v in adjacency_list.values()])

        return num_edges

    def count_degrees(self, adjacency_list: Dict[any, List[any]]) -> Dict[any, List[int]]:
        """ Count degrees for every vertex.
        """

        degree_counts = {}

        for ori, des_list in adjacency_list.items():

            if ori not in degree_counts:
                degree_counts[ori] = [0, 0]
            degree_counts[ori][1] += len(des_list)

            for des in des_list:
                if des not in degree_counts:
                    degree_counts[des] = [0, 0]
                degree_counts[des][0] += 1

        return degree_counts

    def _read_edges(self, file_path: str) -> Dict[any, List[any]]:
        """ Utility I/O function that reads from the input
        """

        with open(file_path, 'r') as file:
            data = file.read().split('\n')

        adjacency_list = {}

        for line in data:

            line_ = line.split(': ')

            ori, des_list = int(line_[0]), line_[1].split(' ')

            if ori not in adjacency_list:
                adjacency_list[ori] = []

            for des in des_list:
                adjacency_list[ori].append(int(des))

        return adjacency_list

    def test(self):
        adjacency_list = {
            0: [3],
            1: [0],
            2: [1, 6],
            3: [2],
            4: [2],
            5: [4],
            6: [5, 8],
            7: [9],
            8: [7],
            # 9: [6]
        }
        num_nodes = self.count_edges(adjacency_list)
        assert num_nodes == 11
