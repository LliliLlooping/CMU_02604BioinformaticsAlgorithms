from MoneyChanging import  MoneyChanging
from ManhattanTourist import ManhattanTourist
from LCSeq import LongestCommonSubsequence
from DAG import DAG

money_changing = MoneyChanging()
money_changing.test()

manhattan_tourist = ManhattanTourist()
manhattan_tourist.test()

lcseq = LongestCommonSubsequence()
lcseq.test()

dag = DAG('./input_DAG_LongestPath.txt')
dag.test()