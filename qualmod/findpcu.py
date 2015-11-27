import csv
import time
from pyeda.boolalg.expr import exprvar, And, Or, Not
from bidict import bidict
from itertools import compress
from pyeda.inter import espresso_exprs

def int2boolset(i, x):
    """
    Accepts an integer i, a list of pyeda boolean variables x, and converts
    the integer into the set of boolean values corresponding to its
    representation in binary form. 
    
    For example, if there are four boolean variables, and it is given
    the integer 14, which has the binary representation "1110", then
    it will return the set {x[0], x[1], x[2], ~x[3]}.

    >>> respvarList = [ 'cat_goshawk', 'rat_goshawk', 'cat_tropicBird', 'rat_tropicBird']
    >>> boolvarList = list(map(exprvar, respvarList))
    >>> boolvarList
    [cat_goshawk, rat_goshawk, cat_tropicBird, rat_tropicBird]
    >>> boolset14 = int2boolset(14,boolvarList) # {cat_goshawk, cat_tropicBird, rat_goshawk, ~rat_tropicBird}
    >>> ~boolvarList[3] in boolset14
    True
    >>> boolset15 = int2boolset(15,boolvarList) # {cat_goshawk, cat_tropicBird, rat_goshawk, rat_tropicBird}
    >>> ~boolvarList[3] in boolset15
    False
    """

    boolLen = len(x)
    miniStr = '{:0' + str(boolLen) + 'b}'
    iBinstr = miniStr.format(i)
    boolset = set(xval if int(ival) else ~xval for ival,xval in zip(iBinstr,x))

    return boolset

def intList2boolexpr(unobservedInts, boolvarList):
    """
    The purpose of this function is to turn a list of integers into a
    pyeda boolean expression. Each integer is turned into its
    equivalent boolean and-product (see int2boolset), and then the
    boolean expression returned is the boolean or-sum of these
    and-products.

    >>> respvarList = [ 'cat_goshawk', 'rat_goshawk', 'cat_tropicBird', 'rat_tropicBird']
    >>> boolvarList = list(map(exprvar, respvarList))
    >>> unobservedInts = [14,15]
    >>> u = intList2boolexpr(unobservedInts, boolvarList)
    >>> ucheck = Or(And('cat_goshawk', 'rat_goshawk', 'cat_tropicBird', Not('rat_tropicBird')), And('cat_goshawk', 'rat_goshawk', 'cat_tropicBird', 'rat_tropicBird'))
    >>> u.equivalent(ucheck)
    True
    """

    unobservedAndsList = list()
    for i in unobservedInts:

        boolset = int2boolset(i,boolvarList)
        unobservedAndsList.append(And(*boolset))

    # Combine them with an Or to make the final expression
    unobservedBoolexpr = Or(*unobservedAndsList)

    return unobservedBoolexpr

def getRespvarList2BoolvarList(respvarList, str4true, str4false):
    """
    The purpose of this function is to create basic boolean algebra
    structures from a list of strings representing response variables
    (respvarList) and strings representing the response values mapping
    to true (str4true, a single string or list of strings) and false (str4false), which are used as
    prefixes. The structures it creates and returns are (1) a list of
    boolean variables, (2) a bidictionary mapping the boolean values
    to their string representations, and (3) a bidictionary mapping
    the string representations to an index for use with the list of
    boolean variables.

    >>> respvarList = [ 'cat_goshawk', 'cat_tropicBird' ]
    >>> boolvarList, boolval2respval, respval2idx = getRespvarList2BoolvarList(respvarList, 'pos', 'neg')
    >>> boolvarList
    [cat_goshawk, cat_tropicBird]
    >>> type(boolvarList[0])
    <class 'pyeda.boolalg.expr.Variable'>
    >>> type(boolval2respval)
    <class 'bidict._bidict.bidict'>
    >>> boolval2respval[ boolvarList[0] ]
    'poscat_goshawk'
    >>> boolval2respval.inv[ 'poscat_goshawk' ]
    cat_goshawk
    >>> boolval2respval.inv[ 'negcat_goshawk' ]
    ~cat_goshawk
    >>> respval2idx[ 'poscat_goshawk' ]
    1
    >>> respval2idx[ 'negcat_goshawk' ]
    -1
    """

    l = len(respvarList)
    boolvarList = list(map(exprvar, respvarList))

    respvalList = [''.join(str4true) + respvar for respvar in respvarList] + [''.join(str4false) + respvar for respvar in respvarList] 
    boolvalList = boolvarList + [~x for x in boolvarList]

    boolval2respval = bidict(zip( boolvalList, respvalList))
    respval2idx = bidict(zip( respvalList, list(range(1,l+1)) + [-i for i in range(1,l+1)] ))

    return boolvarList, boolval2respval, respval2idx

def boolexpr2RespvalList(boolexpr, x2s):
    '''
    Take a boolean expression and a bidictionary mapping 
    the boolean variables to their strings
    and return an ordered list of the equivalent
    value-response combinations as a list of strings

    >>> respvarList = [ 'cat_goshawk', 'cat_tropicBird' ]
    >>> boolvarList, boolval2respval, respval2idx = getRespvarList2BoolvarList(respvarList, 'pos', 'neg')
    >>> boolexpr = Or('cat_tropicBird', And(Not('cat_goshawk'),'cat_tropicBird'))
    >>> PCUList = boolexpr2RespvalList( boolexpr, boolval2respval )
    >>> PCUList[0]
    ['poscat_tropicBird']
    >>> 'poscat_tropicBird' in PCUList[1]
    True
    >>> 'negcat_goshawk' in PCUList[1]
    True
    '''

    (bDict, bLen, bSet) = boolexpr.encode_dnf()
    PCUList = [ [ x2s[bDict[idx]] for idx in boolPCU ] for boolPCU in bSet ]
    PCUList.sort(key=lambda PCU: len(PCU)) # Order them to make life easier for everyone, particularly me

    return PCUList

def getUnobservedInts(fInName, desiredResponsesMask, boolLen, str4true, subsetMask=None, subsetResponses=None):
    
    # TODO: change this so it accepts the file iterator instead

    # Open the csv and get our row iterator
    fIn = open(fInName)
    csv_f = csv.reader(fIn)

    # Skip the header row
    next(csv_f) 

    # Start with all possible responses as integers set ...
    unobservedInts = set(range(2**boolLen))
    # ... and loop through our rows, discarding the observeds
    for row in csv_f:

        if subsetMask == None:

            i = int(''.join(['1' if i in str4true else '0' for i in compress(row,desiredResponsesMask)]), 2)
            unobservedInts.discard(i)

        else:

            if tuple(compress(row, subsetMask)) == subsetResponses:

                i = int(''.join(['1' if i in str4true else '0' for i in compress(row,desiredResponsesMask)]), 2)
                unobservedInts.discard(i)

    fIn.close()

    return unobservedInts

# ----

def general_pcu_search(fInName, str4true, str4false, desiredResponses=None, subsetConstraints=None):
    '''
    Accepts a file containing comma-separated value rows of responses and minimises according to the desiredResponses and constraints imposed
    '''

    # = Read in the header, which creates allResponses, and order our desiredResponses to correspond to that
    a = time.clock()
    print('Started. Obtaining list of unobserveds ...')

    fIn = open(fInName)
    csv_f = csv.reader(fIn)
    allResponses = next(csv_f)
    fIn.close()

    # = Get subsetResponses, so that they're in order of appearance in the file we're using, they are the response outcomes we're including in the minimisation

    if subsetConstraints: 
        fileIdx = [allResponses.index(sR[0]) for sR in subsetConstraints]
        subsetResponses = tuple(zip(*sorted(zip(fileIdx,subsetConstraints))))[1]
        subsetResponses = tuple(zip(*subsetResponses)) #subset responses so it's ( (resp1, resp2, ...), (val1, val2, ...) ) in order of appearance
    else:
        subsetResponses = None

    # = Get desiredResponses, so that they're in order of appearance in the file we're using, they are the responses species we're including in the minimisation

    if desiredResponses:
        # Sort our desiredResponses according to the order they appear in allResponses
        fileIdx = [allResponses.index(dR) for dR in desiredResponses]
        desiredResponses = list(zip(*sorted(zip(fileIdx,desiredResponses))))[1]
    else:
        if subsetResponses:
            # Make sure our subsetted responses aren't included
            desiredResponses = list(filter(lambda r: not r in subsetResponses[0], allResponses))
        else:
            desiredResponses = allResponses

    boolLen = len(desiredResponses)

    # = Create masks

    desiredResponsesMask = [aR in desiredResponses for aR in allResponses]

    if subsetResponses:
        subsetMask = [r in subsetResponses[0] for r in allResponses]
    else:
        subsetMask = None

    # = Get all of our unobserved combinations of desiredResponses as a set of integers

    if subsetConstraints: 
        unobservedInts = getUnobservedInts(fInName, desiredResponsesMask, boolLen, str4true, subsetMask, subsetResponses[1])
    else:
        unobservedInts = getUnobservedInts(fInName, desiredResponsesMask, boolLen, str4true)

    # = Turn our set of unobserveds into a boolean expression =
    b = time.clock()
    print(b-a)
    print('List of unobserved obtained. Boolean expression being generated ...')

    # Create our boolean variables and some useful dictionaries
    x, x2s, r2idx = getRespvarList2BoolvarList(desiredResponses, str4true, str4false)

    # Turn each integer representing unobserved into a
    # boolean-and into boolean expression 
    unobservedBoolexpr = intList2boolexpr(unobservedInts, x)

    # = Use espresso to minimise the unobservedBoolexpr
    c = time.clock()
    print(c-b)
    print('Boolean expression generated. Minimisation being performed ...')

    boolExprMin, = espresso_exprs(unobservedBoolexpr)

    # Turn boolean expression into list of list of strings
    PCUList = boolexpr2RespvalList(boolExprMin, x2s)


    # = Write a file of the results
    d = time.clock()
    print(d-c)
    print('Minimisation complete.')

    # = Write the PCUs we've found to a file

    fOutName = fInName.split('.c')[0]

    if subsetConstraints:

        # Write the subsetMask as an integer, use as identifier for file
        subsetID = int(''.join(['1' if a else '0' for a in subsetMask]),2)
        fOutName = fOutName + '_sub' + str(subsetID) + '_pcus.py'

    else:

        # Use basic name
        fOutName = fOutName + '_pcus.py'

    fOut = open(fOutName,'w')
    print('Writing ' + fOutName + ' ...')

    # Write a preamble about the subsetting, if needed
    if subsetConstraints:

        fOut.write('# Minimisation performed on a subset subject to the following constraints\n')
        for sName, sConst in subsetConstraints:
            fOut.write('# ')
            fOut.write(sName + ': ' + sConst + '\n')

    # First write the desiredResponses, so we know on which part the search was done
    fOut.write('searchedResponses = [\'' + '\',\''.join(desiredResponses) + '\']\n')

    # Now write each PCU
    fOut.write('PCUList = [\n')
    for PCU in PCUList:
        fOut.write('[\'' + '\',\''.join(PCU) + '\'],\n')
    fOut.write(']\n')

    fOut.close()
