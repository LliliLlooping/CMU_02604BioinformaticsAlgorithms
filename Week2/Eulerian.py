from typing import Dict
import numpy as np
from AdjacencyList import AdjacencyList

class Eulerian:
    
    def __init__(self):
        self.adjacencyList = AdjacencyList()
    
    def find_eulerian_cycle(self, adjacency_list: Dict[str, str]):
        
        # Initializes a random starting node
        next_starting_node = np.random.choice(list(adjacency_list.keys()))
        
        # Initializes a cycle
        eulerian_cycle = self.find_cycle(adjacency_list, next_starting_node)
        
        # Count the remaining edge
        remainingEdges = self.adjacencyList.count_edges(adjacency_list)
        
        # Until visits all edges
        while remainingEdges > 0:
            
            # Find the next potential starting nodes, i.e.
            # the nodes on current cycle that still have outbounding edges
            potential_starting_nodes = [i for i, node in enumerate(eulerian_cycle) if len(adjacency_list[node]) > 0]
            next_starting_node_index = np.random.choice(potential_starting_nodes)
            next_starting_node = eulerian_cycle[next_starting_node_index]
            
            # Generates the next cycle
            cycle = self.find_cycle(adjacency_list, next_starting_node)
                                            
            # Updates the remaining edge           
            remainingEdges -= len(cycle)

            # Merges the two cycles
            eulerian_cycle = eulerian_cycle[next_starting_node_index:] + eulerian_cycle[:next_starting_node_index]
            eulerian_cycle += cycle
        
        eulerian_cycle.append(eulerian_cycle[0])
        
        return eulerian_cycle
    
    
    def find_cycle(self, adjacency_list: Dict[str, str], starting_node: int):
        """
            Eulerian Cycle guaranteed.
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
            9: [6]
        }  
        cycle = self.find_eulerian_cycle(adjacency_list)
        print(cycle)
            
        