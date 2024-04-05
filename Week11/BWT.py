
def bwt_transform(text: str) -> str:
    return ''.join(map(lambda x: x[-1], sorted([text[i:] + text[:i] for i in range(len(text))])))