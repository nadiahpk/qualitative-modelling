spp_list = ['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants', 'livestock', 'gopherSnake', 'willow', 'raptorSmall', 'fox', 'precipitation', 'openCupNestingPasserines', 'treesBig', 'scrubJay', 'westNileVirus', 'mosquito', 'woodpecker', 'shrike', 'raven', 'rats', 'scrubOak', 'mouse', 'goldenEagle']

# Interaction matrix from Scott Morrison email "Matrix" to nadiah.org on 09/09/15
# Original excel file in ~/work/scrubjay/corresp/matrices/SRI_interaction_matrix_Sep09.xlsx

# key is recipient of positive effect
positive_edges_dict = {
'willow': ['fogMoisture', 'precipitation'],
'manzanita': ['fox', 'fogMoisture', 'precipitation'],
'scrubOak': ['scrubJay', 'fogMoisture', 'precipitation', 'mouse'],
'treesBig': ['manzanita', 'scrubOak', 'mouse', 'scrubJay', 'fogMoisture', 'precipitation'],
'understoryPlants': ['manzanita', 'scrubOak', 'treesBig', 'fogMoisture', 'precipitation'],
'fox': ['manzanita', 'treesBig', 'skunk', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'skunk': ['mouse', 'openCupNestingPasserines', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'mouse': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'openCupNestingPasserines'],
'openCupNestingPasserines': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'raptorSmall': ['treesBig', 'fox', 'skunk', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'woodpecker', 'rats', 'scrubJay'],
'raven': ['treesBig', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'livestock', 'rats', 'scrubJay'],
'goldenEagle': ['fox', 'skunk', 'mouse', 'raptorSmall', 'livestock', 'rats', 'gopherSnake'],
'baldEagle': ['fox', 'skunk', 'raptorSmall', 'gopherSnake', 'livestock'],
'gopherSnake': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'openCupNestingPasserines', 'woodpecker', 'rats', 'scrubJay'],
'mosquito': ['fogMoisture', 'precipitation', 'willow', 'manzanita', 'scrubOak', 'treesBig'],
'woodpecker': ['scrubOak', 'treesBig'],
'shrike': ['mouse', 'openCupNestingPasserines'],
'livestock': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'rats': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'openCupNestingPasserines', 'shrike', 'scrubJay'],
'scrubJay': ['scrubOak', 'treesBig', 'mouse', 'openCupNestingPasserines'],
'westNileVirus': ['openCupNestingPasserines', 'raptorSmall', 'raven', 'goldenEagle', 'baldEagle', 'mosquito', 'woodpecker', 'shrike', 'scrubJay'],
'fogMoisture': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
}

negative_edges_dict = {
'willow': ['willow', 'livestock'],
'manzanita': ['manzanita', 'scrubOak', 'treesBig', 'livestock', 'rats'],
'scrubOak': ['manzanita', 'scrubOak', 'treesBig', 'woodpecker', 'livestock', 'rats'],
'treesBig': ['treesBig', 'livestock', 'rats'],
'understoryPlants': ['willow', 'understoryPlants', 'livestock'],
'fox': ['fox', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'skunk': ['fox', 'skunk', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'mouse': ['fox', 'skunk', 'mouse', 'raptorSmall', 'raven', 'gopherSnake', 'shrike', 'rats', 'scrubJay'],
'openCupNestingPasserines': ['fox', 'skunk', 'mouse', 'openCupNestingPasserines', 'raptorSmall', 'raven', 'gopherSnake', 'shrike', 'rats', 'scrubJay', 'westNileVirus'],
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
}

uncertain_positive_edges_dict = {
'scrubOak': ['mouse'],
'skunk': ['shrike', 'scrubJay'],
'baldEagle': ['gopherSnake', 'livestock'],
'mosquito': ['willow', 'manzanita', 'scrubOak', 'treesBig'],
'shrike': ['openCupNestingPasserines'],
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

# species not currently represented on santa rosa
absent_species_list = ['livestock', 'scrubJay', 'westNileVirus', 'rats']

# Constraints from Scott Morrison email 22 October 2015 to uq (fwd to nadiah.org) on 22 October (26 October), find in ~/work/scrubjay/corresp/constraints/ConstraintsMatrix_v1_Oct15.pdf

# Results of livestock removal
livestock_removal_responses = {
    'manzanita' : +1,
    'baldEagle': +1,
    'skunk': +1,
    'understoryPlants' : +1,
    'gopherSnake' : +1,
    'willow' : +1,
    'raptorSmall': +1,
    'fox': +1,
    'openCupPasserines': +1,
    'treesBig': +1,
    'scrubJay': +1,
    'mosquito': +1,
    'raven': -1,
    'rats': +1,
    'scrubOak' : +1,
    'mouse' : +1,
    'shrike' : -1,
    'goldenEagle' : -1,
}
livestock_removal_responses_uncertain = [ 'baldEagle', 'skunk', 'gopherSnake' , 'mosquito', 'rats', 'shrike' ]
livestock_removal_possible_extinctions = ['shrike', 'goldenEagle']

# r constraints here (the growth rate in the absence of all of the species modelled, could survive --> +1)
r_signs = {
    'manzanita': +1,
    'baldEagle': +1,
    'skunk': -1,
    'understoryPlants': +1,
    'livestock': +1,
    'gopherSnake': +1,
    'willow': +1,
    'raptorSmall': -1,
    'fox': -1,
    'openCupNestingPasserines': -1,
    'treesBig': +1,
    'scrubJay': -1,
    'westNileVirus': -1,
    'mosquito': +1,
    'raven': +1,
    'rats': +1,
    'scrubOak': +1,
    'mouse': +1,
    'shrike': +1,
    'goldenEagle': -1,
}
r_signs_uncertain = ['understoryPlants', 'gopherSnake', 'raptorSmall', 'openCupNestingPasserines', 'scrubJay', 'mosquito', 'raven', 'shrike', 'goldenEagle']
