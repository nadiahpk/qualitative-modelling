import imp
import numpy as np
#import sys
#import networkx as nx

from qualmod import initialise_foodweb, qualitative_community_matrix, get_conditions_lists

# INPUT
webNo = 1
search_terminator = 0.8
t_min = 1e5
t_max = 1e6

fInName = 'macq' + str(webNo) + '.py'
f = open(fInName)
data = imp.load_source('data', '', f)
f.close()
# gives data.negative_edges_dict and data.positive_edges_dict
control_list = data.control_list
validation = data.validation
sppList = data.spp_list

web = initialise_foodweb(data.positive_edges_dict, data.negative_edges_dict)
sz = web.order()

# Qualitative matrix
(Mq, s2idx) = qualitative_community_matrix(web)

# validation condition
condn_idxs, condn = get_conditions_lists(s2idx, validation)

# Initialise output files
fs = {ps: open('uniques_web' + str(webNo) + '_' + ps + '.csv', 'w') for ps in control_list}
for ps in control_list:
    header = [ps + '_' + ms for ms in sppList]
    fs[ps].write(','.join(header) + '\n')

# Initialise collected responses with empty sets
collectedResponses = {spp: set() for spp in sppList} # Key is species perturbed and set will contain tuples of responses

t = 1
t_last_updated = 0
while (((t-t_last_updated) < search_terminator*t) | (t < t_min)) & (t < t_max):
    
    # Find valid stable community matrix
    valid = False

    while not valid:

        # Find a random community matrix that is stable
        maxEig = 1

        while maxEig > 0:
            M = np.multiply(np.random.random_sample((sz,sz)), Mq)
            maxEig = max(np.real(np.linalg.eigvals(M)))

        # Now have a stable matrix

        # Find sensitivity matrix
        Sq = - np.linalg.inv(M)

        # Check validation criteria
        valid = all(np.sign(Sq[condn_idxs,s2idx['rabbits']]) == condn)

    # Now have a valid stable community matrix

    for ps in control_list:

        # NOTE: looking at increase in rabbits not decrease here
        response = tuple('neg' if Sq[s2idx[ms],s2idx[ps]]<0 else 'pos' if Sq[s2idx[ms],s2idx[ps]]>0 else 'zer' for ms in sppList)

        if response not in collectedResponses[ps]:

            fs[ps].write(','.join(response) + '\n')
            collectedResponses[ps].add(response)
            t_last_updated = t

    t += 1

# Print info about run
fname_info = 'info_web' + str(webNo) + '.txt'
f_info = open(fname_info,'w')
f_info.write('Ran for t = ' + str(t) + ' random webs\n')
f_info.write('Last new response found at t = ' + str(t_last_updated) + ' \n')
f_info.close()

# Close output files
for ps in control_list:
    fs[ps].close()

