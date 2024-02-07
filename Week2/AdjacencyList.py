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
    
    def count_edges(self, adjacency_list: Dict[str, str]) -> int:
        
        # Guaranteed no independent node.
        
        num_edges = sum([len(v )for v in adjacency_list.values()])
        
        return num_edges
    
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