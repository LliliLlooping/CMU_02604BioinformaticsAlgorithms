from copy import deepcopy

class GreedySorting:
    
    def __init__(self):
        pass
    
    def sort(self, permutation):
        output = []
        for i in range(1, len(permutation) + 1):
            if permutation[i-1] != i:
                self.sort_util(permutation, i, output)
                # print(output)
        return output

    def sort_util(self, permutation, k, output):
        if k in permutation:
            target_index = permutation.index(k)
            self.reverse(output, permutation, k-1, target_index)
            self.reverse(output, permutation, k-1, k-1)
        else:
            target_index = permutation.index(-k)
            self.reverse(output, permutation, k-1, target_index)
        
    def reverse(self, output, permutation, start, end):
        for i in range((end - start) // 2 + 1):
            self.swap(permutation, start + i, end - i)
        self.display(permutation)
        output.append(deepcopy(permutation))
            
    def swap(self, permutation, left_index, right_index):
        tmp = permutation[right_index]
        permutation[right_index] = -permutation[left_index]
        permutation[left_index] = -tmp
    
    def display(self, permutation):
        s = ''
        for x in permutation:
            if x > 0:
                s += '+' + str(x) + ' '
            else:
                s += str(x) + ' '
        s = s[:-1]
        print(s)
        
        
        
    def test(self):
        with open('input.txt', 'r') as file:
            permutation = [int(x) for x in file.read().split(' ')]
        output = self.sort(permutation)
        # print(output)