import sys
import csv
import time
from pyeda.inter import espresso_exprs
from findpcu import getUnobservedInts, getRespvarList2BoolvarList, intList2boolexpr, boolexpr2RespvalList

#webNo = 1
#for webNo in range(1,4):
if True:
    if True:
        fInName = 'uniques_web2.csv'

        str4true = 'pos'
        str4false = 'neg'

        # = Read in the header, which creates allResponses, and order our desiredResponses to correspond to that
        a = time.clock()
        print('a')

        fIn = open(fInName)
        csv_f = csv.reader(fIn)
        allResponses = next(csv_f)
        fIn.close()

        # Sort our desiredResponses according to the order they appear in allResponses
        desiredResponses = allResponses

        boolLen = len(desiredResponses)

        # = Get all of our unobserved combinations of desiredResponses as a set of integers

        # A mask to take out only those entries in our desiredResponses
        desiredResponsesMask = [True if aR in desiredResponses else False for aR in allResponses]

        unobservedInts = getUnobservedInts(fInName, desiredResponsesMask, boolLen, str4true)

        # = Turn our set of unobserveds into a boolean expression =
        b = time.clock()
        print('b')

        # Create our boolean variables and some useful dictionaries
        x, x2s, r2idx = getRespvarList2BoolvarList(desiredResponses, str4true, str4false)

        # Turn each integer representing unobserved into a
        # boolean-and into boolean expression 
        unobservedBoolexpr = intList2boolexpr(unobservedInts, x)

        # = Use espresso to minimise the unobservedBoolexpr
        c = time.clock()
        print('c')

        boolExprMin, = espresso_exprs(unobservedBoolexpr)
        PCUList = boolexpr2RespvalList(boolExprMin, x2s)


        # = Write a file of the results
        d = time.clock()
        print('d')

        print(d-c)
        print(c-b)
        print(b-a)

        # Write the PCUs we've found to a file
        fOutName = fInName.split('.c')[0]
        fOutName = fOutName + '_pcus.py'

        fOut = open(fOutName,'w')

        # First write the desiredResponses, so we know on which part the search was done
        fOut.write('searchedResponses = [\'' + '\',\''.join(desiredResponses) + '\']\n')

        # Now write each PCU
        fOut.write('PCUList = [\n')
        for PCU in PCUList:
            fOut.write('[\'' + '\',\''.join(PCU) + '\'],\n')
        fOut.write(']\n')

        fOut.close()

