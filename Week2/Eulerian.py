from typing import Dict, List, Tuple
import numpy as np
from AdjacencyList import AdjacencyList


class Eulerian:

    def __init__(self):
        self.adjacencyList = AdjacencyList()

    def find_eulerian_path(self, adjacency_list: Dict[int, List[int]]) -> List[int]:
        """ Find the Eulerian Path in the graph.
            The graph is strongly connected, all nodes are balanced, except the starting and ending nodes.

        Args:
            adjacency_list (Dict[str, str]): The adjacency list of the graph.

        Returns:
            List[int]: The Eulerian path.
        """

        # Find the unbalanced node
        (s, t) = self._find_start_end_from_adjacency_list(adjacency_list)

        # Add an edge from t to s, making it a cycle
        self._turn_path_into_cycle(adjacency_list, s, t)

        # Find the eulerian cycle, but remove the repeating node at the end
        eulerian_cycle = self.find_eulerian_cycle(adjacency_list)[:-1]

        # Find the starting position in the cycle
        s_index = self._find_start_end_from_cycle(eulerian_cycle, s, t)

        # Align the cycle to the right position
        eulerian_path = eulerian_cycle[s_index:] + eulerian_cycle[:s_index]

        return eulerian_path

    def _find_start_end_from_adjacency_list(self, adjacency_list: Dict[int, List[int]]) -> Tuple[int]:

        # Count in/out degrees
        degree_counts = self.adjacencyList.count_degrees(adjacency_list)

        # Identify the start/end
        for k, v in degree_counts.items():

            if v[0] < v[1]:
                s = k

            elif v[0] > v[1]:
                t = k

        return (s, t)

    def _find_start_end_from_cycle(self, cycle: List[int], s: int, t: int) -> int:

        # Find all occurence for s and t
        s_index_list, t_index_list = np.where(np.array(cycle) == s)[
            0], np.where(np.array(cycle) == t)[0]

        # Find the s that appears after t
        s_index = [s_index for s_index in s_index_list if (
            s_index - 1) % len(cycle) in t_index_list][0]

        return s_index

    def _turn_path_into_cycle(self, adjacency_list: Dict[int, List[int]], s: int, t: int):
        """ Add an edge from t to s.

        """

        if t not in adjacency_list:
            adjacency_list[t] = []

        adjacency_list[t].append(s)

    def find_eulerian_cycle(self, adjacency_list: Dict[int, List[int]]) -> List[int]:
        """ Find the Eulerian Cycle in the graph.
            Theorem: Every balanced, strongly connected graph is Eulerian.
        Args:
            adjacency_list (Dict[str, str]): The adjacency list of the graph.

        Returns:
            List[int]: The Eulerian cycle.
        """

        # Initializes a random starting node
        next_starting_node = np.random.choice(list(adjacency_list.keys()))

        # Initializes a cycle
        eulerian_cycle = self._find_cycle(adjacency_list, next_starting_node)

        # Count the remaining edge
        remainingEdges = self.adjacencyList.count_edges(adjacency_list)

        # Until visits all edges
        while remainingEdges > 0:

            # Find the next potential starting nodes, i.e.
            # the nodes on current cycle that still have outbounding edges
            potential_starting_nodes = [i for i, node in enumerate(
                eulerian_cycle) if len(adjacency_list[node]) > 0]
            next_starting_node_index = np.random.choice(
                potential_starting_nodes)
            next_starting_node = eulerian_cycle[next_starting_node_index]

            # Generates the next cycle
            cycle = self._find_cycle(adjacency_list, next_starting_node)

            # Updates the remaining edge
            remainingEdges -= len(cycle)

            # Merges the new and the old cycles
            eulerian_cycle = eulerian_cycle[next_starting_node_index:] + \
                eulerian_cycle[:next_starting_node_index]
            eulerian_cycle += cycle

        eulerian_cycle.append(eulerian_cycle[0])

        return eulerian_cycle

    def _find_cycle(self, adjacency_list: Dict[int, List[int]], starting_node: int):
        """
            The graph is guaranteed to be balanced and strongly connected.
        """

        # Initialize the cycle
        cycle = [starting_node]

        # The destinations from the current node
        destinations = adjacency_list[cycle[-1]]

        while len(destinations) > 0:

            current_node = cycle[-1]

            # Picks a destination
            next_node = np.random.choice(destinations)

            # Record this edge in the cycle
            cycle.append(next_node)

            # Removes the edge from the graph
            adjacency_list[current_node].remove(next_node)

            # Exits when comes back to the starting node
            if next_node == cycle[0]:
                return cycle[:-1]

            # If continues, updates the destinations
            destinations = adjacency_list[cycle[-1]]

    def test(self):
        # adjacency_list = {
        #     0: [3],
        #     1: [0],
        #     2: [1, 6],
        #     3: [2],
        #     4: [2],
        #     5: [4],
        #     6: [5, 8],
        #     7: [9],
        #     8: [7],
        #     9: [6]
        # }
        # cycle = self.find_eulerian_cycle(adjacency_list)
        # print(cycle)

        adjacency_list = self.adjacencyList._read_edges('./input_eulerian.txt')
        path = self.find_eulerian_path(adjacency_list)
        print(path)
