from typing import List, Tuple, Dict
from util import dictionary_to_trie

def trie_construction(patterns: List[str]) -> List[Tuple[int, int, str]]:
    
    def add_pattern_to_trie(pattern_: str, trie_dictionary_: Dict[int, Dict[int, str]], next_new_node_: int) -> int:
        
        def add_pattern_to_trie_recur(pattern__: str, trie_dictionary__: Dict[int, Dict[int, str]], next_new_node__: int, current_node__: int) -> int:
            
            def exists_edge(dic: Dict[int, Dict[int, str]], node: int, char: str):
                # checks if exists an edge labeled by char from node
                # return the destination of this edge if exists; otherwise -1
                if node not in dic:
                    return -1
                for k, v in dic[node].items():
                    if v == char:
                        return k
                return -1
            
            def adds_edge(dic: Dict[int, Dict[int, str]], edge: Tuple[int, int, str]) -> None:
                # adds a new edge
                ori, des, weight = edge
                if ori not in dic:
                    dic[ori] = {}
                dic[ori][des] = weight

            if not pattern__ or len(pattern__) < 0:
                return next_new_node__
            char__ = pattern__[0]
            destination__ = exists_edge(trie_dictionary__, current_node__, char__)

            if destination__ != -1:
                # if exists an edge: (current_node__, destination__, char__)
                next_new_node__ = add_pattern_to_trie_recur(pattern__[1:], trie_dictionary__, next_new_node__, destination__)
            else:
                # if not, adds a new edge
                adds_edge(trie_dictionary__, (current_node__, next_new_node__, char__))
                next_new_node__ = add_pattern_to_trie_recur(pattern__[1:], trie_dictionary__, next_new_node__ + 1, next_new_node__)
                
            return next_new_node__
        
        # starts from the root
        current_node_ = 0

        # recursively adds this pattern
        next_new_node_ = add_pattern_to_trie_recur(pattern_, trie_dictionary_, next_new_node_, current_node_)

        return next_new_node_
    
    # initialize trie_dictionary with an empty dictionary
    trie_dictionary = {}

    # initialize next_new_node with 0
    next_new_node = 1

    for pattern in patterns:
        # adds one pattern
        # updates next_new_node because next pattern still needs it
        next_new_node = add_pattern_to_trie(pattern, trie_dictionary, next_new_node)

    # convert into output format
    trie = dictionary_to_trie(trie_dictionary)

    return trie


def modified_trie_construction(text: str) -> Dict[int, Dict[int, Tuple[str, int]]]:

    def add_suffix_to_trie(text_: str, offset_: int, trie_dictionary_: Dict[int, Dict[int, str]], next_new_node_: int) -> None:
        def exists_edge(dic: Dict[int, Dict[int, str]], node: int, char: str):
                # checks if exists an edge labeled by char from node
                # return the destination of this edge if exists; otherwise -1
                if node not in dic:
                    return -1
                for k, v in dic[node].items():
                    if v[0] == char:
                        return k
                return -1
        
        def adds_edge(dic: Dict[int, Dict[int, str]], edge: Tuple[int, int, str, int]) -> None:
                # adds a new edge
                ori, des, weight, idx = edge
                if ori not in dic:
                    dic[ori] = {}
                dic[ori][des] = (weight, idx)
        
        suffix_ = text_[offset_:]
        current_node_ = 0
        for i_ in range(len(suffix_)):
            destination = exists_edge(trie_dictionary_, current_node_, suffix_[i_])
            if destination != -1:
                adds_edge(trie_dictionary_, (current_node_, destination, suffix_[i_], offset_ + i_))
                current_node_ = destination
            else:
                adds_edge(trie_dictionary_, (current_node_, next_new_node_, suffix_[i_], offset_ + i_))
                current_node_ = next_new_node_
                next_new_node_ += 1

        return next_new_node_

    
    # initialize trie_dictionary with an empty dictionary
    trie_dictionary = {}

    # initialize next_new_node with 0
    next_new_node = 1

    for offset in reversed(range(len(text))):

        # adds one suffix
        # updates next_new_node because next suffix still needs it
        next_new_node = add_suffix_to_trie(text, offset, trie_dictionary, next_new_node)

    return trie_dictionary
