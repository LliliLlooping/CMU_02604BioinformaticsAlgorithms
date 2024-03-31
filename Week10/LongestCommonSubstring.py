from SuffixTreeConstruction import tree_construction
from typing import Dict, List, Tuple

def find_longest_repeated_substring(text1: str, text2: str) -> List[str]:
    
    def dfs(tree_dictionary_: Dict[int, Dict[int, Tuple[int, int]]], text1_: str, text2_: str, current_node_: int, current_string_: str, strings: List[str]) -> None:

        if current_node_ in tree_dictionary_:
            for child_, tp_ in tree_dictionary_[current_node_].items():
                starts_, length_ = tp_

                if length_ > len(text2_):
                    text1_substring_ = text1[starts_:starts_+len(text2_)]
                    text2_substring_ = text2_
                    for i in reversed(range(1, len(text2_)+1)):
                        if text2_substring_[:i] == text1_substring_[:i]:
                            strings.append(current_string_+text2_substring_[:i])
                            return

                else:
                    text1_substring_ = text1[starts_:starts_+length_]
                    text2_substring_ = text2_[:length_]
                    for i in reversed(range(1, length_+1)):
                        if text2_substring_[:i] == text1_substring_[:i]:
                            strings.append(current_string_+text2_substring_[:i])
                            dfs(tree_dictionary_, text1_, text2_[length_:], child_, current_string_+text2_substring_[:i], strings)
                            break

    # build suffix tree
    text1 += '$'
    tree1_dictionary = tree_construction(text1) 

    print(tree1_dictionary)

    # dfs to check if shared
    strings = []
    for i in reversed(range(len(text2))):
        suffix = text2[i:]
        dfs(tree1_dictionary, text1, suffix, 0, '', strings)
    
    # process result
    if len(strings) == 0:
        return ['']
    
    max_length = max(map(lambda item: len(item), strings))
    strings = [item for item in strings if len(item) == max_length]

    return strings
    