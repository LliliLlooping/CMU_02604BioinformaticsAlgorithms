from typing import List

def inverse_bwt_transform(transform: str) -> str:
    def find_next_char(first_col_: List[str], last_col_: List[str], row_idx_: int) -> int:
        char_ = first_col_[row_idx_]
        char_first_col_order_ = first_col_[:row_idx_].count(char_)
        next_row_idx_ = [i_ for i_, c_ in enumerate(last_col_) if c_ == char_][char_first_col_order_]
        return (next_row_idx_, first_col_[next_row_idx_])
    
    last_col = list(transform)
    first_col = sorted(last_col)
    text = ''
    next_row, next_char = find_next_char(first_col, last_col, 0)
    while next_char != '$':
        text += next_char
        next_row, next_char = find_next_char(first_col, last_col, next_row)
    return text + '$'