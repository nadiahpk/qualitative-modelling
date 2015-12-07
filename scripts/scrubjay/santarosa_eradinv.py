import imp
import copy
import sys
import numpy as np
import networkx as nx

from qualmod import initialise_foodweb, qualitative_community_matrix, update_s2idx, get_spp_list, getM, delta_spp_removal, getStableM, unifMRConstr, delta_spp_addition, isStableM

riflag = int(sys.argv[1]) # Just these two extreme variations for now

# = Inputs

if riflag == 0:
    removeAmbiguousEdges = False
else:
    removeAmbiguousEdges = True

fWebName = 'web_SRI.py'
newSppName = 'scrubJay'
remSppName = 'livestock'

# Length of search
search_terminator = 0.5
#t_max = 1e5
#t_min = 1e3
t_max = 3
t_min = 2

# A list of species to remove from the full web to create the post-invasion web
remFromFullWeb = ['precipitation', 'westNileVirus', 'rats']

# Doing parameter sweep by random sampling in M
#drawsFnc = lambda Mq: np.multiply(np.random.random_sample( Mq.shape ), Mq) 
drawsFnc = lambda Mq, s2idx, rConstr: unifMRConstr(Mq, s2idx, rConstr)

# Validation function for eradication response
validnFncSurvivors = lambda delta, s2idx: [delta[s2idx[sppName]] > -1 for sppName in data.livestock_removal_survive_strict]
validnFncResponses = lambda delta, s2idx: [np.sign(delta[s2idx[sppName]]) == sppResp for sppName, sppResp in data.livestock_removal_responses_lax.items()]

# A function to define our r sign constraints. 
getRConstr = lambda s2idx: {sppName: rSign for sppName,rSign in data.r_signs_lax.items() if sppName in s2idx}
#getRConstr = lambda s2idx: dict() # Example of how to turn off all r constraints

# == Which types of responses will we record?

recordErad = True # Recording signs of responses to eradication
recordEradNames = ['baldEagle', 'goldenEagle', 'gopherSnake', 'mouse', 'raptorSmall', 'shrike', 'skunk', 'woodpecker'] # set(s2idxErad.keys()) - set(data.livestock_removal_responses_lax.keys())

recordEradExt = False # Recording if extinction occurred after eradication
recordEradExtNames = ['goldenEagle', 'shrike']

recordTot = False # Recording sign of total response to both eradication and invasion
recordTotNames = ['baldEagle', 'fogMoisture', 'fox', 'goldenEagle', 'gopherSnake', 'manzanita', 'mosquito', 'mouse', 'passerines', 'raptorSmall', 'raven', 'scrubOak', 'shrike', 'skunk', 'treesBig', 'understoryPlants', 'willow', 'woodpecker']

# Note that the functions above require that data be defined before they're called
# = /Inputs


# = Read in the web and other details about the system

f = open(fWebName)
data = imp.load_source('data', '', f)
f.close()
# gives data.negative_edges_dict and
# data.positive_edges_dict

# = Create the web of all the species to be considered

fullWeb = initialise_foodweb(data.positive_edges_dict, data.negative_edges_dict)

if removeAmbiguousEdges:
    ambigEdges = [(giver,recip) for recip, giverList in data.uncertain_positive_edges_dict.items() for giver in giverList] + [(giver,recip) for recip, giverList in data.uncertain_negative_edges_dict.items() for giver in giverList]
    fullWeb.remove_edges_from(ambigEdges)

fullWeb.remove_nodes_from(remFromFullWeb)

# = Create the orig web

origWeb = fullWeb.copy()
origWeb.remove_nodes_from([newSppName])

(MqOrig, s2idxOrig) = qualitative_community_matrix(origWeb)

# Dictionary of r constraints
rConstr = getRConstr(s2idxOrig)

# NOTE: Weaken the stability constraint here to speed up finding stable systems 
for i in range(len(s2idxOrig)):
    MqOrig[i,i] = -2

# = Get all of the indexing stuff we'll need for after the eradication
# Mark as "0" because it is for the initial species eradicated, not for any cascading extinction effects

remSppIdx = s2idxOrig[remSppName]
s2idxErad0, orig2eradIdxs = update_s2idx(s2idxOrig, [remSppName])
sppListErad0 = get_spp_list(s2idxErad0) # List of species ordered by index
nErad0 = len(sppListErad0)

# = Indexing etc. for outcomes of invasion

lenNewqCol = len(s2idxErad0)
newqCol = np.zeros(lenNewqCol)
for s in fullWeb.successors(newSppName):
    if s in s2idxErad0:
        newqCol[ s2idxErad0[s] ] = fullWeb[newSppName][s]['sign']

# = Prepare output file

# == Open file

fOutName = 'uniques_eradinv_' + fWebName.split('.')[0] + str(riflag) + '.csv'
f = open(fOutName,'w')

# == Write preamble

interactions = list()
if recordErad:
    interactions += ['erad_' + spp for spp in recordEradNames]

if recordEradExt:
    interactions += ['eradExt_' + spp for spp in recordEradExtNames]

if recordTot:
    interactions += ['tot_' + spp for spp in recordTotNames]

f.write(','.join(interactions) + '\n')


# = Search the parameter space

responses = set()

#if True: # TODO loop later

t = 0
t_last_updated = 0
#while (((t-t_last_updated) < search_terminator*t) | (t < t_min)) & (t < t_max):
#if True:
while t < 10:

    validRes = False # The response sign validation condition
    validSur = False # The survival validation condition

    while (validRes == False) or (validSur == False):

        # Reset to False, as only changing on finding True

        validRes = False 
        validSur = False 

        # = Draw stable MOrig

        MOrig, cntRej = getStableM(drawsFnc, MqOrig, s2idxOrig, rConstr)

        # == Do eradication and see if all survive

        # This is the response to the removal
        deltaErad0, MErad0 = delta_spp_removal(MOrig, remSppIdx)
        deltaErad = deltaErad0
        MErad = MErad0
        # We keep deltaErad0 as it will be used to find the total effect of both eradication of the grazer and extinction

        if all(validnFncSurvivors(deltaErad, s2idxErad0)):

            extns = deltaErad < -1

            if any(extns) == False and isStableM(MErad):

                validSur = True

                if all(validnFncResponses(deltaErad, s2idxErad0)):

                    # Set the indices dictionary we'll be using later
                    s2idxErad = s2idxErad0
                    validRes = True # EXITs here

            else:

                # = If additional species went extinct, we need to find the consequences of those extinctions

                s2idxErad = s2idxErad0
                extnNames = [remSppName]

                while any(extns) and all(validnFncSurvivors(deltaErad, s2idxErad)):
                    

                    # Remove all species with deltaErad < -1, and recalculate delta to check for any further consequent extinctions

                    extnIdxsErad = np.where(extns)[0] # Returns array of their indices
                    extnNames += [s2idxErad.inv[i] for i in extnIdxsErad]
                    s2idxErad, throwout = update_s2idx(s2idxOrig, extnNames)
                    extnIdxsOrig = [s2idxOrig[sppName] for sppName in extnNames]

                    deltaErad, MErad = delta_spp_removal(MOrig, extnIdxsOrig)

                    extns = deltaErad < -1 # List of species that probably went extinct

                # ~ Now have either run out of further extinctions or lost a species that should have survived

                if all(validnFncSurvivors(deltaErad, s2idxErad)) and isStableM(MErad):

                    validSur = True

                    if all(validnFncResponses(deltaErad, s2idxErad)):

                        validRes = True # EXITs here

    # ~ Now have an MOrig that satisfies our constraints 

    if recordTot:

        # == Find invade post-eradication system 

        # Multiply by 1.5 to improve coverage of space
        newMCol = 1.5 * np.random.random_sample(lenNewqCol) * newqCol
        deltaInv, throwout = delta_spp_addition( MErad0 , newMCol )


    # == Store response

    # TODO: Expand this later when I have a handle on it
    response = list()

    if recordErad:

        for sppName in recordEradNames:
            if sppName not in s2idxErad:
                response.append('neg')
            else:
                if deltaErad[s2idxErad[sppName]] < 0:
                    response.append('neg')
                elif deltaErad[s2idxErad[sppName]] > 0:
                    response.append('pos')
                else:
                    response.append('zer')
    
    if recordEradExt:
        
        for sppName in recordEradExtNames:
            if sppName not in s2idxErad:
                response.append('ext')
            else:
                response.append('suv')

    if recordTot:

        deltaTot = (1+deltaErad0) * (1+deltaInv) - 1
        response += ['pos' if d > 0 else 'neg' if d < 0 else 'zer' for d in deltaTot]

    response = tuple(response)

    if not(response in responses):
        responses.add(response)
        f.write(','.join(response) + '\n')
        f.flush()
        t_last_updated = t

    t += 1


f.close()

# Print info about run
f_info_name = 'info_eradonly_' + fWebName.split('.')[0] + str(riflag) + '.txt'
f_info = open(f_info_name,'w')
f_info.write('Ran for t = ' + str(t) + ' random webs\n')
f_info.write('Last new response found at t = ' + str(t_last_updated) + ' \n')
f_info.close()


