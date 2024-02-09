from AdjacencyList import AdjacencyList
from typing import List, Dict
from copy import deepcopy


class ContigGeneration:

    def __init__(self):
        self.adjacencyList = AdjacencyList()

    def contig_generation(self, patterns: List[str]) -> List[str]:
        """
            Contig Generation Problem: Generate the contigs from a collection of reads (with imperfect coverage).

            Input: A collection of k-mers Patterns.
            Output: All contigs in DeBruijn (Patterns).
        """

        # Construct the De Bruijn graph from patterns
        adjacency_list = self.adjacencyList.construct_from_kmers(patterns)

        # Count the in/out degrees for every node
        degreeCounter = self.adjacencyList.count_degrees(adjacency_list)

        contigs = []

        # Find a valid start.
        node = self._find_start(adjacency_list, degreeCounter)
        while node != 'None':
            # The while loop finds all contigs
            # except independent cycles.

            # Use depth-first search to find contigs
            self._dfs(adjacency_list=adjacency_list, node=node, contigs=contigs,
                      currentPath=node, degreeCounter=degreeCounter)

            # Update the starting point.
            node = self._find_start(adjacency_list, degreeCounter)

        # Find independent cycles
        contigs += self._find_independent_cycle(adjacency_list)

        return contigs

    def _find_start(self, adjacency_list: Dict[any, List[any]], degreeCounter: Dict[any, List[int]]) -> str:
        """
        Find a valid starting point in the graph, or return 'None'
        """

        for k, v in adjacency_list.items():

            if not self._is_one_one(degreeCounter, k) and len(v) > 0:
                return k

        return 'None'

    def _is_one_one(self, degreeCounter: Dict[any, List[int]], node: any) -> bool:

        counter = degreeCounter[node]

        return counter[0] == 1 and counter[1] == 1

    def _dfs(self, adjacency_list: Dict[any, List[any]], node: any, contigs: List[str], currentPath: str, degreeCounter: Dict[any, List[int]]):

        # If the node has no outbounding edges, the path reaches an end
        if node not in adjacency_list or len(adjacency_list[node]) == 0:
            contigs.append(currentPath)
            return

        # For all outbounding edges
        outboundingEdges = deepcopy(adjacency_list[node])
        for destination in outboundingEdges:

            # Update the outbounding list
            adjacency_list[node].remove(destination)

            # If the destination node is one-one, keep extending
            # End, otherwise
            if not self._is_one_one(degreeCounter, destination):
                contigs.append(currentPath + destination[-1])
            else:
                self._dfs(adjacency_list, destination, contigs, currentPath +
                          destination[-1], degreeCounter)

    def _find_independent_cycle(self, adjacency_list: Dict[any, List[any]]) -> List[str]:
        """
            Find pure independent cycle from the adjacency list of a directed graph.
            Intend to use after find all other paths.
        """

        cycles = []

        # Count the number of remaining edges in the graph
        # It's guaranteed that all remaining edges are part of a pure independent cycle.
        edgeCounter = self.adjacencyList.count_edges(adjacency_list)

        while edgeCounter > 0:
            for k, v in adjacency_list.items():
                if len(v) > 0:
                    # When spot a node with outbounding edge(s)

                    # Generate cycle from this node
                    patterns = self._generate_cycleenerateCycle(
                        adjacency_list, k)

                    # Update the number of remaining edges
                    edgeCounter -= len(patterns)

                    # Add the starting point the the kmer list again st. it looks like a loop
                    patterns.append(patterns[0])

                    # Glue the kmer list
                    cycle = patterns[0] + \
                        ''.join([p[-1] for p in patterns[1:]])
                    cycles.append(cycle)

        return cycles

    def _generate_cycle(self, adjacency_list: Dict[any, List[any]], node: any) -> List[str]:
        """
            Find a cycle starting from 'node' in graph 'g'
        """

        cycle = [node]

        while len(adjacency_list[cycle[-1]]) > 0:
            # While the current node still has outbounding edges

            # Add the next node to the cycle
            cycle.append(adjacency_list[cycle[-1]][0])

            # Update the adjacency list and,
            # If already form a cycle, break.
            if adjacency_list[cycle[-1]][0] in cycle:
                adjacency_list[cycle[-1]] = []
                break
            else:
                adjacency_list[cycle[-1]] = []

        return cycle

    def test(self):
        patterns = ['ATG', 'ATG', 'TGT', 'TGG', 'CAT', 'GGA', 'GAT', 'AGA']
        contigs = self.contig_generation(patterns)
        print(contigs)
