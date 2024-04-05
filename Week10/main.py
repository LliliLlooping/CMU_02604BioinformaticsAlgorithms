from util import read_patterns, read_patterns_matching
from TrieConstruction import trie_construction, modified_trie_construction
from SuffixTreeConstruction import tree_construction
from LongestRepeatedSubstring import find_longest_repeated_substring
from LongestCommonSubstring import find_longest_repeated_substring
from SuffixArrayConstruction import suffix_array_construction
from PatternsMatching import approximate_patterns_matching, patterns_matching

# patterns = read_patterns()
# print("Patterns: ", patterns)
# trie_1 = trie_construction(patterns)
# print(trie_1)

# text = patterns[0]
# trie_2 = modified_trie_construction(text)
# print(trie_2)


# tree = tree_construction(text)
# print(tree)

# longest_repeated_substring = find_longest_repeated_substring(text)
# print(longest_repeated_substring)
 
# text2 = patterns[1]
# print(find_longest_repeated_substring(text, text2))

# print(suffix_array_construction('DEADBEEFS'))

text, patterns = read_patterns_matching()
print(approximate_patterns_matching(text, patterns, 2))