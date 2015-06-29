import numpy as np
import networkx as nx

from qualmod import initialise_foodweb, qualitative_community_matrix, TwoWayDictionary, draw_foodweb, get_conditions_lists, get_spp_list, update_s2idx, delta_spp_removal, delta_spp_addition
from web_SRI import positive_edges_dict, negative_edges_dict, abiotic_species_list, livestock_removal_responses, r_signs

# Create the network
full_web = initialise_foodweb(positive_edges_dict, negative_edges_dict)
full_web.remove_nodes_from(abiotic_species_list) # No abiotic "species"

# Create the network during grazing
# We'll call it "graz"

graz_web = full_web.copy()

if False:
    # draw web, incl. scrubJay
    graz_absent_species_list = ['westNileVirus', 'rats', 'mosquito']
    graz_web.remove_nodes_from(graz_absent_species_list)
    draw_foodweb(graz_web)

# The first three of these are absent, and the mosquito is only of concern from west nile virus
graz_absent_species_list = ['scrubJay', 'westNileVirus', 'rats', 'mosquito']
graz_web.remove_nodes_from(graz_absent_species_list)
n_graz = graz_web.order()


# Qualitative interaction matrix and species to index
(Mq_graz, s2idx_graz) = qualitative_community_matrix(graz_web)

# = We're interested in the outcome after removal of livestock =

rem_spp = 'livestock'

# Preliminaries for that web, which we'll call "erad"
n_erad = n_graz - 1
k = s2idx_graz.d[rem_spp] # index of species to be removed

# Create new s2idx for our eradication web, and a mask for mapping from graz to erad 
s2idx_erad, mask_graz2erad = update_s2idx(s2idx_graz, [rem_spp])

# = We're interested in the invasion of the scrubjay into the erad web immediately after livestock were removed

# Create row and column for scrub jay for the qualitative community matrix
SJq_col = np.zeros(n_erad)
SJq_row = np.zeros(n_erad)

for neighbor in full_web.neighbors('scrubJay'):

    if full_web.has_edge('scrubJay',neighbor) and s2idx_erad.d.has_key(neighbor): 
        SJq_col[ s2idx_erad.d[neighbor] ] = full_web['scrubJay'][neighbor]['sign']

    if full_web.has_edge(neighbor,'scrubJay') and s2idx_erad.d.has_key(neighbor): 
        SJq_row[ s2idx_erad.d[neighbor] ] = full_web[neighbor]['scrubJay']['sign']

# = We're interested in matching two plausibility criteria 

# (1) Sign conditions on the livestock removal responses
condn_delta_erad_idxs, condn_delta_erad = get_conditions_lists(s2idx_erad, livestock_removal_responses)
# (2) Sign conditions on the r
condn_r_graz_idxs, condn_r_graz = get_conditions_lists(s2idx_graz, r_signs)

# = Write unique sets of responses to file

f = open('uniques.csv','w')

# Write header
spp_list = get_spp_list(s2idx_erad)
interactions = ['erad_' + spp for spp in spp_list]
interactions.extend(['inv_' + spp for spp in spp_list])
f.write(','.join(interactions) + '\n')

collected_responses = set()
t = 0
sz = list()
while t < 10: # TODO: short run for now to test
#if True:
    # Find a random stable web that matches the observed delta and r signs

    match_condn_delta = False

    while match_condn_delta == False:

        # Create random stable graz web TODO: This assumption should be addressed

        max_eigval = 1

        while max_eigval >= 0:

            match_condn_r = False

            while match_condn_r == False:

                M_graz = np.multiply( np.random.random_sample( (n_graz, n_graz) ), Mq_graz )
                # match_condn_r = all( np.sign(-np.sum(M_graz,axis=1)[condn_r_graz_idxs]) == condn_r_graz )
                match_condn_r = True # TODO: DEBUGGING

            max_eigval = max( np.real( np.linalg.eigvals( M_graz ) ) )

        # Now we have a stable graz web, M_graz.
        # This is the response to the removal
        delta_erad, M_erad = delta_spp_removal(M_graz, k)

        match_condn_delta = all(np.sign(delta_erad[condn_delta_erad_idxs]) == condn_delta_erad)

    # = TODO: Find a scrub jay that can invade the erad system 

    # The graz community immediately after the removal of livestock
    # M_immed = np.delete( np.delete(M_graz, k, axis=0) , k, axis=1 )

    # r_k = - \sum_j a_{kj} n_j
    #     = - \sum_j m_{kj} 
    # where m is the new community matrix.
    # \gamma_k = r_k + \sum_{i \neq k} a_{ki} x_i 
    # where x is the state at which the invasion took place, and m_{x} is its community matrix
    # But need a way of dealing with x_i

    # = Find the response of the species to the invasion and store result

    M_new_col = np.random.random_sample(n_erad) * SJq_col
    delta_inv, throwout = delta_spp_addition( M_graz[mask_graz2erad,:][:,mask_graz2erad] , M_new_col )

    #delta_erad = np.sign(delta_erad)
    #delta_inv = np.sign(delta_inv)

    response = ['pos' if v > 0 else 'neg' if v < 0 else 'zer' for v in delta_erad]
    response.extend(['pos' if v > 0 else 'neg' if v < 0 else 'zer' for v in delta_inv])
    response = tuple(response)

    if not(response in collected_responses):
        collected_responses.add(response)
        f.write(','.join(response) + '\n')

    sz.append(len(collected_responses))
    t += 1

f.close()
