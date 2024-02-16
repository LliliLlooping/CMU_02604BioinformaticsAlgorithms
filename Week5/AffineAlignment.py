from typing import Tuple
import numpy as np

class AffineAlignment:
    
    def __init__(self):
        pass
    
    def alignment(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, gap_opening_penalty: int, gap_extension_penalty: int, mode: str) -> Tuple[int, str, str]:
        
        if mode == 'global':
            score, gapped_s1, gapped_s2 = self.global_affine_alignment(s1, s2, match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty)
            
            return score, gapped_s1, gapped_s2
        
    def global_affine_alignment(self, s1: str, s2: str, match: int, mismatch: int, gap_opening_penalty: int, gap_extension_penalty: int) -> Tuple[int, str, str]:
        
        score, vertical_backtrack, horizontal_backtrack, diagonal_backtrack = self._global_alignment_backtrack(s1, s2, match, mismatch, gap_opening_penalty, gap_extension_penalty)

        gapped_s1, gapped_s2 = self._output(vertical_backtrack, horizontal_backtrack, diagonal_backtrack,  s1, s2, len(s1), len(s2))

        return (score, gapped_s1, gapped_s2)  
    
    def _output(self, vertical_backtrack, horizontal_backtrack, diagonal_backtrack, s1: str, s2: str, i: int, j: int)  -> Tuple[str, str]:
        
        gapped_s1, gapped_s2 = [], []
        
        self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j, 'diagonal')
        
        gapped_s1, gapped_s2 = ''.join(gapped_s1[::-1]), ''.join(gapped_s2[::-1])
        
        return (gapped_s1, gapped_s2)
        
    def _output_recur(self, vertical_backtrack: np.array, horizontal_backtrack: np.array, diagonal_backtrack: np.array, gapped_s1: str, gapped_s2: str, s1: str, s2: str, i: int, j: int, which_matrix):
        
        if which_matrix == 'diagonal' and i == 0 and j == 0:
            return
        
        if which_matrix == 'diagonal':
            if diagonal_backtrack[i, j] == 1:   # horizontal
                # gapped_s1.append('-')
                # gapped_s2.append(s2[j-1])
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j, 'horizontal')
                return
            
            elif diagonal_backtrack[i, j] == 2: # vertical
                # gapped_s1.append(s1[i-1])
                # gapped_s2.append('-')
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j, 'vertical')
                return
            
            else:                       # diagonal
                gapped_s1.append(s1[i-1])
                gapped_s2.append(s2[j-1])
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j - 1, 'diagonal')
                return
            
        elif which_matrix == 'vertical':
            if vertical_backtrack[i, j] == 1:   # horizontal
                gapped_s1.append('-')
                gapped_s2.append(s2[j-1])
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j - 1, 'horizontal')
                return
            
            elif vertical_backtrack[i, j] == 2: # vertical
                gapped_s1.append(s1[i-1])
                gapped_s2.append('-')
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j, 'vertical')
                return
            
            else:                       # diagonal
                gapped_s1.append(s1[i-1])
                gapped_s2.append('-')
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j, 'diagonal')
                return
        
        else:
            if horizontal_backtrack[i, j] == 1:   # horizontal
                gapped_s1.append('-')
                gapped_s2.append(s2[j-1])
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j - 1, 'horizontal')
                return
            
            elif horizontal_backtrack[i, j] == 2: # vertical
                gapped_s1.append(s1[i-1])
                gapped_s2.append('-')
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i - 1, j, 'vertical')
                return
            
            else:                       # diagonal
                gapped_s1.append('-')
                gapped_s2.append(s2[j-1])
                self._output_recur(vertical_backtrack, horizontal_backtrack, diagonal_backtrack, gapped_s1, gapped_s2, s1, s2, i, j - 1, 'diagonal')
                return

            
    
    def _global_alignment_backtrack(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, gap_opening_penalty: int, gap_extension_penalty: int) -> Tuple[int, np.array]:
        
        vertical_score, horizontal_score, diagonal_score, vertical_backtrack, horizontal_backtrack, diagonal_backtrack = self._initialize_matrix(s1, s2, match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty)
            
        self._fill_matrix(s1, s2, match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, vertical_score, horizontal_score, diagonal_score, vertical_backtrack, horizontal_backtrack, diagonal_backtrack)
        
        # In global alignment, the score must be located at the bottom-right corner
        global_score = diagonal_score[len(s1), len(s2)]
        
        print(vertical_score)
        print()
        print(horizontal_score)
        print()
        print(diagonal_score)
        print()
        print(vertical_backtrack)
        print()
        print(horizontal_backtrack)
        print()
        print(diagonal_backtrack)
        return (global_score, vertical_backtrack, horizontal_backtrack, diagonal_backtrack)
        
    def _initialize_matrix(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, gap_opening_penalty: int, gap_extension_penalty: int) -> Tuple[np.array]:
        
        l1, l2 = len(s1), len(s2)
        
        vertical_score, horizontal_score, diagonal_score = np.zeros((l1 + 1, l2 + 1), dtype=float), np.zeros((l1 + 1, l2 + 1), dtype=float), np.zeros((l1 + 1, l2 + 1), dtype=int)
       
        diagonal_score[0, 0] = 0
        diagonal_score[0, 1] = -gap_opening_penalty
        diagonal_score[1, 0] = -gap_opening_penalty
        for i in range(2, l1 + 1):
            diagonal_score[i, 0] = diagonal_score[i - 1, 0] - gap_extension_penalty
        for j in range(2, l2 + 1):
            diagonal_score[0, j] = diagonal_score[0, j - 1] - gap_extension_penalty
            
        vertical_score[0, 1:] = -np.inf
        horizontal_score[1:, 0] = -np.inf
        
        vertical_backtrack, horizontal_backtrack, diagonal_backtrack = np.zeros((l1 + 1, l2 + 1), dtype=int), np.zeros((l1 + 1, l2 + 1), dtype=int), np.zeros((l1 + 1, l2 + 1), dtype=int)
        for i in range(1, l1 + 1):
            diagonal_backtrack[i, 0] = 2
            # vertical_backtrack[i, 0] = 2
        for j in range(1, l2 + 1):
            diagonal_backtrack[0, j] = 1
            # horizontal_backtrack[0, j] = 1
        
        
        return (vertical_score, horizontal_score, diagonal_score, vertical_backtrack, horizontal_backtrack, diagonal_backtrack)
    
    def _fill_matrix(self, s1: str, s2: str, match_reward: int, mismatch_penalty: int, gap_opening_penalty: int, gap_extension_penalty: int, vertical_score: np.array, horizontal_score: np.array, diagonal_score: np.array, vertical_backtrack: np.array, horizontal_backtrack: np.array, diagonal_backtrack: np.array):
        
        m, n = diagonal_score.shape
        
        for i in range(1, m):
            for j in range(1, n):
                
                self._update_vertical_score(vertical_score, diagonal_score, i, j, gap_opening_penalty, gap_extension_penalty, vertical_backtrack)
                
                self._update_horizontal_score(horizontal_score, diagonal_score, i, j, gap_opening_penalty, gap_extension_penalty, horizontal_backtrack)
                
                self._update_diagonal_score(s1, s2, i, j, match_reward, mismatch_penalty, vertical_score, horizontal_score, diagonal_score, diagonal_backtrack)

        return
    
    def _update_vertical_score(self, vertical_score, diagonal_score, i, j, gap_opening_penalty: int, gap_extension_penalty: int, vertical_backtrack: np.array):
        
        gap_extension_score = vertical_score[i - 1, j] - gap_extension_penalty
        
        gap_opening_score = float(diagonal_score[i - 1, j]) - gap_opening_penalty
        
        if gap_opening_score > gap_extension_score:
            
            vertical_score[i, j] = gap_opening_score
            vertical_backtrack[i, j] = 3
        else:
            
            vertical_score[i, j] = gap_extension_score
            vertical_backtrack[i, j] = 2
            
    def _update_horizontal_score(self, horizontal_score, diagonal_score, i, j, gap_opening_penalty: int, gap_extension_penalty: int, horizontal_backtrack: np.array):
        
        gap_extension_score = horizontal_score[i, j - 1] - gap_extension_penalty
        
        gap_opening_score = float(diagonal_score[i, j - 1]) - gap_opening_penalty
        
        if gap_opening_score > gap_extension_score:
            
            horizontal_score[i, j] = gap_opening_score
            horizontal_backtrack[i, j] = 3
            
        else:
            
            horizontal_score[i, j] = gap_extension_score
            horizontal_backtrack[i, j] = 1
            
    def _update_diagonal_score(self, s1: str, s2: str, i: int, j: int, match_reward: int, mismatch_penalty: int, vertical_score: np.array, horizontal_score: np.array, diagonal_score: np.array, diagonal_backtrack: np.array):
        
        vertical_gap_score = int(vertical_score[i, j])
        
        horizontal_gap_score = int(horizontal_score[i, j])
        
        if s1[i - 1] == s2[j - 1]:
            diagonal_match_score = diagonal_score[i - 1, j - 1] + match_reward
            
        else:
            diagonal_match_score = diagonal_score[i - 1, j - 1] - mismatch_penalty

        if max(vertical_gap_score, horizontal_gap_score, diagonal_match_score) == vertical_gap_score:
            diagonal_score[i, j] = vertical_gap_score
            diagonal_backtrack[i, j] = 2
        
        elif max(vertical_gap_score, horizontal_gap_score, diagonal_match_score)  == horizontal_gap_score:
            diagonal_score[i, j] = horizontal_gap_score
            diagonal_backtrack[i, j] = 1  
            
        else:
            diagonal_score[i, j] = diagonal_match_score
            diagonal_backtrack[i, j] = 3
           

    def test(self):
        match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty = 5, 2, 15, 5
        s1 = 'ACGTA'
        s2 = 'ACT'
        score, gapped_s1, gapped_s2 = self.alignment(s1, s2, match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, 'global')
        print(score)
        print(gapped_s1)
        print(gapped_s2)