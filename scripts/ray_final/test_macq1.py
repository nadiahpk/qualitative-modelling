import numpy as np
import imp # for importing from a python file
from qualmod import initialise_foodweb, qualitative_community_matrix


# =================================================================================

# Functions for drawing sample and validating

# = 1: Specifying the community-matrix elements directly =

# == 1.1: Methods of drawing elements for the community matrix ==

# Raymond Baseline
def raymondM(Mq):
    '''
    Returns a community matrix (Jacobian) corresponding to the
    qualitative matrix Mq with non-zero elements chosen as in Raymond et al. (2010)
    '''

    # |a_{ij}| ~ U(0.01,1)
    M = np.multiply(0.01 + 0.99*np.random.random_sample( Mq.shape ), Mq)

    # a_{ii} ~ U(-1,-0.25)
    for i in range(Mq.shape[0]):
        M[i,i] = -0.75*np.random.random() - 0.25

    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
        S[abs(S)<1e-10] = 0 # Sets to numerical rounding - simply copying the Raymond method here
    except:
        S = None

    return M, S

def uniformM(Mq):
    '''
    Returns a community matrix (Jacobian) corresponding to the
    qualitative matrix Mq with non-zero elements chosen from a random
    uniform distribution
    '''

    M = np.multiply(np.random.random_sample( Mq.shape ), Mq)
    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
    except:
        S = None

    return M, S

# Test 2
def efficiencyM(Mq, b = 1):
    '''
    Returns a community matrix (Jacobian) corresponding to the
    qualitative matrix Mq with draws from rand unif,
    but with predator responses a_{j,i} drawn from beta distribution
    with mean 0.01 x a_{i,j}
    '''

    # = Create A =
    sz = Mq.shape[0]
    M = np.zeros( (sz,sz) )
    for i in range(sz):

        for j in range(sz):

            if Mq[i,j] != 0:

                if i == j: # With self

                    M[i][i] = -np.random.random()

                else: # With other

                    if Mq[i,j] == -1 and Mq[j,i] == +1:

                            M[i,j] = -np.random.random()

                            # calculate beta distribution parameter a given b for a mean of 0.01 * M[i,j]
                            a = 0.01 * abs(M[i,j]) * b / ( 1 - 0.01 * abs(M[i,j]) )
                            M[j,i] = np.random.beta(a,b)

                    elif Mq[i,j] == +1 and Mq[j,i] == -1:

                            # Only allocate predator-prey on detection of prey
                            pass

                    else:
                            # Anything else, just allocate 

                            M[i,j] = Mq[i,j] * np.random.random()

    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
    except:
        S = None

    return M, S

# Test 3
def difficultStabilityM(Mq, Ef):
    '''
    Returns a community matrix (Jacobian) corresponding to the
    qualitative matrix Mq with non-zero elements chosen from U(0,1), but the diagonal
    elements scaled by f ~ Beta(1, b). The purpose of this is to make it more difficult to find stable
    matrices, as the stability constraint barely rejects any matrices
    '''

    b = (1-Ef)/Ef

    # find basal
    basal = [ all(row <= 0) for row in Mq ]

    # |a_{ij}| ~ U(0,1)
    M = np.multiply(np.random.random_sample( Mq.shape ), Mq)

    # a_{ii} ~ Beta(1,b) if i a consumer
    for i in range(Mq.shape[0]):

        if basal[i] == False:

            M[i,i] = -np.random.beta(1, b)

    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
    except:
        S = None

    return M, S

# An alternative way of doing Test 3
def difficultStabilityM2(Mq, Ef):
    '''
    Returns a community matrix (Jacobian) corresponding to the
    qualitative matrix Mq with non-zero elements chosen from U(0,1), but the diagonal
    elements scaled by f ~ Beta(a, 1). The purpose of this is to make it more difficult to find stable
    matrices, as the stability constraint barely rejects any matrices
    '''

    a = Ef / (1-Ef)
    #b = (1-Ef)/Ef

    # find basal
    basal = [ all(row <= 0) for row in Mq ]

    # |a_{ij}| ~ U(0,1)
    M = np.multiply(np.random.random_sample( Mq.shape ), Mq)

    # a_{ii} ~ Beta(1,b) if i a consumer
    for i in range(Mq.shape[0]):

        if basal[i] == False:

            M[i,i] = -np.random.beta(a, 1)

    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
    except:
        S = None

    return M, S

# == 1.2: Possible validation constraints on the community matrix ==

def isStableM(M):
    '''
    Returns True if community matrix (the Jacobian) M is stable
    '''

    return max(np.real(np.linalg.eigvals(M))) < 0


# = 2: Specifying the LV elements =

# Utility function to convert a system specified as A,r pair into the Jacobian M
def Ar2M(A,r):

    N = np.linalg.solve(A, -r)
    M = np.dot( np.diag(N), A )
    try:
        S = -np.linalg.inv(M) # calculate its sensitivity matrix
    except:
        S = None
    return M, S

# == 2.1: Methods of drawing LV elements ==

def uniformAr(Mq):
    '''
    Simple LV coefficient allocation, respects only sign of Mq
    Returns A, r
    '''

    sz = Mq.shape[0]

    # = Create r =
    r = 2 * np.random.random_sample(sz) - 1

    # = Create A =
    A = np.multiply(np.random.random_sample( Mq.shape ), Mq)

    return A, r

# == 2.2: Possible validation constraints on the LV ==

def isFeasAr(A,r):
    '''
    Checks if A, r return a feasible system
    '''

    return all( np.linalg.solve( A, -r ) > 0 )

# =================================================================================

# Main

# Get the data needed to define the full food web

f = open('macq1.py') # where the dictionary defining the foodweb we're using is defined
data = imp.load_source('data', '', f)
f.close()

# From macq1.py I now have:
#   data.spp_list: list of the species in order
#   data.pretty_names: key is species and value is the full name for the species
#   data.negative_edges_dict: key is the recipient of the negative edge and the value is a list of donors
#   data.positive_edges_dict: key is the recipient of the positive edge and the value is a list of donors
#   data.validation: key is the species and value is +1 or -1 response to increase in rabbits
#   data.control_spp: species that are controlled

web = initialise_foodweb(data.positive_edges_dict, data.negative_edges_dict) # returns a networkx digraph

# Get: Mq, qualitative community matrix; s2idx: bidictionary mapping species name to index in Mq
(Mq, s2idx) = qualitative_community_matrix(web)

# Create the validation function
validationFunc = lambda S: all( np.sign( S[ s2idx[validation_spp] , s2idx[data.control_spp] ] ) == validation_sign for validation_spp, validation_sign in data.validation.items() )


# Define the experiments. Uncomment the test that you would like to run.

experiments = {
        'Raymond': ( 'sampling M',
            lambda Mq: raymondM(Mq),
            lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Uniform M': ( 'sampling M',
            #lambda Mq: uniformM(Mq),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Uniform LV': ( 'sampling LV',
            #lambda Mq: uniformAr(Mq),
            #lambda A, r: isFeasAr(A,r),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Efficiency M': ('sampling M',
            #lambda Mq: efficiencyM(Mq, 10),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.5': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.5), # equiv to uniform distn
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.45': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.45),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.4': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.4),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.35': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.35),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.3': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.3),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.25': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.25),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.2': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.2),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.15': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.15),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.1': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.1),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M2 Ef = 0.05': ('sampling M',
            #lambda Mq: difficultStabilityM2(Mq, 0.05),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.5': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.5), # equiv to uniform distn
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.45': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.45),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.4': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.4),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.35': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.35),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.3': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.3),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.25': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.25),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.2': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.2),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.15': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.15),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.1': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.1),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        #'Difficult stability M Ef = 0.05': ('sampling M',
            #lambda Mq: difficultStabilityM(Mq, 0.05),
            #lambda M, S: all([ validationFunc(S), isStableM(M) ]) ),
        }


# Count the species responses for each experiment

no_valid_max = 10 # sample size used

# Storage
cntPos = dict()
cntNeg = dict()
cntRejected = dict()

for experiment_name, samplers_validators in experiments.items():

    print('running experiment ' + experiment_name)

    # Ready the storage dictionaries
    cntPos[ experiment_name ] = np.zeros(Mq.shape[0])
    cntNeg[ experiment_name ] = np.zeros(Mq.shape[0])
    cntRejected[ experiment_name ] = 0

    # Extract the samplers and validators for this experiment
    sampling_type = samplers_validators[0]

    if sampling_type == 'sampling LV':

        samplerAr = samplers_validators[1]
        validatorAr = samplers_validators[2]
        validatorM = samplers_validators[3]

    else: # 'sampling M'

        samplerM = samplers_validators[1]
        validatorM = samplers_validators[2]


    # Obtain no_valid_max valid matrices for the experiment
    for no_valid in range(no_valid_max):

        # Reports where it is up to
        print(str(no_valid) + ' of ' + str(no_valid_max))


        # Obtain a valid community matrix, counting the number of rejections as we go

        validM = False

        while not validM:

            if sampling_type == 'sampling M':

                M, S = samplerM(Mq) # sample on community matrix

            else: # 'sampling LV'

                # Must first obtain a valid LV system, and then obtain community matrix

                validAr = False

                while not validAr:

                    A, r = samplerAr(Mq) # sample on LV parameters
                    validAr = validatorAr(A, r) # check if valid LV system

                    if not validAr:

                        cntRejected[ experiment_name ] += 1 # LV didn't pass validation criteria, count as rejected

                    else:

                        M, S = Ar2M(A,r) # LV passed validation, now create community matrix from it to check

            # check if returned an S (i.e. M non-singular)
            if S is None:
                validM = False
            else:
                validM = validatorM(M, S) # check if valid community matrix

            if not validM:

                cntRejected[ experiment_name ] += 1 # community matrix didn't pass validation criteria, count it as rejected

            else:

                # Both LV system (if sampled) and community matrix passed validation.
                # So store information about pos and neg responses of each species to a (positive) perturbation of control species.

                cntPos[ experiment_name ] += S[ :, s2idx[data.control_spp] ] > 0
                cntNeg[ experiment_name ] += S[ :, s2idx[data.control_spp] ] < 0


# Write results to file. 
f = open('test.csv','w')

# write order is S positive spp_name, S negative spp_name, S zero spp_name
ss = [ 'S pos ' + spp_name + ',S neg ' + spp_name + ',S zer ' + spp_name for spp_name in data.spp_list ]
f.write('experiment name,no matrices valid, no rejected matrices,' + ','.join(ss) + '\n') # write header

for experiment_name in experiments:

    f.write( experiment_name + ',' )
    f.write( str(no_valid_max) + ',' )
    f.write( str(cntRejected[ experiment_name ]) + ',' )

    for spp_name in data.spp_list:

        cntPos_ = cntPos[ experiment_name ][ s2idx[spp_name] ]
        cntNeg_ = cntNeg[ experiment_name ][ s2idx[spp_name] ]
        cntZer_ = no_valid_max - cntPos_ - cntNeg_

        f.write( ','.join([ str(cntPos_), str(cntNeg_), str(cntZer_) ]) + ',' )

    f.write( '\n' )

f.close()

