from typing import Dict, List, Tuple
from SuffixTreeConstruction import tree_construction
from concurrent.futures import ThreadPoolExecutor, as_completed


def patterns_matching(text: str, patterns: List[str]) -> Dict[str, List[int]]:

    text += '$'
    suffix_tree_dictionary = tree_construction(text)
    
    def task(pattern):
        def pattern_matching(pattern_: str) -> List[int]:

            def dfs(pattern__: str, current_node__: int, start_indices__: List[str], start_end__: Tuple[int, int]) -> None:

                if current_node__ not in suffix_tree_dictionary:

                    start_indices__.append(start_end__[0])
                
                else:
                    
                    for child__, tp__ in suffix_tree_dictionary[current_node__].items():

                        edge_start__, edge_length__ = tp__
                        
                        if edge_length__ < len(pattern__):
                            if text[edge_start__:edge_start__+edge_length__] == pattern__[:edge_length__]:
                                dfs(pattern__[edge_length__:], child__, start_indices__, (edge_start__-(start_end__[1]-start_end__[0]), edge_start__+edge_length__))
                        else:
                            if text[edge_start__:edge_start__+len(pattern__)] == pattern__:
                                dfs(pattern__[len(pattern__):], child__, start_indices__, (edge_start__-(start_end__[1]-start_end__[0]), edge_start__+edge_length__))

            current_node_, start_indices_, start_end_ = 0, [], (0, 0)
            dfs(pattern_, current_node_, start_indices_, start_end_)

            return start_indices_
        
        return pattern, pattern_matching(pattern)

    results = {}
    with ThreadPoolExecutor(max_workers=12) as executor:
        
        futures = [executor.submit(task, pattern) for pattern in patterns]
        
        for future in as_completed(futures):
            pattern, matches = future.result()
            results[pattern] = matches

    return results



def approximate_patterns_matching(text: str, patterns: List[str], tolerance: int) -> Dict[str, List[int]]:

    # text += '$'
    suffix_tree_dictionary = tree_construction(text)
    print(suffix_tree_dictionary)
    
    def pattern_matching(pattern_: str) -> List[int]:

        def dfs(pattern__: str, current_node__: int, start_indices__: List[str], start_end__: Tuple[int, int], d: int) -> None:

            def compare(s1: str, s2: str): 
                assert len(s1) == len(s2)
                return sum([1 for i in range(len(s1)) if s1[i] != s2[i]])

            if current_node__ not in suffix_tree_dictionary:
                if len(pattern__) == 0:
                    start_indices__.append(start_end__[0])
            
            else:
                
                for child__, tp__ in suffix_tree_dictionary[current_node__].items():

                    edge_start__, edge_length__ = tp__
                    
                    if edge_length__ < len(pattern__):
                        mismatch = compare(text[edge_start__:edge_start__+edge_length__], pattern__[:edge_length__])
                        if mismatch <= d:
                            dfs(pattern__[edge_length__:], child__, start_indices__, (edge_start__-(start_end__[1]-start_end__[0]), edge_start__+edge_length__), d-mismatch)
                    else:
                        mismatch = compare(text[edge_start__:edge_start__+len(pattern__)], pattern__)
                        if mismatch <= d:
                            dfs(pattern__[len(pattern__):], child__, start_indices__, (edge_start__-(start_end__[1]-start_end__[0]), edge_start__+edge_length__), d-mismatch)

        current_node_, start_indices_, start_end_ = 0, [], (0, 0)
        dfs(pattern_, current_node_, start_indices_, start_end_, tolerance)

        return start_indices_
    


    results = {}
    for pattern in patterns:
        results[pattern] = pattern_matching(pattern)

    return results

