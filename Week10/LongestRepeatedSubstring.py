from typing import Dict, Tuple, List
from SuffixTreeConstruction import tree_construction

def find_longest_repeated_substring(text: str) -> str:

    def dfs(tree_dictionary_, text_: str, current_node_: int, current_edge_: str, edges_: List[str]):
        for child_, tp_ in tree_dictionary_[current_node_].items():
            if child_ in tree_dictionary_:
                edges.append(current_edge_ + text_[tp_[0]:tp_[0]+tp_[1]])
                dfs(tree_dictionary_, text_, child_, current_edge_ + text_[tp_[0]:tp_[0]+tp_[1]], edges_)

    # build suffix tree
    text += '$'
    tree_dictionary = tree_construction(text) 
    
    # use dfs to find all repeated substrings
    edges = []
    dfs(tree_dictionary, text, 0, '', edges)

    # output longest the substring
    if len(edges) == 0:
        return ''
    edges = list(map(lambda item: (item, len(item)), edges))
    edges.sort(key=lambda item: item[1], reverse=True)

    return edges[0][0]
