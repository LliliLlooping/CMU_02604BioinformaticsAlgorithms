import numpy as np
from typing import List, Dict, Tuple

class DAG:
    
    def __init__(self, file_path='./input_DAG_LongestPath.txt'):
        
        # Initialize the DAG by reading the adjacency_list, start, and end
        [self.s, self.t], self.adjacency_list = self._read_weighted_edges(file_path)
        
        # Find the topological sorting for this DAG
        self.topological_ordered_v = self.topological_sorting()
            
    def _read_weighted_edges(self, file_path: str) -> (List[int], Dict[int, List[Tuple[int, int]]]):
        
        # Read the input file
        with open(file_path, 'r') as file:
            [start, end] = file.readline()[:-1].split(' ')
            start, end = int(start), int(end)
            data = file.read().split('\n')
        
        # Read adjacency list
        adjacency_list = {}
        for line in data:
            [ori, des, weight] = line.split(' ')
            ori, des, weight = int(ori), int(des), int(weight)
            if ori not in adjacency_list:
                adjacency_list[ori] = []
            adjacency_list[ori].append((des, weight))
   
        return [start, end], adjacency_list
    
    def topological_sorting(self) -> List[int]:
        
        # Find all unique vertices
        vertices = self._list_edges(self.adjacency_list)
        
        # Maintain a dictionary for recording if we have visited a vertex
        visited = {v: False for v in vertices}
        
        # Maintain a stack o record the result
        stack = []
        
        # DFS on the vertices
        for v in vertices:
            if visited[v] == False:
                self._topological_sorting_recursion(v, visited, stack)
        
        return stack[::-1]
                
    def _topological_sorting_recursion(self, ori: int, visited: List[bool], stack: List[int]):
 
        # Mark the current node as visited.
        visited[ori] = True
 
        # Recur for all the vertices adjacent to this vertex
        if ori in self.adjacency_list:
            for pair in self.adjacency_list[ori]:
                des = pair[0]
                if visited[des] == False:
                    self._topological_sorting_recursion(des, visited, stack)
 
        # Push current vertex to stack which stores result
        stack.append(ori)
        
    def _list_edges(self, ajacency_list: Dict[int, List[Tuple[int, int]]]) -> List[int]:
        
        # Enumerate all the vertices
        nodes = []
        for ori, v in ajacency_list.items():
            nodes.append(ori)
            for des in v:
                nodes.append(des[0])
        return list(set(nodes))

    def longest_path(self):
        
        """
            This function does not try to find the longest path in the DAG.
            It finds the longest path between self.s and self.t
        """
        # Find the starting node in the topological ordered list
        s_index, t_index = np.where(np.array(self.topological_ordered_v) == self.s)[0][0], np.where(np.array(self.topological_ordered_v) == self.t)[0][0]
        
        # Maintain a dictionary for saving the distance,
        # and another for recording the backtracks for every vertices
        distance, last_nodes = {self.s: 0}, {}
        
        # Iterate over all starting between s and t
        for i in range(s_index, t_index):
            
            ori = self.topological_ordered_v[i]
            
            if ori not in self.adjacency_list or ori not in distance:
                continue
            
            destination_dic = {k: v for (k, v) in self.adjacency_list[ori]}
            
            # Iterate over all outbounding edges from the start
            for des, weight in destination_dic.items():
                if des not in distance:
                    distance[des] = distance[ori] + weight
                    last_nodes[des] = ori
                elif weight > 0 and distance[ori] + weight > distance[des]:
                    distance[des] = distance[ori] + weight
                    last_nodes[des] = ori
        
        
        pre_step = self.t
        
        # Maintain a list for recording the backtrack
        backtrack = []
        
        # Trace back until hit s
        while pre_step != self.s:
            backtrack.append(pre_step)
            pre_step = last_nodes[pre_step]
        backtrack.append(self.s)
        
        longest_path = backtrack[::-1]
        
        longest_distance = distance[self.t]
        
        return longest_distance, longest_path
    
    # def _read_edges(self, file_path: str) -> Dict[int, List[Tuple[int, int]]]:
    #     with open(file_path, 'r') as file:
    #         data = file.read().split('\n')
    #     adjacency_list = {}
    #     for line in data:
    #         line_ = line.split(': ')
    #         ori, des_list = int(line_[0]), line_[1].split(' ')
    #         if ori not in adjacency_list:
    #             adjacency_list[ori] = []
    #         for des in des_list:
    #             adjacency_list[ori].append((int(des), 1))
    #     return adjacency_list
    
    def test(self):
        longest_distance, longest_path = self.longest_path()
        assert longest_distance == 62
        assert longest_path == [0, 14, 29, 44]
        # print(longest_distance, longest_path)