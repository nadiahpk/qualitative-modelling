import sys
import csv
import time
from pyeda.inter import espresso_exprs
from findpcu import getUnobservedInts, getRespvarList2BoolvarList, intList2boolexpr, boolexpr2RespvalList

#from uniques_0_pcus_150715_06_38_41 import PCUList as prevPCUList
prevPCUList = list()

# fInName = './sj1/uniques_0.csv'
fInName = str(sys.argv[1])

desiredResponses = ['inv_manzanita', 'inv_gopherSnake', 'inv_understoryPlants', 'inv_scrubOak', 'inv_skunk', 'inv_goldenEagle', 'inv_baldEagle', 'inv_willow', 'inv_openCupNestingPasserines', 'inv_raven', 'inv_treesBig', 'inv_fox', 'inv_raptorSmall', 'inv_mouse']

str4true = ['pos','zer']
str4false = 'neg'

# = Read in the header, which creates allResponses, and order our desiredResponses to correspond to that
a = time.clock()

fIn = open(fInName)
csv_f = csv.reader(fIn)
allResponses = next(csv_f)
fIn.close()

# Sort our desiredResponses according to the order they appear in allResponses
# TODO: probably not the simplest way to have done this
fileIdx = [allResponses.index(dR) for dR in desiredResponses]
desiredResponses = list(zip(*sorted(zip(fileIdx,desiredResponses))))[1]
boolLen = len(desiredResponses)


# = Get all of our unobserved combinations of desiredResponses as a set of integers

# A mask to take out only those entries in our desiredResponses
desiredResponsesMask = [True if aR in desiredResponses else False for aR in allResponses]

unobservedInts = getUnobservedInts(fInName, desiredResponsesMask, boolLen, str4true)


# = Turn our set of unobserveds into a boolean expression =
b = time.clock()

# Create our boolean variables and some useful dictionaries
x, x2s, r2idx = getRespvarList2BoolvarList(desiredResponses, str4true, str4false)

# Previously found, hardcode for now TODO
prevFound = list( set(x2s.inv[e] for e in PCU) for PCU in prevPCUList ) 

# Turn each integer representing unobserved into a
# boolean-and into boolean expression (except for those that
# appear in our previously found list, if specified)
unobservedBoolexpr = intList2boolexpr(unobservedInts, x)


# = Use espresso to minimise the unobservedBoolexpr
c = time.clock()

boolExprMin, = espresso_exprs(unobservedBoolexpr)
PCUList = boolexpr2RespvalList(boolExprMin, x2s)


# = Write a file of the results
d = time.clock()

print(d-c)
print(c-b)
print(b-a)

# Write the PCUs we've found to a file
fOutName = fInName.split('.c')[0]
fOutName = fOutName + '_pcus_' + time.strftime("%y%m%d_%I_%M_%S") + '.py'

fOut = open(fOutName,'w')

# First write the desiredResponses, so we know on which part the search was done
fOut.write('searchedResponses = [\'' + '\',\''.join(desiredResponses) + '\']\n')

# Now write each PCU
fOut.write('PCUList = [\n')
for PCU in PCUList:
    fOut.write('[\'' + '\',\''.join(PCU) + '\'],\n')
fOut.write(']\n')

fOut.close()

