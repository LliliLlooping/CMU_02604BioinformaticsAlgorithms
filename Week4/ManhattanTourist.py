from typing import List
import numpy as np

class ManhattanTourist:
    
    def __init__(self):
        pass
    
    def longest_path_length(self, n: int, m: int, down: List[List[int]], right: List[List[int]]) -> int:
        
        # Initializes the DP array
        array = np.zeros((n + 1, m + 1), dtype=int)
        
        # Initializes the first row
        for j in range(1, m + 1):
            array[0, j] = array[0][j - 1] + right[0][j - 1]
        
        # Initializes the first column
            for i in range(1, n + 1):
                array[i, 0] = array[i - 1][0] + down[i - 1][0]
        
        # Fills in the entire array
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                array[i, j] = max(array[i - 1][j] + down[i - 1][j], array[i][j - 1] + right[i][j - 1])
                
        result = array[n, m]
        
        return result
    
    def test(self):
        n, m = 4, 4
        down = [
            [1, 0, 2, 4, 3],
            [4, 6, 5, 2, 1],
            [4, 4, 5, 2, 1],
            [5, 6, 8, 5, 3]
        ]
        right = [
            [3, 2, 4, 0],
            [3, 2, 4, 2],
            [0, 7, 3, 3],
            [3, 3, 0, 2],
            [1, 3, 2, 2]
        ]
        result = self.longest_path_length(n, m, down, right)
        assert result == 34