from typing import Dict

def dictionary_to_trie(trie_dictionary: Dict[int, Dict[int, str]]):
        trie = []
        for ori, ori_dic in trie_dictionary.items():
            for des, char in ori_dic.items():
                trie.append((ori, des, char))
        return trie

def read_patterns(path='./patterns.txt'):
    with open(path, 'r') as file:
        pattern_list = file.read().split(' ')
    return pattern_list