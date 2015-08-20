import sys
import numpy as np
import networkx as nx

from qualmod import initialise_foodweb, qualitative_community_matrix, draw_foodweb, get_conditions_lists, get_spp_list, update_s2idx, delta_spp_removal, delta_spp_addition
from web_SRI import positive_edges_dict, negative_edges_dict, abiotic_species_list, livestock_removal_responses, r_signs
from somepars import ambig_edges_list

# Nimrod begin
# Get ID for this nimrod task
ambig_edge_ID = int(sys.argv[1])
# Nimrod end

# = Here I create a kind of null run with no constraints and only the responses to the invasion recorded =

livestock_removal_responses = dict()
r_signs = dict()

record_erad = False # Recording signs of responses
record_eradext = False # Recording if extinction 
record_inv = True
record_tot = False # Record sum of effects
record_totext = False # Record sum of effects if extinction

search_terminator = 0.5
#t_max = 1e8
t_max = 10

# = Create base network

# Create the base network with all edges included
full_web = initialise_foodweb(positive_edges_dict, negative_edges_dict)
full_web.remove_nodes_from(abiotic_species_list) # No abiotic "species"

# Remove ambiguous edges if required
full_web.remove_edges_from(ambig_edges_list[ambig_edge_ID])

# = Create grazing network

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
k = s2idx_graz[rem_spp] # index of species to be removed

# Create new s2idx for our eradication web, and a list of indices for mapping from graz to erad 
s2idx_erad, graz2eradIdxs = update_s2idx(s2idx_graz, [rem_spp])

# = We're interested in the invasion of the scrubjay into the erad web immediately after livestock were removed

# Create row and column for scrub jay for the qualitative community matrix
SJq_col = np.zeros(n_erad)
SJq_row = np.zeros(n_erad)

for neighbor in full_web.neighbors('scrubJay'):

    if full_web.has_edge('scrubJay',neighbor) and neighbor in s2idx_erad:
        SJq_col[ s2idx_erad[neighbor] ] = full_web['scrubJay'][neighbor]['sign']

    if full_web.has_edge(neighbor,'scrubJay') and neighbor in s2idx_erad:
        SJq_row[ s2idx_erad[neighbor] ] = full_web[neighbor]['scrubJay']['sign']

# = We're interested in matching two plausibility criteria 

# (1) Sign conditions on the livestock removal responses
condn_delta_erad_idxs, condn_delta_erad = get_conditions_lists(s2idx_erad, livestock_removal_responses)
# (2) Sign conditions on the r
condn_r_graz_idxs, condn_r_graz = get_conditions_lists(s2idx_graz, r_signs)

# = Open file and write headers

f_name = 'uniques_' + str(ambig_edge_ID) + '.csv'
f = open(f_name,'w')

spp_list = get_spp_list(s2idx_erad) # List of species ordered by index

# Write headers needed
interactions = list()
if record_erad:
    interactions += ['erad_' + spp for spp in spp_list]
if record_eradext:
    interactions += ['eradext_' + spp for spp in spp_list]
if record_inv:
    interactions += ['inv_' + spp for spp in spp_list]
if record_tot:
    interactions += ['tot_' + spp for spp in spp_list]
    if record_totext:
        interactions += ['totext_' + spp for spp in spp_list]
f.write(','.join(interactions) + '\n')

# = Write unique sets of responses to file

collected_responses = set()
t = 0
t_last_updated = 0
while (((t-t_last_updated) < search_terminator*t) | (t < 1000)) & (t < t_max):

    # Find a random stable web that matches the observed delta and r signs

    match_condn_delta = False

    while match_condn_delta == False:

        # Create random stable graz web TODO: This assumption should be addressed

        max_eigval = 1

        while max_eigval >= 0:

            # Create a community matrix that matches the r conditions

            M_graz = np.multiply( np.random.random_sample( (n_graz, n_graz) ), Mq_graz )

            for i,condn in zip(condn_r_graz_idxs,condn_r_graz):

                while np.sign(-np.sum(M_graz,axis=1)[i]) != condn:

                    M_graz[i,:] = np.multiply( np.random.random_sample( (1, n_graz) ), Mq_graz[i,:] )


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
    delta_inv, throwout = delta_spp_addition( M_graz[graz2eradIdxs,:][:,graz2eradIdxs] , M_new_col )

    # Collect up the responses we need
    response = list()
    if record_erad:
        response += ['pos' if v > 0 else 'neg' if v < 0 else 'zer' for v in delta_erad]
    if record_eradext:
        response += ['ext' if v < -1 else 'suv' for v in delta_erad]
    if record_inv:
        response += ['pos' if v > 0 else 'neg' if v < 0 else 'zer' for v in delta_inv]
    if record_tot:
        delta_tot = [ de+di for de,di in zip(delta_erad,delta_inv) ]
        response += ['pos' if v > 0 else 'neg' if v < 0 else 'zer' for v in delta_tot]
        if record_totext:
            response += ['ext' if v < -1 else 'suv' for v in delta_tot]
    response = tuple(response)

    if not(response in collected_responses):
        collected_responses.add(response)
        f.write(','.join(response) + '\n')
        t_last_updated = t

    t += 1

# Print info about run
f_info_name = 'info_' + str(ambig_edge_ID) + '.txt'
f_info = open(f_info_name,'w')
f_info.write('Ran for t = ' + str(t) + ' random webs\n')
f_info.write('Last new response found at t = ' + str(t_last_updated) + ' \n')
f_info.close()


f.close()
