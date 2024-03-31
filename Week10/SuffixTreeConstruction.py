from typing import List, Dict, Tuple
from TrieConstruction import modified_trie_construction
from util import dictionary_to_trie

def tree_construction(text: str):

    # merging the tree rooted at node
    def merge_dfs(tree_dictionary_: Dict[int, Dict[int, Tuple[str, int]]], trie_dictionary_: Dict[int, Dict[int, Tuple[str, int]]], node_: int, current_edge_: Tuple[int, int, int, int]) -> Dict[int, Dict[int, Tuple[int, int]]]:

        # merge the current edge
        def merge(tree_dictionary__: Dict[int, Dict[int, Tuple[str, int]]], current_edge__: List[int]) -> None:
            ori__, des__, ori_idx__, edge_length__ = current_edge__
            if edge_length__ < 1:
                return
            if ori__ not in tree_dictionary__:
                tree_dictionary__[ori__] = {}
            tree_dictionary__[ori__][des__] = (ori_idx__, edge_length__)

        # updates current edge
        def updates(current_edge__: Tuple[int, int, int, int], node__: int) -> None:
            return (current_edge__[0], node__, current_edge__[2], current_edge__[3] + 1)

        if node_ not in trie_dictionary_:
            merge(tree_dictionary_, current_edge_)

        elif len(trie_dictionary_[node_]) == 1:
            child_ = list(trie_dictionary_[node_].keys())[0]
            current_edge_ = updates(current_edge_, child_)
            merge_dfs(tree_dictionary_, trie_dictionary_, child_, current_edge_)

        else:
            merge(tree_dictionary_, current_edge_)
            for child_, v_ in trie_dictionary_[node_].items():
                current_edge_ = (node_, child_, v_[1], 1)
                merge_dfs(tree_dictionary_, trie_dictionary_, child_, current_edge_)

        return
    
    trie_dictionary = modified_trie_construction(text)
    
    # edge_starts, edge_ends, edge_starts_idx, edge_length
    current_edge = (0, 0, 0, 0)

    tree_dictionary = {}
    merge_dfs(tree_dictionary, trie_dictionary, 0, current_edge)

    return tree_dictionary

    tree = dictionary_to_trie(tree_dictionary)
    edges = [text[item[2][0]:item[2][0]+ item[2][1]] for item in tree]
    return edges
