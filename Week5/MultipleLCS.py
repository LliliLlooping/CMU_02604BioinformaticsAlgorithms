import numpy as np

class MultipleLCS:
    
    def __init__(self):
        pass
    
    def find_triple_lcs(self, s1, s2, s3, mode):
        
        if mode == 'global':
            
            score, backtrack = self.global_triple_backtrack(s1, s2, s3)
            
            gapped_s1, gapped_s2, gapped_s3 = self.triple_output(backtrack, s1, s2, s3)
        
        return score, gapped_s1, gapped_s2, gapped_s3
    
    def triple_output(self, backtrack, s1, s2, s3):
        
        gapped_s1, gapped_s2, gapped_s3 = [], [], []
        
        self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, len(s1), len(s2), len(s3))

        gapped_s1, gapped_s2, gapped_s3 = ''.join(gapped_s1[::-1]), ''.join(gapped_s2[::-1]), ''.join(gapped_s3[::-1])
        
        return (gapped_s1, gapped_s2, gapped_s3)
    
    def _triple_output_recur(self, backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i, j, k):
        
        if i == 0 and j == 0 and k == 0:
            return

        if backtrack[i, j, k] == 1:
            gapped_s1.append(s1[i-1])
            gapped_s2.append(s2[j-1])
            gapped_s3.append(s3[k-1])
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i - 1, j - 1, k - 1)
            
        elif backtrack[i, j, k] == 2:
            gapped_s1.append(s1[i-1])
            gapped_s2.append(s2[j-1])
            gapped_s3.append('-')
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i - 1, j - 1, k)
            
        elif backtrack[i, j, k] == 3:
            gapped_s1.append(s1[i-1])
            gapped_s2.append('-')
            gapped_s3.append(s3[k-1])
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i - 1, j, k - 1)
            
        elif backtrack[i, j, k] == 4:
            gapped_s1.append('-')
            gapped_s2.append(s2[j-1])
            gapped_s3.append(s3[k-1])
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i, j - 1, k - 1)
            
        elif backtrack[i, j, k] == 5:
            gapped_s1.append(s1[i-1])
            gapped_s2.append('-')
            gapped_s3.append('-')
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i - 1, j, k)
            
        elif backtrack[i, j, k] == 6:
            gapped_s1.append('-')
            gapped_s2.append(s2[j-1])
            gapped_s3.append('-')
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i, j - 1, k)
        
        elif backtrack[i, j, k] == 7:
            gapped_s1.append('-')
            gapped_s2.append('-')
            gapped_s3.append(s3[k-1])
            self._triple_output_recur(backtrack, gapped_s1, gapped_s2, gapped_s3, s1, s2, s3, i, j, k - 1)
    
    def global_triple_backtrack(self, s1, s2, s3):
    
        l1, l2, l3 = len(s1), len(s2), len(s3)
        
        score, backtrack = np.zeros((l1 + 1, l2 + 1, l3 + 1), dtype=int), np.zeros((l1 + 1, l2 + 1, l3 + 1), dtype=int)
        
        backtrack[:, 0, 0] = 5
        backtrack[0, :, 0] = 6
        backtrack[0, 0, :] = 7
        backtrack[0, 0, 0] = 0
        backtrack[1:, 1:, 0] = 2
        backtrack[1:, 0, 1:] = 3
        backtrack[0, 1:, 1:] = 4
    
        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                for k in range(1, l3 + 1):
                    
                    score_gap = max(score[i - 1, j, k], score[i, j - 1, k], score[i, j, k - 1], score[i - 1, j - 1, k], score[i - 1, j, k - 1], score[i, j - 1, k - 1])
                    
                    if s1[i-1] == s2[j-1] and s1[i-1] == s3[k-1] and score[i-1, j-1, k-1] + 1 > score_gap:
                        
                        score[i, j, k] = score[i-1, j-1, k-1] + 1
                        
                        backtrack[i, j, k] = 1
                        
                    else:
                        
                        score[i, j, k] = score_gap

                        if score[i, j, k] == score[i - 1, j - 1, k]:
                            backtrack[i, j, k] = 2
                        
                        elif score[i, j, k] == score[i - 1, j, k - 1]:
                            backtrack[i, j, k] = 3
                            
                        elif score[i, j, k] == score[i, j - 1, k - 1]:
                            backtrack[i, j, k] = 4
                            
                        elif score[i, j, k] == score[i - 1, j, k]:
                            backtrack[i, j, k] = 5
                        
                        elif score[i, j, k] == score[i, j - 1, k]:
                            backtrack[i, j, k] = 6
                            
                        elif score[i, j, k] == score[i, j, k - 1]:
                            backtrack[i, j, k] = 7

        return score[l1, l2, l3], backtrack
    
    def test(self):
        s1 = 'ATATCGG'
        s2 = 'TCCGA'
        s3 = 'ATGTACTG'
        score, gapped_s1, gapped_s2, gapped_s3 = self.find_triple_lcs(s1, s2, s3, 'global')
        print(score)
        print(gapped_s1)
        print(gapped_s2)
        print(gapped_s3)