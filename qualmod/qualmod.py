import networkx as nx
import numpy as np
from bidict import bidict

def initialise_foodweb(positive_edges_dict, negative_edges_dict):

    """
    Accepts a dictionary of positive edges and a dictionary of 
    negative edges. Dictionaries are set up so that the recipient
    of the interaction is the key and the species with a positive
    or negative interaction with that recipient appear in the value
    list. It returns a networkx digraph with positive edges 
    having a 'color' green and 'sign' of +1, and negative edges
    having a 'color' red and 'sign' -1. The colour labels make 
    export to graphviz convenient.
    
    # species 1 eats species 2 and species 2 is self-limiting 
    >>> G = initialise_foodweb({'species 1':['species 2']}, {'species 2':['species 1','species 2']})
    >>> sorted(G.nodes())
    ['species 1', 'species 2']
    >>> sorted(G.edges())
    [('species 1', 'species 2'), ('species 2', 'species 1'), ('species 2', 'species 2')]

    >>> G.edge['species 1'].keys()
    dict_keys(['species 2'])
    >>> G.edge['species 1']['species 2']['color']
    'red'
    >>> G.edge['species 1']['species 2']['sign']
    -1
    """

    # Make list of tuples of negative edges
    negative_edges_list = [(giver, recipient) for recipient, giver_list in negative_edges_dict.items() for giver in giver_list]
    positive_edges_list = [(giver, recipient) for recipient, giver_list in positive_edges_dict.items() for giver in giver_list]

    # Create networkx digraph to represent food web
    G = nx.DiGraph()
    G.add_edges_from(negative_edges_list, color='red', sign=-1)
    G.add_edges_from(positive_edges_list, color='green', sign=1)



    return G

def qualitative_community_matrix(G, spp_to_idx=None):

    """
    Takes a digraph of the food web, returns the
    qualitative community matrix, with positive and
    negative interactions marked by positive and negative
    1. Denoted by an A with an empty circle in Dambacher
    et al. (2002). Optionally returns a bi-dictionary
    mapping species labels to indices of matrix.
 
    >>> G = initialise_foodweb({'species 1':['species 2']}, {'species 2':['species 1','species 2']})
    >>> (Mq, spp_to_idx) = qualitative_community_matrix(G)

    # Mq will look something like this: Mq = array([[-1., -1.], [ 1.,  0.]])

    >>> Mq[spp_to_idx['species 1'],spp_to_idx['species 1']]
    0.0

    >>> Mq[spp_to_idx['species 1'],spp_to_idx['species 2']]
    1.0

    >>> Mq[spp_to_idx['species 2'],spp_to_idx['species 1']]
    -1.0

    >>> Mq[spp_to_idx['species 2'],spp_to_idx['species 2']]
    -1.0

    # spp_to_idx will look something like this: bidict({'species 2': 0, 'species 1': 1})

    >>> sorted(spp_to_idx.keys())
    ['species 1', 'species 2']

    >>> sorted(spp_to_idx.values())
    [0, 1]
    """

    # Number of nodes, or species
    order = G.order()

    # A mapping from the species names to an index in the community matrix
    if spp_to_idx is None:
        spp_to_idx = bidict( zip(G.nodes(), range(order)) )

    # Construction of the qualitative community matrix
    Mq = np.zeros(shape=(order,order))
    for (giver, recipient, data) in G.edges_iter(data=True):
        row = spp_to_idx.get(recipient)
        col = spp_to_idx.get(giver)
        Mq[row][col] = data['sign']

    return (Mq, spp_to_idx)

def draw_foodweb(G, f_name = 'web.dot'):
    '''
    Writes a .dot file, for use with graphviz, drawing the
    food web. 

    You can process this file with fdp -Teps web.dot > web.eps
    '''
    # TODO: Allow it to process ambiguous edges

    f = open(f_name,'w');
    f.write('digraph {\n')
    f.write('edge [dir=both];\n')

    GG = G.to_undirected()


    for (u, v) in GG.edges_iter():

        # Aiming for this kind of thing
        # e.g. manzanita -> manzanita   [color=red, weight=-1];

        # Positive single and double-directions
        wstr = None
        if G.has_edge(u,v) == True:

            # print('u: ' + u + ', v:' + v)
            if G[u][v]['sign'] == 1:
                if G.has_edge(v, u):
                    if G.edge[v][u]['sign'] == -1:
                        wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=vee, arrowtail=dot, color=\"#000099\"];\n'
                    else:
                        wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=vee, arrowtail=vee, color=\"#006600\"];\n'
                else:
                    wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=vee, arrowtail=none, color=\"#40e0d0\"];\n'

            # Single-direction negatives
            if G[u][v]['sign'] == -1:
                if u != v:
                    if G.has_edge(v,u):
                        if G.edge[v][u]['sign'] == -1:
                            wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=dot, arrowtail=dot, color=red];\n'
                        else:
                            wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=dot, arrowtail=vee, color=\"#000099\"];\n'
                    else:
                        wstr = '\"' + u + '\" -> ' + '\"' + v + '\" [arrowhead=dot, arrowtail=none, color=\"#990033\"];\n'

        else: # Must be only in the reverse direction

            if G[v][u]['sign'] == 1:
                wstr = '\"' + v + '\" -> ' + '\"' + u + '\" [arrowhead=vee, arrowtail=none, color=\"#40e0d0\"];\n'
            elif G[v][u]['sign'] == -1:
                wstr = '\"' + v + '\" -> ' + '\"' + u + '\" [arrowhead=dot, arrowtail=none, color=\"#990033\"];\n'

        if wstr != None:
            f.write(wstr)

    f.write('}')
    f.close()


def get_conditions_lists(s2idx, conditions_dict):
    '''
    Turn a dictionary of conditions into two lists that correspond to one another.
    The first list returned are indices to match the indices in s2idx.
    the second list returned are the conditions corresponding to those indices.

    >>> spp_list = ['manzanita', 'understoryPlants', 'willow', 'fox', 'scrubOak', 'openCupNestingPasserines', 'treesBig', 'baldEagle', 'raptorSmall', 'raven', 'skunk', 'mouse', 'gopherSnake', 'goldenEagle']
    >>> s2idx = bidict( zip(spp_list, range(len(spp_list))) )
    >>> conditions_dict = { 'manzanita' : +1, 'understoryPlants' : -1, 'willow' : +1, 'treesBig' : +1, 'scrubOak' : +1, 'goldenEagle' : +1 }
    >>> idx_list, conditions_list = get_conditions_lists(s2idx, conditions_dict)
    >>> idx_list
    [0, 1, 2, 4, 6, 13]
    >>> conditions_list
    [1, -1, 1, 1, 1, 1]
    '''

    if conditions_dict:

        conditions_list = [None] * len(s2idx)
        for spp, condition in conditions_dict.items(): # Replace None with a condition if there is one
            if spp in s2idx:
                conditions_list[ s2idx[spp] ] = condition

        # Remove the Nones and get a list of tuples of the indices
        idx_conditions = list(zip(*filter(lambda x: x[1] != None, list(enumerate(conditions_list)))))
        idx_list = list(idx_conditions[0])
        conditions_list = list(idx_conditions[1])

    else:
        
        # Empty conditions_dict return empty lists
        idx_list = list()
        conditions_list = list()

    return idx_list, conditions_list 

def get_spp_list(s2idx):
    '''
    The purpose of this function is to return a list from s2idx ordered by the indices specified in s2idx.

    >>> s2idx = bidict( zip(['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants'],[0,1,3,4,5]) )
    >>> get_spp_list(s2idx)
    ['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants']
    '''

    spp_list = sorted(s2idx, key=s2idx.get)

    return spp_list


def update_s2idx(s2idx, removal_list):
    '''
    The purpose of this function is to update the s2idx
    bidictionary after the removal of some species, and 
    return a list of the indices to keep

    >>> s2idx = bidict( zip(['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants'],range(5)) )
    >>> removal_list = ['skunk','manzanita']
    >>> s2idx_new, keepIdxs = update_s2idx(s2idx,removal_list)
    >>> s2idx_new.inv[0]
    'baldEagle'
    >>> s2idx_new.inv[1]
    'fogMoisture'
    >>> s2idx_new.inv[2]
    'understoryPlants'
    >>> keepIdxs
    [1, 2, 4]

    '''

    n = len(s2idx)

    spp_list = get_spp_list(s2idx)

    spp_list_new = list( filter(lambda x: x not in removal_list, spp_list) )
    keepIdxs = sorted( [s2idx[s] for s in spp_list_new] )
    s2idx_new = bidict( zip(spp_list_new, range(len(spp_list_new))) )

    return s2idx_new, keepIdxs

# Population size changes from species removals and
# additions

def delta_spp_removal(M_orig, ks):
    '''
    The purpose of this function is use a community matrix and a list 
    of species indices to be deleted to return the normalised change 
    in population size at steady state and the new community matrix

    >>> A = np.array([ [-1.00796, -2.48013, -0.17320,  2.29484], [ 6.27482,  0.06681, -0.69141,  0.00000], [-0.40011, -2.65795, -4.58292,  1.19376], [ 0.77790,  0.00000,  0.00000, -0.69673] ])
    >>> r = np.array([-0.401669, -3.931875, 4.107145, 0.020180 ])
    >>> n = np.linalg.solve(A,-r)
    >>> k = 2
    >>> mask = np.ones(4, dtype=bool)
    >>> mask[k] = False
    >>> A_new = A[mask,:][:,mask]
    >>> r_new = r[mask]
    >>> n_new = np.linalg.solve(A_new, -r_new)
    >>> delta_true = np.divide(n_new-n[mask],n[mask])
    >>> M_orig = np.dot(A, np.diag(n))
    >>> delta, M_new = delta_spp_removal(M_orig, k)
    >>> all(abs(delta_true - delta) < 1e-10)
    True
    '''

    # Now we have a stable grazing web, M_grazing.
    # Remove the removal species
    M_new = np.delete(M_orig, ks, axis=0)
    M_new_ks = M_new[:,ks]
    M_new = np.delete(M_new, ks, axis=1)

    # This is the response to the removal
    delta = np.linalg.solve(M_new, M_new_ks)

    # Deal with if there is more than one species to be removed
    if not isinstance(ks,int):
        if len(ks) > 1:
            delta = sum(delta.T)

    return delta, M_new

def delta_spp_addition(M_orig, M_new_col, M_new_row=None):
    '''
    The purpose of this function is add a single new species, defined
    by a column of M of length k and a row of length k+1, to a system defined
    by M_orig, and return the normalised change in population size at steady 
    state and the new community matrix

    >>> A = np.array([ [-1.00796, -2.48013, -0.17320,  2.29484], [ 6.27482,  0.06681, -0.69141,  0.00000], [-0.40011, -2.65795, -4.58292,  1.19376], [ 0.77790,  0.00000,  0.00000, -0.69673] ])
    >>> r = np.array([-0.401669, -3.931875, 4.107145, 0.020180 ])
    >>> n = np.linalg.solve(A,-r)
    >>> M = np.dot(A, np.diag(n))
    >>> k = 4
    >>> mask = np.ones(5, dtype=bool)
    >>> mask[k] = False
    >>> A_new = np.array( [[-1.00796, -2.48013, -0.1732 ,  2.29484, -0.     ], [ 6.27482,  0.06681, -0.69141,  0.     ,  1.2044 ], [-0.40011, -2.65795, -4.58292,  1.19376, -5.07491], [ 0.7779 ,  0.     ,  0.     , -0.69673,  0.37504], [ 0.     , -1.62222,  1.08349, -0.35541, -0.80522]])
    >>> r_new = np.array([-0.401669, -3.931875,  4.107145,  0.02018 ,  1.3921  ])
    >>> n_new = np.linalg.solve(A_new, -r_new)
    >>> delta_true = np.divide(n_new[mask]-n,n)
    >>> M_new_2 = np.dot(A_new, np.diag(n_new))
    >>> M_new_col = M_new_2[mask,k]
    >>> M_new_row = M_new_2[k,:]
    >>> delta, M_new = delta_spp_addition(M, M_new_col, M_new_row)
    >>> all(abs(delta_true - delta) < 1e-10)
    True
    '''

    delta = np.linalg.solve(M_orig, -M_new_col)

    if M_new_row == None:
        M_new = None
    else:
        M_new = np.concatenate( ( np.concatenate( ( np.dot(M_orig, np.diag(delta+1)) , np.array([M_new_col]).T), axis=1 ) , np.array([M_new_row])), axis=0 )

    return delta, M_new
