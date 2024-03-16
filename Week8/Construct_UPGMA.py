from typing import List
from copy import deepcopy

class BinaryTree:

    def __init__(self, id, age=0.0, num_offspring=1, left=None, right=None): 

        self.id = id
        self.age = age
        self.num_offspring = num_offspring
        self.children: BinaryTree[2] = [left, right]

    def __eq__(self, other):

        if isinstance(other, BinaryTree):
            return self.id == other.id
        
        return False
    
class Construct_UPGMA:

    def __init__(self):
        pass

    def construct_tree(self, input_distance_matrix: List[List[int]]):

        def construct_adjacency_list(input_distance_matrix):

            n = len(input_distance_matrix)

            adjacency_list = {}

            for i in range(n):
                adjacency_list[i] = {}

                for j in range(n):
                    adjacency_list[i][j] = input_distance_matrix[i][j]

            return adjacency_list
        
        def BFS(node, edges):

            if node.children[0] == None:
                return 
            
            for child in node.children:
                edges.append((node.id, child.id, round(node.age - child.age, 3)))

            for child in node.children:
                BFS(child, edges)

        adjacency_list = construct_adjacency_list(input_distance_matrix)

        num_nodes = len(input_distance_matrix)
        
        nodes = []

        for i in range(num_nodes):
            nodes.append(BinaryTree(i))

        roots = deepcopy(nodes)

        while len(roots) > 1:

            self.merge_closest(nodes, roots, adjacency_list, num_nodes)

            num_nodes += 1

        edges = []

        BFS(roots[0], edges)

        return edges

    def merge_closest(self, nodes, roots, adjacency_list, num_nodes):

        def find_closest(adjacency_list, num_nodes):

            smallest_idx = [0, 1]
            smallest_value = float("inf")

            for i in range(num_nodes - 1):
                
                if i not in adjacency_list:
                    continue

                for j in range(i + 1, num_nodes):

                    if j not in adjacency_list[i]:
                        continue

                    if adjacency_list[i][j] < smallest_value:
                        smallest_value = adjacency_list[i][j]
                        smallest_idx = [i, j]

            return smallest_idx
        
        i, j = find_closest(adjacency_list, num_nodes)

        node_i, node_j = nodes[i], nodes[j]

        roots.remove(node_i)
        roots.remove(node_j)

        new_node = BinaryTree(num_nodes, (adjacency_list[i][j]) / 2, nodes[i].num_offspring + nodes[j].num_offspring, left = nodes[i], right = nodes[j])
        nodes.append(new_node)
        roots.append(new_node)

        new_list = {}

        for k, v in adjacency_list.items():

            if k == i or k == j:
                continue

            if i in v and j in v:
                v[num_nodes] = (v[i] * node_i.num_offspring + v[j] * node_j.num_offspring) / (node_i.num_offspring + node_j.num_offspring)
                del v[i], v[j]

            new_list[k] = v[num_nodes]

        adjacency_list[num_nodes] = new_list

        del adjacency_list[i], adjacency_list[j]


    def test(self):
        input_distance_matrix = [
            [0, 13, 21, 22],
            [13, 0, 12, 13],
            [21, 12, 0, 13],
            [22, 13, 13, 0]
        ]
        result = self.construct_tree(input_distance_matrix)
        print(result)

