import numpy as np
from typing import Tuple
import sys
sys. setrecursionlimit(2048)

class Alignment:
    
    def __init__(self):
        pass
    
    def local_alignment(self, match: int, mismatch: int, indel: int, s1: str, s2: str):
        
        score, backtrack, [i, j] = self.local_alignment_backtrack(match, mismatch, indel, s1, s2)
        gapped_s1, gapped_s2 = [], []
        self.output(backtrack, gapped_s1, gapped_s2, s1, s2, i, j)
        
        gapped_s1, gapped_s2 = ''.join(gapped_s1[::-1]), ''.join(gapped_s2[::-1])
        
        return (score, gapped_s1, gapped_s2)
    
    def global_alignment(self, match: int, mismatch: int, indel: int, s1: str, s2: str):
        
        score, backtrack = self.global_alignment_backtrack(match, mismatch, indel, s1, s2)
        gapped_s1, gapped_s2 = [], []
        self.output(backtrack, gapped_s1, gapped_s2, s1, s2, len(s1), len(s2))
        
        gapped_s1, gapped_s2 = ''.join(gapped_s1[::-1]), ''.join(gapped_s2[::-1])
        
        return (score, gapped_s1, gapped_s2)
    
    
    def global_alignment_backtrack(self, match: int, mismatch: int, indel: int, s1: str, s2: str) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int), np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)
        
        for i in range(1, l1+1):
            score[i, 0] = -indel * i
            backtrack[i, 0] = 2
            
        for j in range(1, l2+1):
            score[0, j] = -indel * j
            backtrack[0, j] = 1
            
        for i in range(1, l1+1):
            for j in range(1, l2+1):
                
                if s1[i-1] == s2[j-1]:
                    diag = score[i-1, j-1] + match
                else:
                    diag = score[i-1, j-1] - mismatch
                up = score[i-1, j] - indel
                left = score[i, j-1] - indel
                
                if diag == max(diag, up, left):
                    score[i, j] = diag
                    backtrack[i, j] = 3
                    
                elif left == max(diag, up, left):
                    score[i, j] = left
                    backtrack[i, j] = 1
                    
                else:
                    score[i, j] = up
                    backtrack[i, j] = 2
        return score[len(s1), len(s2)], backtrack
    
    
    def output(self, backtrack, gapped_s1, gapped_s2, s1, s2, i, j):
        """
            Recursively output based on an backtrack array.
        """
        if backtrack[i, j] == 0:
            return
        if backtrack[i, j] == 1: # horizontal
            gapped_s1.append('-')
            gapped_s2.append(s2[j-1])
            self.output(backtrack, gapped_s1, gapped_s2, s1, s2, i, j - 1)
            return
        elif backtrack[i, j] == 2: # vertical
            gapped_s1.append(s1[i-1])
            gapped_s2.append('-')
            self.output(backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j)
            return
        else: # diagonal
            gapped_s1.append(s1[i-1])
            gapped_s2.append(s2[j-1])
            self.output(backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j - 1)
            return
        
    def local_alignment_backtrack(self, match: int, mismatch: int, indel: int, s1: str, s2: str) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int), np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)
            
        for i in range(1, l1+1):
            for j in range(1, l2+1):
                
                if s1[i-1] == s2[j-1]:
                    diag = score[i-1, j-1] + match
                else:
                    diag = score[i-1, j-1] - mismatch
                up = score[i-1, j] - indel
                left = score[i, j-1] - indel
                
                if 0 == max(diag, up, left, 0):
                    score[i, j] = 0
                    
                elif diag == max(diag, up, left, 0):
                    score[i, j] = diag
                    backtrack[i, j] = 3
                    
                elif left == max(diag, up, left, 0):
                    score[i, j] = left
                    backtrack[i, j] = 1
                    
                else:
                    score[i, j] = up
                    backtrack[i, j] = 2
                    
        print(score)
        print(backtrack)
        i, j = np.argmax(score) // score.shape[1], np.argmax(score) % score.shape[1]
        return score[i, j], backtrack, [i, j]
    
    def test(self):
        match, mismatch, indel = 1, 1, 1
        s1 = 'TAACG'
        s2 = 'ACGTG'
        score, gapped_s1, gapped_s2 = self.local_alignment(match, mismatch, indel, s1, s2)
        print(score, gapped_s1, gapped_s2)