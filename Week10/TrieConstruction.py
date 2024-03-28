from typing import List, Tuple, Dict

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

    def dictionary_to_trie(trie_dictionary_: Dict[int, Dict[int, str]]) -> None:
        trie_ = []
        for ori_, ori_dic_ in trie_dictionary_.items():
            for des_, char_ in ori_dic_.items():
                trie_.append((ori_, des_, char_))
        return trie_
    
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
