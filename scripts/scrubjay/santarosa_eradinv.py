import imp
import sys
import numpy as np
import networkx as nx

from qualmod import initialise_foodweb, qualitative_community_matrix, update_s2idx, get_spp_list, getM, delta_spp_removal, getStableM, unifMRConstr, delta_spp_addition

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
t_max = 1e5
t_min = 1e3
#t_max = 3
#t_min = 2

# A list of species to remove from the full web to create the post-invasion web
remFromFullWeb = ['precipitation', 'westNileVirus', 'rats']

# Doing parameter sweep by random sampling in M
#drawsFnc = lambda Mq: np.multiply(np.random.random_sample( Mq.shape ), Mq) 
drawsFnc = lambda Mq, s2idx, rConstr: unifMRConstr(Mq, s2idx, rConstr)

# Validation function for eradication response
validnFncSurvivors = lambda delta, s2idx: [delta[s2idx[sppName]] > -1 for sppName in data.livestock_removal_survive_lax]
validnFncResponses = lambda delta, s2idx: [np.sign(delta[s2idx[sppName]]) == sppResp for sppName, sppResp in data.livestock_removal_responses_lax.items()]

# A function to define our r sign constraints. 
getRConstr = lambda s2idx: {sppName: rSign for sppName,rSign in data.r_signs_lax.items() if sppName in s2idx}
#getRConstr = lambda s2idx: dict() # Example of how to turn off all r constraints

# == Which types of responses will we record?

recordErad = True # Recording signs of responses to eradication
ml = ['baldEagle', 'goldenEagle', 'gopherSnake', 'mouse', 'raptorSmall', 'shrike', 'skunk', 'woodpecker']
getMonitorErad = lambda sppList: [s for s in sppList if s in ml]

recordEradExt = False # Recording if extinction occurred after eradication

recordInv = False # Recording signs of responses to invasion

recordInvExt = False # Recording if extinction occurred after invasion

recordTot = True # Recording sign of total response to both eradication and invasion


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

# TODO: Just trying to speed the damned thing up
for i in range(len(s2idxOrig)):
    MqOrig[i,i] = -2

# = Get all of the indexing stuff we'll need for after the eradication

remSppIdx = s2idxOrig[remSppName]
s2idxErad, orig2eradIdxs = update_s2idx(s2idxOrig, [remSppName])
sppListErad = get_spp_list(s2idxErad) # List of species ordered by index
nErad = len(sppListErad)

# == Monitoring species lists and indices
monitorErad = getMonitorErad(sppListErad)
monitorEradIdxs = [s2idxErad[s] for s in monitorErad]

# = Indexing etc. for outcomes of invasion

'''
newqRow = np.zeros(nErad)
for p in fullWeb.predecessors(newSppName):
    if p in s2idxErad:
        newqRow[ s2idxErad[p] ] = fullWeb[p][newSppName]['sign']
'''

newqCol = np.zeros(len(s2idxErad))
for s in fullWeb.successors(newSppName):
    if s in s2idxErad:
        newqCol[ s2idxErad[s] ] = fullWeb[newSppName][s]['sign']

# = Prepare output file

# == Open file

fOutName = 'uniques_eradinv_' + fWebName.split('.')[0] + str(riflag) + '.csv'
f = open(fOutName,'w')

# == Write preamble

interactions = list()
if recordErad:
    interactions += ['erad_' + spp for spp in monitorErad]

if recordEradExt:
    interactions += ['eradExt_' + spp for spp in monitorEradExt]

if recordInv:
    interactions += ['inv_' + spp for spp in monitorInv]

if recordInvExt:
    interactions += ['invExt_' + spp for spp in monitorInvExt]

if recordTot:
    interactions += ['tot_' + spp for spp in sppListErad]

f.write(','.join(interactions) + '\n')


# = Search the parameter space

responses = set()

#if True: # TODO loop later

t = 0
t_last_updated = 0
while (((t-t_last_updated) < search_terminator*t) | (t < t_min)) & (t < t_max):

    validRes = False # The response sign validation condition

    while validRes == False:

        validSur = False # The survival validation condition

        cntInvalid = 0
        while validSur == False:

            # = Draw M

            MOrig, cntRej = getStableM(drawsFnc, MqOrig, s2idxOrig, rConstr)

            # == Do eradication and see if all survive

            # This is the response to the removal
            deltaErad, MErad = delta_spp_removal(MOrig, remSppIdx)

            if all(validnFncSurvivors(deltaErad, s2idxErad)):
                validSur = True
            else:
                cntInvalid += 1

        if all(validnFncResponses(deltaErad, s2idxErad)):
            validRes = True

    # == Find invade post-eradication system 

    # Multiply by 1.5 to improve coverage of space
    newMCol = 1.5 * np.random.random_sample(nErad) * newqCol
    deltaInv, throwout = delta_spp_addition( MErad , newMCol )

    # == Store response

    response = list()
    if recordErad:
        response += ['pos' if deltaErad[i] > 0 else 'neg' if deltaErad[i] < 0 else 'zer' for i in monitorEradIdxs]
    if recordEradExt:
        response += ['ext' if d < -1 else 'suv' for d in deltaErad]
    if recordInv:
        response += ['pos' if d > 0 else 'neg' if d < 0 else 'zer' for d in deltaInv]
    if recordInvExt:
        response += ['ext' if d < -1 else 'suv' for d in deltaInv]
    if recordTot:
        deltaTot = (1+deltaErad) * (1+deltaInv) - 1
        response += ['pos' if d > 0 else 'neg' if d < 0 else 'zer' for d in deltaTot]
    response = tuple(response)

    if not(response in responses):
        responses.add(response)
        f.write(','.join(response) + '\n')
        f.flush()
        t_last_updated = t

    t += 1

# = For printing to screen
#clasErad = ['+' if deltaErad[i] > 0 else ('x' if deltaErad[i] < -1 else '-') for i in monitorEradIdxs]
#print(list(zip(clasErad,monitorErad)))

f.close()

# Print info about run
f_info_name = 'info_eradonly_' + fWebName.split('.')[0] + str(riflag) + '.txt'
f_info = open(f_info_name,'w')
f_info.write('Ran for t = ' + str(t) + ' random webs\n')
f_info.write('Last new response found at t = ' + str(t_last_updated) + ' \n')
f_info.close()

f.close()

