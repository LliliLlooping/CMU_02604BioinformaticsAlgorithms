from TwoBreak import TwoBreak

class ShortestRearrangementScenario:

    def __init__(self):
        self.twoBreak= TwoBreak()
    
    def solve_shortest_rearrangement_scenario(self, P, Q):

        record = [P]
        
        # find a two-break
        (i_1, i_2, i_3, i_4) = self.identify_breaks(P, Q)

        while i_1 != -1: # while we still have a valid two-break

            # do the two-break
            P = self.twoBreak.two_break_on_genome(P, i_1, i_2, i_3, i_4)
            record.append(P)

            # find next two-break
            (i_1, i_2, i_3, i_4) = self.identify_breaks(P, Q)

        return record


    def identify_breaks(self, P, Q):

        # turn genome into graph
        red_edges, blue_edges = self.twoBreak.genome_to_graph(P), self.twoBreak.genome_to_graph(Q)

        # select an arbitrary blue edge in a non-trivial alternating red-blue cycle and
        # perform the 2-break on the two red edges flanking this blue edge
        for edge in blue_edges:

            b1, b2 = edge[0], edge[1]

            r1, r2 = self._find_neighbor(red_edges, b1), self._find_neighbor(red_edges, b2)

            if b2 != r1:
                return b1, r1, b2, r2
            
        return -1, -1, -1, -1
    
    def _find_neighbor(self, edges, node):

        for edge in edges:

            if edge[0] == node:
                return edge[1]
            
            elif edge[1] == node:
                return edge[0]
        
    def test(self):
        P =  [[1, 2, 3, 4, 5, 6]]
        Q = [[1, -3, -6, -5], [2, -4]]
        print(self.solve_shortest_rearrangement_scenario(P, Q))