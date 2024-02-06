from IdentifyMotif import IdentifyMotif
from RandomizedMotifSearch import RandomizedMotifSearch
from GibbsMotifSearch import GibbsMotifSearch

identifyMotif = IdentifyMotif()
identifyMotif.test()

randomizedMotifSearch = RandomizedMotifSearch()
randomizedMotifSearch.test()

gibbsMotifSearch = GibbsMotifSearch()
gibbsMotifSearch.test()


print('All tests passed!')
