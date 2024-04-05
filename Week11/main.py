import numpy as np
from BWT import bwt_transform
from InverseBWT import inverse_bwt_transform
from BWMatching import bw_matching

print(bwt_transform('ACCAACACTG$'))
# print(inverse_bwt_transform('G$CAGCTAGGG'))
# print(bw_matching('TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC', ['CCT', 'CAC', 'GAG', 'CAG', 'ATC']))