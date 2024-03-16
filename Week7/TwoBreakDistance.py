import numpy as np
import sys
sys.setrecursionlimit(32768)

class TwoBreakDistance:
     
    def __init__(self):
        pass
    
    def calculate_two_breaks_distance(self, p, q):

        adjacency_list = {}
        
        for cycle in p:
            l = len(cycle)
            for i in range(l):
                
                ori = int(cycle[i])
                des = int(cycle[(i+1)%l])
                
                if ori not in adjacency_list:
                    adjacency_list[ori] = []
                if -des not in adjacency_list[ori]:
                    adjacency_list[ori].append(-des)
                
                adjacency_list[-des] = []
                adjacency_list[-des].append(ori)
                
        for cycle in q:
            l = len(cycle)
            for i in range(l):
                
                ori = int(cycle[i])
                des = int(cycle[(i+1)%l])
                
                if ori not in adjacency_list:
                    adjacency_list[ori] = []
                adjacency_list[ori].append(-des)
                
                if -des not in adjacency_list:
                    adjacency_list[-des] = []
                adjacency_list[-des].append(ori)
        print(adjacency_list)
        num_cycles = self.count_cycles(adjacency_list)
            
        synteny_p = [abs(int(synteny)) for cycle in p for synteny in cycle]
        synteny_q = [abs(int(synteny)) for cycle in q for synteny in cycle]
        alphabet = [synteny for synteny in synteny_p if synteny in synteny_q]

        
        return len(alphabet) - num_cycles
        
    def count_cycles(self, adjacency_list):
        cycles = []
        node = self.get_node(adjacency_list)
        while node != 0:
            cycle = [node]
            self.travel(adjacency_list, cycle)
            cycles.append(cycle)
            node = self.get_node(adjacency_list)
        print(cycles)
        return len(cycles)
        
    def travel(self, adjacency_list, cycle):
        node = cycle[-1]
        next_node = adjacency_list[node][0]
        adjacency_list[node].remove(next_node)
        adjacency_list[next_node].remove(node)
        cycle.append(next_node)
        if next_node != cycle[0]:
            self.travel(adjacency_list, cycle)
        return
        
    def get_node(self, adjacency_list):
        for k, v in adjacency_list.items():
            if len(v) > 0:
                return k
        return 0
        
        
    def test(self):
        str_P = "(+1 +2 +3)(+4 +5)"
        str_Q = "(+2 -1 +4 -3 +5)"
        
        P = [s.split(' ') for s in str_P[1:-1].split(')(')]
        Q = [s.split(' ') for s in str_Q[1:-1].split(')(')]
        
        d = self.calculate_two_breaks_distance(P, Q)
        print(d)
        
    
