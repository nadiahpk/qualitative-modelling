#import networkx as nx
import numpy as np
from bidict import bidict

from qualmod import qualitative_community_matrix, initialise_foodweb
from web_TWN import positive_edges_dict, negative_edges_dict, unmonitored_spp_list


def searchweb(G, ID, control_list, monitored_spp_list, search_terminator, t_max):

    order = G.order()
    spp_list = G.nodes() # ***

    # Make qualitative community matrix

    # - A mapping from the index of the matrix to the name of the species and back again
    spp_to_idx = bidict(zip(spp_list, range(order)))
    # - Qualitative community matrix (elements are 0, +1, or -1)
    Mq = qualitative_community_matrix(G,spp_to_idx)[0]

    # Writing responses to two files 

    # - One file for which rat control was easy
    fname_easy = 'uniques_easy_' + str(ID) + '.csv'
    f_easy = open(fname_easy,'w')
    #   - Write header
    #     - interactions = ['cat_cat', 'cat_rat', 'cat_tropicBird', 'cat_brownBooby', 'cat_islandThrush', ...]
    interactions = [control_spp + '_' + responding_spp for control_spp in control_list for responding_spp in monitored_spp_list]
    #     - 'cat_cat,cat_rat,cat_tropicBird,cat_brownBooby,cat_islandThrush ...
    f_easy.write(','.join(interactions) + '\n')

    # - One file for which rat control was hard
    fname_hard = 'uniques_hard_' + str(ID) + '.csv'
    f_hard = open(fname_hard,'w')
    f_hard.write(','.join(interactions) + '\n')

    # Also storing responses
    collected_response_easy = set()
    collected_response_hard = set()

    # Keep searching until haven't found a new combination for half the time it has been
    # searching
    t = 0
    t_last_updated = 0
    while (((t-t_last_updated) < search_terminator*t) | (t < 1000)) & (t < t_max):
    # for t in range(2000):

        # Find random community matrix with easy control for cats
        control_easy_cat = False

        while control_easy_cat == False:

            # Find random community matrix that is stable
            max_eigval = 1

            while max_eigval > 0:

                # Assign random uniform values to M
                M = np.multiply(np.random.random_sample((order, order)), Mq)
                # Get eigenvalues
                eig_vals = np.linalg.eigvals(M)
                # Maximum eigenvalue needs to be negative
                max_eigval = max(np.real(eig_vals))

            # Invert matrix, find qualitative sensitivity matrix
            Sq = - np.linalg.inv(M)

            control_easy_cat = (Sq[spp_to_idx['cat'],spp_to_idx['cat']] > 0)

        # Now we have found a random community matrix with easy control for cats

        # Record the response of each of the monitored species to the control
        response = tuple(['neg' if -Sq[spp_to_idx[ms],spp_to_idx[cs]]<0 else 'pos' for cs in control_list for ms in monitored_spp_list])

        # Need to split into cases where rat control was easy or hard
        control_easy_rat = (Sq[spp_to_idx['rat'],spp_to_idx['rat']] > 0)

        if control_easy_rat:

            if not(response in collected_response_easy):

                f_easy.write(','.join(response) + '\n')
                collected_response_easy.add(response)
                t_last_updated = t

        else:

            if not(response in collected_response_hard):

                f_hard.write(','.join(response) + '\n')
                collected_response_hard.add(response)
                t_last_updated = t

        t += 1


    # Print info about run
    fname_info = 'info_' + str(ID) + '.txt'
    f_info = open(fname_info,'w')
    f_info.write('Ran for t = ' + str(t) + ' random webs\n')
    f_info.write('Last new response found at t = ' + str(t_last_updated) + ' \n')
    f_info.close()

    f_easy.close()
    f_hard.close()
