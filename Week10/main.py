from util import read_patterns
from TrieConstruction import trie_construction, modified_trie_construction
from SuffixTreeConstruction import tree_construction
from LongestRepeatedSubstring import find_longest_repeated_substring
from LongestCommonSubstring import find_longest_repeated_substring

patterns = read_patterns()
# print("Patterns: ", patterns)
# trie_1 = trie_construction(patterns)
# print(trie_1)

text = patterns[0]
# trie_2 = modified_trie_construction(text)
# print(trie_2)


# tree = tree_construction(text)
# print(tree)

# longest_repeated_substring = find_longest_repeated_substring(text)
# print(longest_repeated_substring)
 
text2 = patterns[1]
print(find_longest_repeated_substring(text, text2))