rnaToAA = {
    'AAA': 'K',
    'AAC': 'N',
    'AAG': 'K',
    'AAU': 'N',
    'ACA': 'T',
    'ACC': 'T',
    'ACG': 'T',
    'ACU': 'T',
    'AGA': 'R',
    'AGC': 'S',
    'AGG': 'R',
    'AGU': 'S',
    'AUA': 'I',
    'AUC': 'I',
    'AUG': 'M',
    'AUU': 'I',
    'CAA': 'Q',
    'CAC': 'H',
    'CAG': 'Q',
    'CAU': 'H',
    'CCA': 'P',
    'CCC': 'P',
    'CCG': 'P',
    'CCU': 'P',
    'CGA': 'R',
    'CGC': 'R',
    'CGG': 'R',
    'CGU': 'R',
    'CUA': 'L',
    'CUC': 'L',
    'CUG': 'L',
    'CUU': 'L',
    'GAA': 'E',
    'GAC': 'D',
    'GAG': 'E',
    'GAU': 'D',
    'GCA': 'A',
    'GCC': 'A',
    'GCG': 'A',
    'GCU': 'A',
    'GGA': 'G',
    'GGC': 'G',
    'GGG': 'G',
    'GGU': 'G',
    'GUA': 'V',
    'GUC': 'V',
    'GUG': 'V',
    'GUU': 'V',
    'UAC': 'Y',
    'UAU': 'Y',
    'UCA': 'S',
    'UCC': 'S',
    'UCG': 'S',
    'UCU': 'S',
    'UGC': 'C',
    'UGG': 'W',
    'UGU': 'C',
    'UUA': 'L',
    'UUC': 'F',
    'UUG': 'L',
    'UUU': 'F'
}


def DnaToRna(dnaText):
    return dnaText.replace('T', 'U')


def RnaToDna(rnaText):
    return rnaText.replace('U', 'T')


def CheckText(text, aaString, results, geneticCode):

    # Calculate the length of the reading frame
    lengthReadingFrame = len(aaString) * 3

    for i in range(0, len(text), 3):

        # Visit all possible reading frames
        readingFrame = text[i:i+lengthReadingFrame]
        if len(readingFrame) < lengthReadingFrame:
            return

        # Store all valid reading frames
        CheckReadingFrame(readingFrame, aaString, results, geneticCode)

    return


def CheckReadingFrame(readingFrame, aaString, results, geneticCode):
    lengthAa = len(aaString)
    for i in range(lengthAa):
        kmer = readingFrame[i * 3: (i+1) * 3]
        aa = aaString[i]
        if kmer not in geneticCode or geneticCode[kmer] != aa:
            return
    results.append(readingFrame)


DnaComplement = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}


def ReverseComplement(dnaText, dicComplement=DnaComplement):
    reversed = dnaText[::-1]
    complemented = ''.join([dicComplement[s] for s in reversed])
    return complemented


def PeptideEncoding(dnaText, aaString, geneticCode=rnaToAA):
    """
        Peptide Encoding Problem: Find substrings of a genome encoding a given amino acid sequence.

        Input: A DNA string Text, an amino acid string Peptide, and the array GeneticCode.
        Output: All substrings of Text encoding Peptide (if any such substrings exist).
    """

    # Generate the forward RNA text
    forwardRnaText = DnaToRna(dnaText)

    # Generate the backward RNA text
    backwardRnaText = DnaToRna(ReverseComplement(dnaText))

    # Check six possible reading frames
    forwardResults, backwardResults = [], []
    for offset in [0, 1, 2]:
        CheckText(forwardRnaText[offset:], aaString,
                  forwardResults, geneticCode)
        CheckText(backwardRnaText[offset:], aaString,
                  backwardResults, geneticCode)

    # Translate all results from rna back ro dna, and
    # reverse complement back all results from the reverse-complement string
    forwardResults = [RnaToDna(rna) for rna in forwardResults]
    backwardResults = [ReverseComplement(
        RnaToDna(result)) for result in backwardResults]

    results = forwardResults + backwardResults

    return results


######################################################################
########################## Debugging Runs ############################
######################################################################

# text = 'TTCGAATCCGTATTGCTTTGGTTGGTTGAGAGAGCGACCTACATTGCTAGTCAGAATAGGTGATTCACACAAAGCTTAGCACCTGGGCAGCACCCCGTGATGTAAACCTATGGGAACTAAGGGAGTCCTGCGGTTTTAGCCAGCAAGCGAGCCGGCAGGAACACTCATACCATCGGACGCGTTTGACGCCTCCCCGGAAAGGAAGTATTTGAGCCTCATTATTACGTATTGCCCGTTAGTCGACAAATCAAGCCCTCGTACGCAGCTTATTCGTACGACGTGGAGGCGTTCCCACGGGCCTAACACGATTGGAACACCACCATAGTAGTGTGGTTCAAATACCTCCTTTGGAGATCTAGAGCTTCACTCTGATTCTAGAGGCAACTTTACAATCGCTCTACGAAATTGTATGGACATCATCAACCGGATATTCTGGGGCGGTAGAATTTCTTTTGTTCGAATCGCTCTAGGCCAGGATCAAATTAATTGAATTGCGGACTCAAGGATCGCGATAGCCGACACATCGGACGCTGTAGAAAGCCAGTCTCTGGATTTAATCCACCCTCTATGTTTGACAAAGCACTAAAACGGGATAGTTTCGGGTGGTATAAGTTTCCCAAGACGATTGCATCGCAATTCATCAACAACCATGAACTTACTGTTTTAGTACTTCCACACACCTTGTTAAATTACGCCTTTACTTCATGTTGCGGTGTGTGTTAGATAGTGTGCAGCTACAAGTCTACCGCCATCGCAGCTCGGGATACCGGCAGATGAGATGGTCCTGAGCTCGTACCGGACTCAAACTTTTTCCTTTACTACCTAGGAATCGCCCATGCGAATTTGTCGGACACACACCATTACATTAACGTCACAACAGCTACTGTTAGAATTTTGCTCTTGCAAATCCTGGAAAGAGTTAAAAAAACTCTTCCGCGCGCCAATAGGGTAAATAATAGATAGCCAGACGGCTGTAAGAGGTGATGACATTTGCAACAATCATGCTGTCGCATCTTCCGCAAGTTCATGTCGCGCCTAGGCAATGGATCTGCGAATGGGGGCCACGGGGTATGAACTACGGAATTCTAAGAAAGTTGCCATCCAGAGTTAAGGGTTTGAGGCTAGTTGCATCGCTGGTAACGAACTACCTCATTACTTGGACGCGCAGTGTGACTTCACTCCTGTATAGCGATGATGCCAAGCAGGAATTAGCAAATCTGAAGAGCGTTTCCAAACTGGCCACTTGGACTGACACCTATCGCGGGGGATTTCAGCGCGTGTCGCTCTCACATGAGAGCTGCCGTCAGGAGCGGTAGAGTTTAGAGAGGAATGCGACAAACTCCCTATTCACCTCTCTGGTGATGTAAGGATATTTACGCTTAGTTCTATGCCAGGCTTAGGGCCTCTCGGAACTTTGGTGAGTCCTTATTAATTGATGCTACCTCTCCCTTACCTTCGCCCCAAGTCACGTAGAAGTACTCAATCCTGCTACATGATAATCAAATATTTCCAACGTTGGGAAATCGGTGACATCACATACTAGTTAAGAAACCACTGTCAGTGAACTTATATCCGGGGGAGAAAATCTACTAACTTACATACGCTGTGCGAGCAGTTTTCATTATAAGAAAATATACTCCCGAGGTACCGCATCAAGCACGACATTCCCGGAGAGCATAACATTTCGGTGCACCTGCTTTTGTGCGCTTGCTTGCGGTTATTTATAAACTACGCACAAGGCGCAAACCGCAGTGCGCATGTTTTCTCCGCCTGGCTAGAACTCGACATTCTCGTCAACGCCAATCTATGTGAGAGGATTTAGACCTCTGTGAAAACGAGTCCCTCTATAGAATAAATACCCAGATGCCAATGGGGGTTCTATCCGATGGCAGTGCATGGAGTGGTGGCTCCAGATTAAGGATGAGGAGAGGTAAAGATAACAGTTCGGTCGCCACGACGCGTTGCCAATCGAAATATCAGTACTAAAAGGCCCACCGCTCCGCTTTAGTCCGACTTTACATCCTGTGGAAATTGTCGAACGGAGGCTACATCGGGCTATATGAGTGTGAAAACCTATACTTCTCGCGTCGTTACTCAGTGCCGGTCTCCTGTTTCCCCCAGTCTTACGTACCCTTATTGATATTTGCTTCACGTTGAAACGTCCTAACGCAGCGTAAAGAGGTGTTTGAACCTCATTACTATAAAATCGCGATCGAAGGTAGACTACATACGCAAACGCCGAAACCCTCAGTTGGCCTTGTTGCAAGTATGGAACGTTGTAAAATTTTTCCTAGACGTTGAGCTATCGGTACAAGGTCGTTAGCGTCCTTACCCTTCACTTATATGCCCGACAAAACGCGGGTCCTAGTGCAGTGGTGGGAGCTTGGAATCCCGCAATACAAGGACAACCTGTATCTCGTTCGGCGTTCCGCGATCACTCGATCCCGAACCACTCCAAGCCTGGTTGATCAGCAAAAGCGGAAGGATGGATAAAGGGCTACTGGTTAATGGATGTAAACTTCCAATGATGAAATCCTGGAAACGAGGGATCGGGTTACGGTGGCGAACGGGGTACGGCAACGTGGCTATCTAGAGCCCGACGTTACGACTCATGTACATGCTGCTACGTGGTTGAAGCTGACGTTCAGATGAAGCAGTACTGAGTCCTAGGGCTTACTACTACTCCAATAGGTCTGGCCGGCCAGATACAAAAGTTCGTGGCGGCTCACCCCCTTTCTGGCGGGTGTAGCTTGCTGACCGGTTTGCTCGATAACACAGGCTAGCGAATAGTAATGAGGTTCGAAAACCTCTTTCCAACGACTGAAAGGGTCTACACGAACTATCTACATTTCCCCGCCCATGTCCTTCCGTCTGGTTGCTTCTGGAGATCCTTTCGCATTATACCGCAGCGTAGTGGCTCTGGCATATATGAAAAAATCCTTCTGTGGGTATTTGTGCCATCACTTATTGTTCGTACCGATATGGGATTACAAGTGCGATGTGATAATAAGCGAAGAAGCCAACATGTTACACTGTTCATGCGCTCCGGGTAATGTGCGGGCACCATGCTCAGTTCCCGCTCGCAGTTGTCACTGTCCCTGTTTCGGCACCATAATCAACATTTCCACGGCCACGCTGGTGAATAACCGAGGATACCGAAGTACAGCAAGAATGAGAGCGGGACTCCTCCATCTGCTTGTAATACGCCTTCAAGATAGTCCATAAAACGGTCGGGGTCTTGTTTCGGACTAGCCGCTTTGAAACGGTGCATAGTTGTGTCAAGTGTGGACATTGGCTTTCTATCCTCGTCAGCGATCCTCGGAAAGACTCGGGCAGTCGCCCCGAATCGTAATTAGGTAGTAGTGCGGCTCAAAAACTTCCTTCGACCTAACCGCTATAATGTTCGTAGATATAAATTTCGTTTCAGTATTAACAGGCGCACCGTATATATACGGAATGGTGTCGCCCCATTAGCTGCTCGCCAATATTTATCTAAGACCGCGCGCGTCTAGCGCCTTTAGTAGTTGCACCCGAGTATAGTAATGGGGTTCGAAGACTTCCTTCGCAAGGCTGCCATACTGTATCACAAGTACTGACGGAGCCCCGGAGGAGTGCAGGATACGGCAAAGGAGACCATTACCGGGGCATGAGTCCAAGTTAGCCCGTTAGGTGAAGGACGCTGATACAATAGTGAATCCGTTACTGAAAGGTTTAGAAGACCGGGGGGCTCGCACTAGGTCCAAATATTATGAACCCTACTCCTGCAACTGAATTGGCCGTCCAGGCGATATTTAAAAGGGGTTACTAGCAGGTTCATCGGAGCCCGTACTCCTTCCGGGCATAGTCGTTCGACGGGTAGAAATTCATCCAGTCGTGCCGGATACCCCGAGAATACCCCTATTTTTTGATCCTTCACCATCATCGTCCGCGGACTCATCTAAGTACCTCAGACCGAAACTGTTATCGTAGCGAAGAGCGAACTCGAATGACATCGCTTGTCCAACAGGGAAAATATGTAAAGTATATGCAGATTATTATAGGAAGATCACAAACTCCATCGCGCCTAGGCCAAAGACTTGCCAGAACAACATCTCTTCCAGAGCAAGGAAGTGTTTGAACCTCACTATTATCGAGAGAAGTCCCATGAATTTATAATAGTGAGGCTCAAAAACTTCCTTCATCGTCGGGCGCTGGGGCGAGCTAGGCTTCCCTAGCCGTCATTACTGTACCCACGCCAAATATTATCGAGTATGACTACGAAGCCTTCACAAGGGGCTGCAGTAACAGACTAACTCACGCACACCGCAACTACTATCCTAAATTGAGTAAGAAAACCCTCGACTATAGCCCTTGAATTAAATTCGCTATTTAAGGAAGACCGCGCTTCCGCTCGCCCGCGTATAGTTTACCAGTCCCAAGAAACATGTGTGGCCAGCCTACCTGAAGAGCTGTGTAAAGATAGATTCTGACATCCTCAAAAAGAAGTTTTCGAGCCGCACTACTACGCACGGAGCTCCGTTATTCAAGGCATGTCGAAGTACAGCGTGGTGGCCTCTCCTGTTCTCCACCCCAGCTAAACCCACCTTGTTCGAATTCGCGCAACTGTATATGACATGAACACTTACAGGGGTTAGAAGTTACTGCAACCAAGATAGAGCTCGTCGAAGTAATAGTGCGGTTCAAAAACTTCCTTCAATTGGTCTCATCACTTAAATTTAAGAGCTATTGTGAGTACAGGTACGGATGCGGCTTCAGTGGATCTTCAGCATTCATTCCTTGTAGTAATGGGGTTCGAAGACTTCCTTGCCAGGGTACCAAACAAGTCTTGCGCATCCTCCTCCCTAAGGAGGTATTTGAACCCCACTATTACCCACGATAGAACATGCAGGGTTTGATAGTGGAACACCTTTTAGAATCTGGGGATAAATTCCCAGGACTAATGTATGGCTGTAGTAATGAGGTTCAAAAACCTCCTTTTCAGGTGGATCGCAGGCCGTGCTGCCTCACAAGCTGGGACGCCGTCCACGGTATAGCCGGCGTCGGCAGTTACTGTGAAATAGCGGAAACTCGATCCCAATATATCATCTTACGTTTGGCGCCCAATAGTCGCCCAGTACCCGTTGACAGTTCTTTAACTCGGCTTAGAACTACTAGACAGGTTCAACCGAACCTTGCCCTAGTTCCCACTCCCGTAATTCATTTGGGTTTGCATCTAGAATACTGGAGGGTGCATAGACGAAACGTGTACGTCGGAGAAAACGTAAGAAAATGACCTAGACTCATAGTAGTGAGGTTCGAAGACTTCCTTTCAGTGAAATCGATCCACCACTCGCCGCGAAGAGATAATAGCATAGAGCACAAGTGCGCGAGTAGAGAAAAAGGCTATCCCAACCGGGCACGTCCTTCGTGTTTGGCGTTTACATACGGCACCCCGTTTCTGCACGTTAACCGTCTAGTATCCAACGGTGGATGGCGGACGCTAGACTATAGATATGAGATATCGAGACCTGGAGCTGGGTGTGGCTGCAGCCCGGGTCATTGCGGGCTGTGAATTCAAGGGCATGTAAACAAGCGTATATCGAACAGTGGATGGGCACCTGCAATACTCACGGTAGAGTTAGCTCACAGGATTCACGTTGAGGACTATGAGTCCCTCTTCGCTAGCAGTCTGGGGGGATATGGAGTTTAATAGCTTGACGTAGTAATGGGGCTCAAACACCTCTTTGTGTGAGCACAGCTACTTGCATTAAGAGATTCTAAACAGCGATCATCTCGGCTATTTCGGGCCAGCCTTTTCGGCAGGATGTTATGTAGCATTTCTGGAAGCTTCCCCCTCGAATCTACTAGTGGTGAGAAGATGCCCCACCGATATTACTCTTTAATCTTGAGAAACCTAAAACCGATCTGACCTCAGACGGGCGGCTCCCACCCGAGGATAAACTCGTCAATAATAATGTGGCTCGAACACTTCTTTTCTCACTAGGCTTTTACGACACGCCACATGTATTTAAGCATCTACCTAACTTGTGTCTGCTGATATACAGCGCATTCTACGCCCAACCTACCAATTACTTCAACGTAGTGCGTGGCTAAAATTCAGGGGAGCTTCATCTCTGTCTTAATTTGAAGGTTCTTCCGGGGCGTTTGGGAATCTTCGTGCCTTTTGCGAGGTTAAGGTATCAAAGAAGTTTTCGAACCACATTATTACCGCCTTAAGCACCGGCGCATCCTGCTCGTGACAACTCTACCCTGCCCTGATAAAGGCACTGAACGTTCCAGAGAGTGCATCATTGACACGCGAGCAGGCCACAGTAGCCACAAGACGTATGGGTGATTATAGAATTGGTGGAGGTGTTGTTAACGATCAGGAGGACATTAGTGGGAGTTAGGAAAGACCCTATGTTCTCTCTATCGCGGACTTGTAACTTGACAAGCAAAAGGGTAAGAGAGCTGCACACCGAAGCAGGCCCTTCCTATACCTGTTTTTCCTACGCGTAGAGAGGAATCCAGAAAGGTGATAATTGGCATTCGATGAAAAAACAGTGTGCCACTGACTTAGTTCTATATGTGAAGAGCCTGTTAGCACGTGACGGCGGCCTTGGTATAGAGCCCTTAATGGTCTCCATCGCGTAGTAATGGGGCTCGAAAACCTCCTTACTTGGGATTGCGTGGCCTCCTTGTGAGTCATACACAAGGCTTAGGGCTATGGGGCGATACACTCCTTTTCGCGGCGCATGGGGCGGTGATGCCTACATAGTAGTAGTGACTGCCTTTCTGGGGGGCTATTTGTGGATGACCAACACCTGACCAGCGATGCAATCGCTAGGGGAGGTACACCTCTCATATGTTACAACAATCACCGAATTGTGTTTCGAATTCGAATCAAGTTTGCGGTGTCGACCAGATCTGGTCTTGCTGCCATACCGGGTTCGCCGCCTCCGGTGGATAGAACTGCATCTTAAGACATCTGGACCCAGCGGTAAGTAGCGGGAAGAGTTTAGAGTCATTCGTACAACTACAGGCTAAGGGCTTACTGGGGAGTTGTTGTAGGGCATAAAGATCGCCCCATGACTTTTCGTACTTTCCCCGATAGTTCACTCGCAGCGAGCTGCGGCTGGGCTTCGCCACACGAGTACGGGCAACATTTATCTCCTCTAATCACTGGGCACCGCGCGAGGAAATAGAAAACCCTAATCAGTGCTCATGGGCGCATCTATTGGTCTCCGCATGCACGATGCCGCGGAGTGCTTAGTTGTCCCTGCATAATCTTCGTAGATGTATAAGAGATTACCTATTTATTCGGTTTCGGTTCTAGACGTACCTTGCCGCATGAGTATAGGCTAATGAACTGAGTTGGCGCCAGAGGGAAAGGCATAATAATGCGGCTCGAATACTTCCTTAAGGAAGTATTCGAACCACATTACTAT'
# aa = 'KEVFEPHYY'

# text = 'ATGGCCATGGCCCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA'
# aa = 'MA'

# text = 'GAAACT'
# aa = 'SF'

# results = PeptideEncoding(text, aa)
# for result in results:
#     print(result)


# with open('BacillusBrevis.txt', 'r') as file:
#     data = file.readlines()

# text = ''
# for line in data:
#     text += line[:-1]
# text += data[-1][-1]

# aa = 'VKLFPWFNQY'
# results = PeptideEncoding(text, aa)
# print(len(results))
