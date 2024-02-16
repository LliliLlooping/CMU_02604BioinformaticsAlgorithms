import numpy as np

class String:
    def __init__(self):
        pass
    
    def edit_distance(self, s1: str, s2: str) -> int:
        
        l1, l2 = len(s1), len(s2)
        
        distance = np.zeros((l1 + 1, l2 + 1), dtype=int)
        
        for i in range(1, l1 + 1):
            distance[i, 0] = i
            
        for j in range(1, l2 + 1):
            distance[0, j] = j
            
        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                
                up = distance[i-1, j] + 1
                left = distance[i, j-1] + 1
                diag = distance[i-1, j-1] + int(s1[i-1]!=s2[j-1])
                
                distance[i, j] = min(up, left, diag)
                
        return distance[l1, l2]
    
    def test(self):
        s1 = 'GAGA'
        s2 = 'GAT'
        distance = self.edit_distance(s1, s2)
        print(distance)