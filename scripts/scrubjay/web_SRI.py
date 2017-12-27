spp_list = ['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants', 'livestock', 'gopherSnake', 'willow', 'raptorSmall', 'fox', 'precipitation', 'passerines', 'treesBig', 'scrubJay', 'westNileVirus', 'mosquito', 'woodpecker', 'shrike', 'raven', 'rats', 'scrubOak', 'mouse', 'goldenEagle']

# Interaction matrix from Scott Morrison email "Matrix" to nadiah.org on 09/09/15
# Original excel file in ~/work/scrubjay/corresp/matrices/SRI_interaction_matrix_Sep09.xlsx

# key is recipient of positive effect
positive_edges_dict = {
'willow': ['fogMoisture', 'precipitation'],
'manzanita': ['fox', 'fogMoisture', 'precipitation'],
'scrubOak': ['scrubJay', 'fogMoisture', 'precipitation', 'mouse'],
'treesBig': ['manzanita', 'scrubOak', 'mouse', 'scrubJay', 'fogMoisture', 'precipitation'],
'understoryPlants': ['manzanita', 'scrubOak', 'treesBig', 'fogMoisture', 'precipitation'],
'fox': ['manzanita', 'treesBig', 'skunk', 'mouse', 'passerines', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'skunk': ['mouse', 'passerines', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'mouse': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'passerines'],
'passerines': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'raptorSmall': ['treesBig', 'fox', 'skunk', 'mouse', 'passerines', 'gopherSnake', 'woodpecker', 'rats', 'scrubJay'],
'raven': ['treesBig', 'mouse', 'passerines', 'gopherSnake', 'livestock', 'rats', 'scrubJay'],
'goldenEagle': ['fox', 'skunk', 'mouse', 'raptorSmall', 'livestock', 'rats', 'gopherSnake'],
'baldEagle': ['fox', 'skunk', 'raptorSmall', 'gopherSnake', 'livestock'],
'gopherSnake': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'passerines', 'woodpecker', 'rats', 'scrubJay'],
'mosquito': ['fogMoisture', 'precipitation', 'willow', 'manzanita', 'scrubOak', 'treesBig'],
'woodpecker': ['scrubOak', 'treesBig'],
'shrike': ['mouse', 'passerines'],
'livestock': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'rats': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'passerines', 'shrike', 'scrubJay'],
'scrubJay': ['scrubOak', 'treesBig', 'mouse', 'passerines'],
'westNileVirus': ['passerines', 'raptorSmall', 'raven', 'goldenEagle', 'baldEagle', 'mosquito', 'woodpecker', 'shrike', 'scrubJay'],
'fogMoisture': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
}

# I'm imposing self-regulation on all
negative_edges_dict = {
'willow': ['willow', 'livestock'],
'manzanita': ['manzanita', 'scrubOak', 'treesBig', 'livestock', 'rats'],
'scrubOak': ['manzanita', 'scrubOak', 'treesBig', 'woodpecker', 'livestock', 'rats'],
'treesBig': ['treesBig', 'livestock', 'rats'],
'understoryPlants': ['willow', 'understoryPlants', 'livestock'],
'fox': ['fox', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'skunk': ['fox', 'skunk', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'mouse': ['fox', 'skunk', 'mouse', 'raptorSmall', 'raven', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'passerines': ['fox', 'skunk', 'mouse', 'passerines', 'raptorSmall', 'raven', 'gopherSnake', 'shrike', 'rats', 'scrubJay', 'westNileVirus'],
'raptorSmall': ['willow', 'manzanita', 'scrubOak', 'raptorSmall', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'raven': ['raven', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'goldenEagle': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'goldenEagle', 'baldEagle', 'westNileVirus', 'fogMoisture'],
'baldEagle': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'gopherSnake': ['fox', 'skunk', 'raptorSmall', 'raven', 'goldenEagle', 'baldEagle', 'gopherSnake', 'shrike'],
'woodpecker': ['raptorSmall', 'gopherSnake', 'woodpecker', 'rats', 'scrubJay', 'westNileVirus'],
'shrike': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'fox', 'skunk', 'raptorSmall', 'raven', 'gopherSnake', 'shrike', 'rats', 'scrubJay', 'westNileVirus'],
'livestock': ['goldenEagle', 'livestock', 'raven', 'baldEagle'],
'rats': ['fox', 'skunk', 'raptorSmall', 'raven', 'gopherSnake', 'rats'],
'scrubJay': ['fox', 'skunk', 'raptorSmall', 'raven', 'gopherSnake', 'woodpecker', 'shrike', 'rats', 'scrubJay', 'westNileVirus'],
'mosquito': ['mosquito'],
'fogMoisture': ['fogMoisture'],
}

uncertain_positive_edges_dict = {
'scrubOak': ['mouse'],
'skunk': ['shrike', 'scrubJay'],
'baldEagle': ['gopherSnake', 'livestock'],
'mosquito': ['willow', 'manzanita', 'scrubOak', 'treesBig'],
'shrike': ['passerines'],
}

uncertain_negative_edges_dict = {
'manzanita': ['rats'],
'scrubOak': ['rats'],
'treesBig': ['rats'],
'goldenEagle': ['fogMoisture'],
'gopherSnake': ['shrike'],
'woodpecker': ['rats'],
'shrike': ['skunk', 'scrubJay'],
'livestock': ['baldEagle'],
'scrubJay': ['shrike'],
}

# Receiver of interaction is second in tuple
#ambig_edges_list = [ 
    #('mouse', 'scrubOak'), ('rats', 'scrubOak'),
    #('treesBig', 'fox'), 
    #('scrubJay', 'skunk'), 
    #('gopherSnake', 'goldenEagle'), ('fogMoisture', 'goldenEagle'),
    #('gopherSnake', 'baldEagle'), ('livestock', 'baldEagle'), 
    #('willow', 'mosquito'), ('manzanita', 'mosquito'), ('scrubOak', 'mosquito'), ('treesBig', 'mosquito'),
    #('treesBig', 'manzanita'), ('rats', 'manzanita'),
    #('rats', 'treesBig'),
    #('raven', 'livestock'), ('baldEagle', 'livestock'),
#]


abiotic_species_list = ['fogMoisture', 'precipitation']

# Constraints from Scott Morrison email 22 October 2015 to uq (fwd to nadiah.org) on 22 October (26 October), find in ~/work/scrubjay/corresp/constraints/ConstraintsMatrix_v1_Oct15.pdf

# = Response to livestock removal

# Results of livestock removal, generous with uncertainty (see /home/elendil/work/scrubjay/corresp/constraints/summary.ods)
livestock_removal_responses_lax = {
    'manzanita' : +1,
    'understoryPlants' : +1,
    'willow' : +1,
    'fox': +1,
    'passerines': +1,
    'treesBig': +1,
    'raven': -1,
    'scrubOak' : +1,
}

# Results of livestock removal, impose as many constraints
# as we can, including those we know to be true (fog and
# mosquito) from the exploration of the eradicationr
# responses on the lax constraints above
livestock_removal_responses_strict = {
    'manzanita' : +1,
    #'baldEagle': +1,
    'skunk': +1,
    'understoryPlants' : +1,
    'gopherSnake' : +1,
    'willow' : +1,
    'raptorSmall': +1,
    'fox': +1,
    'passerines': +1,
    'treesBig': +1,
    'mosquito': +1,
    'raven': -1,
    'scrubOak' : +1,
    'mouse' : +1,
    'shrike' : -1,
    'goldenEagle' : -1,
    'fogMoisture' : +1,
}

# = Survival after eradication of livestock

# Lax is most generous with uncertainty, and kind of disagreement and don't assume that survives
livestock_removal_survive_lax = [ 'manzanita', 'skunk', 'understoryPlants', 'gopherSnake', 'willow', 'raptorSmall', 'fox', 'passerines', 'treesBig', 'mosquito', 'raven', 'scrubOak']

# Strict uses only those indicated to potentially not survive, so only golden eagle and shrike
livestock_removal_survive_strict = ['baldEagle', 'fogMoisture', 'fox', 'gopherSnake', 'manzanita', 'mosquito', 'mouse', 'passerines', 'raptorSmall', 'raven', 'scrubOak', 'skunk', 'treesBig', 'understoryPlants', 'willow', 'woodpecker']

# = Constraint on r sign (the growth rate in the absence of all of the species modelled, could survive --> +1)
r_signs_lax = {
    'manzanita': +1,
    'baldEagle': +1,
    'willow': +1,
    'westNileVirus': -1,
    'rats': +1,
    'scrubOak': +1,
    'mouse': +1,
}

r_signs_strict = {
    'manzanita': +1,
    'baldEagle': +1,
    'understoryPlants': +1,
    'livestock': +1,
    'willow': +1,
    'raptorSmall': -1,
    'passerines': -1,
    'scrubJay': -1,
    'westNileVirus': -1,
    'mosquito': +1,
    'rats': +1,
    'scrubOak': +1,
    'mouse': +1,
    'shrike': +1,
}

# = Total response

# These response constraints are imposed because the point
# of introducing the scrub jay was to create these
# responses, and because we needed to reduce the number of
# free variables

inv_tot_strict = {
    'treesBig': +1,
    'scrubOak' : +1,
}
