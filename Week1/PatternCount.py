def PatternCount(text: str, pattern: str) -> int:
    """
        Sample Input:
            GCGCG
            GCG

        Sample Output:
            2
    """

    lenText, lenPattern = len(text), len(pattern)

    count = 0
    for idx in range(lenText - lenPattern + 1):
        if text[idx: idx + lenPattern] == pattern:
            count += 1

    return count
