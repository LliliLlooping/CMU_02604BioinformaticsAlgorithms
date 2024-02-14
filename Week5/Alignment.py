import numpy as np
from typing import Tuple
import sys
sys.setrecursionlimit(2048)

from BLOSUM62 import BLOSUM

class Alignment:
    
    def __init__(self):
        pass
    
    def alignment(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, indel_penalty: int, free_ride_before_s1=False, free_ride_after_s1=False, free_ride_before_s2=False, free_ride_after_s2=False) -> Tuple[int, str, str]:
        
        if free_ride_before_s1 == False and free_ride_after_s1 == False and free_ride_before_s2 == False and free_ride_after_s2 == False:
            return self.global_alignment(s1, s2, match_reward, mismatch_penalty, indel_penalty)
            
        elif free_ride_before_s1 == False and free_ride_after_s1 == False and free_ride_before_s2 == True and free_ride_after_s2 == True:
            return self.fitting_alignment(s2, s1, indel_penalty)
            
        elif free_ride_before_s1 == True and free_ride_after_s1 == True and free_ride_before_s2 == False and free_ride_after_s2 == False:
            return self.fitting_alignment(s1, s2, indel_penalty)
            
        elif free_ride_before_s1 == True and free_ride_after_s1 == False and free_ride_before_s2 == False and free_ride_after_s2 == True:
            return self.overlap_alignment(s1, s2, match_reward, mismatch_penalty, indel_penalty)
            
        elif free_ride_before_s1 == False and free_ride_after_s1 == True and free_ride_before_s2 == True and free_ride_after_s2 == False:
            return self.overlap_alignment(s2, s1, match_reward, mismatch_penalty, indel_penalty)
            
        elif free_ride_before_s1 == True and free_ride_after_s1 == True and free_ride_before_s2 == True and free_ride_after_s2 == True:
            return self.local_alignment(s1, s2, match_reward, mismatch_penalty, indel_penalty)
    
    def global_alignment(self, s1: str, s2: str, match: int, mismatch: int, indel: int) -> Tuple[int, str, str]:
        
        score, backtrack = self._global_alignment_backtrack(s1, s2, match, mismatch, indel)
        
        gapped_s1, gapped_s2 = self._output(backtrack, s1, s2, len(s1), len(s2))
        
        return (score, gapped_s1, gapped_s2)  
    
    def fitting_alignment(self, s1: str, s2: str, indel: int) -> Tuple[int, str, str]:
        
        score, backtrack, i = self._fitting_alignment_backtrack(s1, s2, indel)
        
        gapped_s1, gapped_s2 = self._output(backtrack, s1, s2, i, len(s2))
        
        return (score, gapped_s1, gapped_s2) 
    
    def overlap_alignment(self, s1: str, s2: str, match: int, mismatch: int, indel: int) -> Tuple[int, str, str]:
        
        score, backtrack, j = self._overlap_alignment_backtrack(s1, s2, match, mismatch, indel)
        
        gapped_s1, gapped_s2 = self._output(backtrack, s1, s2, len(s1), j)
        
        return (score, gapped_s1, gapped_s2)
    
    def local_alignment(self, s1: str, s2: str, match: int, mismatch: int, indel: int) -> Tuple[int, str, str]:
        
        score, backtrack, [i, j] = self._local_alignment_backtrack(s1, s2, match, mismatch, indel)
        
        gapped_s1, gapped_s2 = self._output(backtrack, s1, s2, i, j)
        
        return (score, gapped_s1, gapped_s2) 
    
    def _output(self, backtrack: np.array, s1: str, s2: str, i: int, j: int)  -> Tuple[str, str]:
        
        gapped_s1, gapped_s2 = [], []
        
        self._output_recur(backtrack, gapped_s1, gapped_s2, s1, s2, i, j)
        
        gapped_s1, gapped_s2 = ''.join(gapped_s1[::-1]), ''.join(gapped_s2[::-1])
        
        return (gapped_s1, gapped_s2)
        
    def _output_recur(self, backtrack: np.array, gapped_s1: str, gapped_s2: str, s1: str, s2: str, i: int, j: int):
        
        if backtrack[i, j] == 0:
            return
        
        if backtrack[i, j] == 1:   # horizontal
            gapped_s1.append('-')
            gapped_s2.append(s2[j-1])
            self._output_recur(backtrack, gapped_s1, gapped_s2, s1, s2, i, j - 1)
            return
        
        elif backtrack[i, j] == 2: # vertical
            gapped_s1.append(s1[i-1])
            gapped_s2.append('-')
            self._output_recur(backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j)
            return
        
        else:                       # diagonal
            gapped_s1.append(s1[i-1])
            gapped_s2.append(s2[j-1])
            self._output_recur(backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j - 1)
            return
        
    def _global_alignment_backtrack(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, indel_penalty: int) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = self._initialize_matrix(l1, l2, 'global', indel_penalty)
            
        self._fill_matrix(s1, s2, match_reward, mismatch_penalty, indel_penalty, score, backtrack, 'global')
        
        # In global alignment, the score must be located at the bottom-right corner
        global_score = score[len(s1), len(s2)]
        
        return global_score, backtrack
        
    def _local_alignment_backtrack(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, indel_penalty: int) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = self._initialize_matrix(l1, l2, 'local')
            
        self._fill_matrix(s1, s2, match_reward, mismatch_penalty, indel_penalty, score, backtrack, 'local')
        
        # In local alignment, the score can be located anywhere
        local_score_index =  np.argmax(score)
        local_score_i, local_score_j = local_score_index // score.shape[1], local_score_index % score.shape[1]
        local_score = score[local_score_i, local_score_j]
        
        return local_score, backtrack, [local_score_i, local_score_j]
    
    def _overlap_alignment_backtrack(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, indel_penalty: int) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = self._initialize_matrix(l1, l2, 'overlap', indel_penalty)
        
        self._fill_matrix(s1, s2, match_reward, mismatch_penalty, indel_penalty, score, backtrack, 'overlap')
        
        # In this setting of overlap alignment, the score must be located in the last row
        overlap_score_j = np.argmax(score[l1, :])
        overlap_score = score[l1, overlap_score_j]
        
        return overlap_score, backtrack, overlap_score_j
    
    def _fitting_alignment_backtrack(self, s1: str, s2: str, indel_penalty: int) -> Tuple[int, np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        score, backtrack = self._initialize_matrix(l1, l2, 'fitting', indel_penalty)
        
        self._fill_matrix(s1, s2, 0, 0, indel_penalty, score, backtrack, 'fitting')
        
        # In this setting of fitting alignment, the score must be located in the last column
        alignment_score_i = np.argmax(score[:, l2])
        alignment_score = score[alignment_score_i, l2]
        
        return alignment_score, backtrack, alignment_score_i
    
    def _initialize_matrix(self, l1: int, l2: int, mode: str, indel_penalty = 0):
        
        score, backtrack = np.zeros((l1 + 1, l2 + 1), dtype=int), np.zeros((l1 + 1, l2 + 1), dtype=int)
        
        if mode == 'local':
            pass
        
        else:
            assert indel_penalty > 0
            
            if mode == 'global':
                # Do not allow free ride anywhere
                
                for i in range(1, l1 + 1):
                    score[i, 0] = -indel_penalty * i
                    backtrack[i, 0] = 2 # vertical
                
                for j in range(1, l2 + 1):
                    score[0, j] = -indel_penalty * j
                    backtrack[0, j] = 1 # horizontal
            
            elif mode == 'overlap' or mode == 'fitting':
                # Allow free ride in the first row
                # meaning it's allowed to delete the prefix of s1 for free
                
                for j in range(1, l2 + 1):
                    score[0, j] = -indel_penalty * j
                    backtrack[0, j] = 1 # horizontal
            else:
                
                ValueError("Wrong mode.")
        
        return score, backtrack
    
    def _fill_matrix(self, s1, s2, match_reward, mismatch_penalty, indel_penalty, score, backtrack, mode):
        
        m, n = score.shape
        
        for i in range(1, m):
            for j in range(1, n):
                
                up = score[i-1, j] - indel_penalty
                
                left = score[i, j-1] - indel_penalty
                
                if mode == 'fitting':
                    diag = score[i-1, j-1] + BLOSUM[s1[i-1]][s2[j-1]]
                else:
                    if s1[i-1] == s2[j-1]:
                        diag = score[i-1, j-1] + match_reward
                    else:
                        diag = score[i-1, j-1] - mismatch_penalty
                
                if mode != 'local':
                    if diag == max(diag, up, left):
                        score[i, j] = diag
                        backtrack[i, j] = 3
                        
                    elif left == max(diag, up, left): # horizontal
                        score[i, j] = left
                        backtrack[i, j] = 1
                        
                    else:                        # vertical
                        score[i, j] = up
                        backtrack[i, j] = 2
                else:
                    if 0 == max(diag, up, left, 0):
                        score[i, j] = 0
                        backtrack[i, j] = 0
                        
                    elif diag == max(diag, up, left, 0):
                        score[i, j] = diag
                        backtrack[i, j] = 3
                        
                    elif left == max(diag, up, left, 0): # horizontal
                        score[i, j] = left
                        backtrack[i, j] = 1
                        
                    else:                        # vertical
                        score[i, j] = up
                        backtrack[i, j] = 2
                    
        return
    
    # def test(self):
    #     match_reward, mismatch_penalty, indel_penalty = 3, 2, 1
        
    #     s = 'CAGAGATGGCCG'
        
    #     t = 'ACG'
        
    #     score, gapped_s1, gapped_s2 = self.alignment(s, t, match_reward, mismatch_penalty, indel_penalty, True, True, True, True)
        
    #     print(score, gapped_s1, gapped_s2)