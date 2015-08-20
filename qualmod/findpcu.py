import csv
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
    to true (str4true) and false (str4false), which are used as
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

    respvalList = [str4true + respvar for respvar in respvarList] + [str4false + respvar for respvar in respvarList] 
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

            i = int(''.join(['1' if i == str4true else '0' for i in compress(row,desiredResponsesMask)]), 2)
            unobservedInts.discard(i)

        else:

            if tuple(compress(row, subsetMask)) == subsetResponses:

                i = int(''.join(['1' if i == str4true else '0' for i in compress(row,desiredResponsesMask)]), 2)
                unobservedInts.discard(i)

    fIn.close()

    return unobservedInts

# ----

