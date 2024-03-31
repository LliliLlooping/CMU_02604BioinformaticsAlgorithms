from typing import List

def suffix_array_construction(text: str) -> List[int]:

    # adds a dollor sign to the end
    text += '$'

    # stores (starting position, suffix) pairs
    pairs = []
    for i in range(len(text)):
        suffix = text[i:]
        pairs.append((i, suffix))
    
    # sorts by suffix
    pairs.sort(key=lambda x: x[1])

    # gets the sorted starting position
    arr = map(lambda x: x[0], pairs)

    return arr