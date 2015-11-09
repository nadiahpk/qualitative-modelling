# key is recipient of positive effect
positive_edges_dict = {
'willow': ['fogMoisture', 'precipitation'],
'manzanita': ['fox', 'fogMoisture', 'precipitation'],
'scrubOak': ['scrubJay', 'fogMoisture', 'precipitation', 'mouse'],
'treesBig': ['manzanita', 'scrubOak', 'mouse', 'scrubJay', 'fogMoisture', 'precipitation'],
'understoryPlants': ['manzanita', 'scrubOak', 'treesBig', 'fogMoisture', 'precipitation'],
'fox': ['manzanita', 'skunk', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'rats', 'scrubJay', 'treesBig'],
'skunk': ['mouse', 'openCupNestingPasserines', 'gopherSnake', 'rats', 'scrubJay'],
'mouse': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'openCupNestingPasserines'],
'openCupNestingPasserines': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'raptorSmall': ['treesBig', 'fox', 'skunk', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'rats', 'scrubJay'],
'raven': ['treesBig', 'mouse', 'openCupNestingPasserines', 'gopherSnake', 'livestock', 'rats', 'scrubJay'],
'goldenEagle': ['fox', 'skunk', 'mouse', 'raptorSmall', 'livestock', 'rats', 'gopherSnake'],
'baldEagle': ['fox', 'skunk', 'raptorSmall', 'gopherSnake', 'livestock'],
'gopherSnake': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'openCupNestingPasserines', 'scrubJay'],
'mosquito': ['fogMoisture', 'precipitation', 'willow', 'manzanita', 'scrubOak', 'treesBig'],
'livestock': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
'rats': ['manzanita', 'scrubOak', 'treesBig', 'understoryPlants', 'mouse', 'openCupNestingPasserines', 'scrubJay'],
'scrubJay': ['scrubOak', 'treesBig', 'mouse', 'openCupNestingPasserines'],
'westNileVirus': ['openCupNestingPasserines', 'raptorSmall', 'raven', 'goldenEagle', 'baldEagle', 'mosquito', 'scrubJay'],
'fogMoisture': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'understoryPlants'],
}

negative_edges_dict = {
'willow': ['willow', 'livestock'],
'manzanita': ['manzanita', 'scrubOak', 'livestock', 'treesBig', 'rats'],
'scrubOak': ['manzanita', 'scrubOak', 'treesBig', 'livestock', 'rats'],
'treesBig': ['treesBig', 'livestock', 'rats'],
'understoryPlants': ['willow', 'understoryPlants', 'livestock'],
'fox': ['fox', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'skunk': ['fox', 'skunk', 'raptorSmall', 'goldenEagle', 'baldEagle'],
'mouse': ['fox', 'skunk', 'mouse', 'raptorSmall', 'raven', 'gopherSnake', 'rats', 'scrubJay'],
'openCupNestingPasserines': ['fox', 'skunk', 'mouse', 'openCupNestingPasserines', 'raptorSmall', 'raven', 'gopherSnake', 'rats', 'scrubJay', 'westNileVirus'],
'raptorSmall': ['willow', 'manzanita', 'scrubOak', 'raptorSmall', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'raven': ['raven', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'goldenEagle': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'goldenEagle', 'baldEagle', 'westNileVirus', 'fogMoisture'],
'baldEagle': ['willow', 'manzanita', 'scrubOak', 'treesBig', 'goldenEagle', 'baldEagle', 'westNileVirus'],
'gopherSnake': ['fox', 'skunk', 'raptorSmall', 'raven', 'goldenEagle', 'baldEagle', 'gopherSnake', 'rats'],
'livestock': ['goldenEagle', 'livestock', 'raven', 'baldEagle'],
'rats': ['fox', 'skunk', 'raptorSmall', 'raven', 'goldenEagle', 'gopherSnake', 'rats'],
'scrubJay': ['fox', 'skunk', 'raptorSmall', 'raven', 'gopherSnake', 'rats', 'scrubJay', 'westNileVirus'],
}

uncertain_positive_edges_dict = {
'scrubOak': ['mouse'],
'fox': ['treesBig'],
'skunk': ['scrubJay'],
'goldenEagle': ['gopherSnake'],
'baldEagle': ['gopherSnake', 'livestock'],
'mosquito': ['willow', 'manzanita', 'scrubOak', 'treesBig'],
}

uncertain_negative_edges_dict = {
'manzanita': ['treesBig', 'rats'],
'scrubOak': ['rats'],
'treesBig': ['rats'],
'goldenEagle': ['fogMoisture'],
'livestock': ['raven', 'baldEagle'],
}

# Receiver of interaction is second in tuple
ambig_edges_list = [ 
    ('mouse', 'scrubOak'), ('rats', 'scrubOak'),
    ('treesBig', 'fox'), 
    ('scrubJay', 'skunk'), 
    ('gopherSnake', 'goldenEagle'), ('fogMoisture', 'goldenEagle'),
    ('gopherSnake', 'baldEagle'), ('livestock', 'baldEagle'), 
    ('willow', 'mosquito'), ('manzanita', 'mosquito'), ('scrubOak', 'mosquito'), ('treesBig', 'mosquito'),
    ('treesBig', 'manzanita'), ('rats', 'manzanita'),
    ('rats', 'treesBig'),
    ('raven', 'livestock'), ('baldEagle', 'livestock'),
]


spp_list = ['manzanita', 'baldEagle', 'fogMoisture', 'skunk', 'understoryPlants', 'livestock', 'gopherSnake', 'willow', 'raptorSmall', 'fox', 'precipitation', 'openCupNestingPasserines', 'treesBig', 'scrubJay', 'westNileVirus', 'mosquito', 'raven', 'rats', 'scrubOak', 'mouse', 'goldenEagle']

abiotic_species_list = ['fogMoisture', 'precipitation']

# species not currently represented on santa rosa
absent_species_list = ['livestock', 'scrubJay', 'westNileVirus', 'rats']

# Results of livestock removal
livestock_removal_responses = {
    'manzanita' : +1,
    'understoryPlants' : -1,
    'willow' : +1,
    'treesBig' : +1,
    'scrubOak' : +1,
}

# r constraints here (the growth rate in the absence of all
# of the species modelled)
r_signs = {
    'manzanita': +1,
    'understoryPlants': +1,
    'livestock': -1,
    'willow': +1,
    'openCupNestingPasserines': -1,
    'treesBig': +1,
    'scrubJay': -1,
    'westNileVirus': -1,
    'scrubOak': +1,
}
