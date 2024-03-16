from typing import List, Tuple

class TwoBreak:

    def __init__(self):
        pass

    def two_break_on_genome(self, genome: List[List[int]], i_1: int, i_2: int, i_3: int, i_4: int):
        
        # turn genome into genome graph
        genome_graph = self.genome_to_graph(genome)
        
        # do a single two-break on the genome graph
        breaked_graph = self.two_break_on_genome_graph(genome_graph, i_1, i_2, i_3, i_4)

        # turn the genome graph back to genome
        breaked_genome = self.graph_to_genome(breaked_graph)

        return breaked_genome

    def genome_to_graph(self, genome: List[List[int]]):

        edges = []

        for cycle in genome:
            edges += self._single_genome_to_graph(cycle)

        return edges
    
    def _single_genome_to_graph(self, cycle: List[int]):

        colored_edges = []

        len_genome = len(cycle)
        for i in range(len_genome):

            n1, n2 = cycle[i], cycle[(i + 1) % len_genome]

            if n1 > 0 and n2 > 0:
                colored_edges.append((2 * n1, 2 * n2 - 1))

            elif n1 > 0 and n2 < 0:
                colored_edges.append((2 * n1, 2 * -n2))
                
            elif n1 < 0 and n2 > 0:
                colored_edges.append((2 * -n1 - 1, 2 * n2 - 1))

            elif n1 < 0 and n2 < 0:
                colored_edges.append((2 * -n1 - 1, 2 * -n2))
        
        return colored_edges

    def two_break_on_genome_graph(self, genome_graph: List[Tuple[int, int]], i_1: int, i_2: int, i_3: int, i_4: int):
        
        if (i_1, i_2) in genome_graph:
            genome_graph.remove((i_1, i_2))
        else:
            genome_graph.remove((i_2, i_1))

        if (i_3, i_4) in genome_graph:
            genome_graph.remove((i_3, i_4))
        else:
            genome_graph.remove((i_4, i_3))

        genome_graph.append((i_1, i_3))

        genome_graph.append((i_2, i_4))

        return genome_graph
    
    
    def graph_to_genome(self, colored_edges: List[Tuple[int, int]]):

        genome = []

        while len(colored_edges) > 0:

            cycle = []

            [i, j] = colored_edges[0]

            while i !=  -1:

                if j % 2 == 0:
                    cycle.append(-j // 2)
                    self._remove_edge(colored_edges, (i, j))
                    [i, j] = self._find_next(colored_edges, j - 1)

                else:
                    cycle.append((j + 1) // 2)
                    self._remove_edge(colored_edges, (i, j))
                    [i, j] = self._find_next(colored_edges, j + 1)
                
            genome.append(cycle)

        return genome
            
    def _find_next(self, genome_graph, x):

        for item in genome_graph:

            if item[0] == x:
                return [item[0], item[1]]
            
            elif item[1] == x:
                return [item[1], item[0]]
            
        return [-1, -1]  
      
    def _remove_edge(self, genome_graph, edge):

        if edge in genome_graph:
            genome_graph.remove(edge)

        else:
            genome_graph.remove((edge[1], edge[0]))
            
        return

    def test(self):

        i_1, i_2, i_3, i_4 = 1, 6, 3, 8

        genome = [[1, -2, -4, 3]]

        result = self.two_break_on_genome(genome, i_1, i_2, i_3, i_4)

        print(result)
        
        
        
                            