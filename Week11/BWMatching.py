from typing import List

def bw_matching(last_col: str, patterns: List[str]) -> List[int]:

    def bw_matching_single(last_col_: str, pattern_: str, last_to_first_: List[int]) -> int:
        top_, bottom_ = 0, len(last_col_) - 1
        while top_ <= bottom_:
            if len(pattern_) > 0:
                symbol_ = pattern_[-1]
                pattern_ = pattern_[:-1]
                if symbol_ in last_col_[top_:bottom_ + 1]:
                    for i_ in range(top_, bottom_ + 1):
                        if last_col_[i_] == symbol_:
                            top_idx_ = i_
                            break
                    for i_ in reversed(range(top_, bottom_ + 1)):
                        if last_col_[i_] == symbol_:
                            bottom_idx_ = i_
                            break
                    top_, bottom_ = last_to_first_[top_idx_], last_to_first_[bottom_idx_]
                else:
                    return 0
            else:
                return bottom_ - top_ + 1
        return -1

    def generate_last_to_first(last_col_: str) -> List[int]:
        last_to_first_ = [-1] * len(last_col_)
        first_col_ = sorted(last_col_)
        for i_, char_ in enumerate(first_col_):
            char_first_col_order_ = first_col_[:i_].count(char_)
            next_row_idx_ = [i_ for i_, c_ in enumerate(last_col_) if c_ == char_][char_first_col_order_]
            last_to_first_[next_row_idx_] = i_
        return last_to_first_

    last_to_first = generate_last_to_first(last_col)

    result = []
    for i in range(len(patterns)):
        result.append(bw_matching_single(last_col, patterns[i], last_to_first))
        
    return result