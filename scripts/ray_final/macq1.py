# order chosen to match figure in paper
spp_list = [
    'albatrosses',
    'prions',
    'burrowSeabirds',   # 3
    'petrels',
    'grassland',        # 5
    'herbfield',
    'macroInverts',
    'mice',             # 8
    'penguins',
    'rabbits',          # 10
    'rats',
    'redpolls',
    'skuas',            # 13
    'surfaceSeabirds',
    'tussock',
]

# pretty names
pretty_names = {
        'albatrosses':      'Albatrosses',
        'prions':           'Antarctic prions',
        'burrowSeabirds':   'Burrow-nesting seabirds',
        'petrels':          'Giant pretrels',
        'grassland':        'Grassland',
        'herbfield':        'Herbfield',
        'macroInverts':     'Macroinvertebrates',
        'mice':             'Mice',
        'penguins':         'Penguins',
        'rabbits':          'Rabbits',
        'rats':             'Rats',
        'redpolls':         'Redpolls starlings',
        'skuas':            'Skuas',
        'surfaceSeabirds':  'Small surface-nesting seabirds',
        'tussock':          'Tall tussock vegetation',
}

# key is recipient of positive effect
positive_edges_dict = {
    'prions':           ['grassland'],
    'skuas':            ['prions','burrowSeabirds','rabbits','penguins'],
    'petrels':          ['penguins','tussock','grassland'],
    'mice':             ['herbfield','macroInverts','tussock'],
    'rats':             ['macroInverts','herbfield','tussock'],
    'burrowSeabirds':   ['tussock'],
    'rabbits':          ['tussock','herbfield','grassland'],
    'macroInverts':     ['herbfield','grassland','tussock'],
    'albatrosses':      ['tussock','herbfield'],
    'redpolls':         ['macroInverts','tussock','herbfield','grassland'],
}

negative_edges_dict = {
    'prions':           ['prions','skuas'],
    'skuas':            ['skuas','tussock'],
    'penguins':         ['penguins','skuas','petrels'],
    'petrels':          ['petrels'],
    'mice':             ['mice','rats'],
    'rats':             ['rats'],
    'burrowSeabirds':   ['burrowSeabirds','skuas','rabbits'],
    'rabbits':          ['rabbits','skuas'],
    'surfaceSeabirds':  ['surfaceSeabirds','rats'],
    'macroInverts':     ['macroInverts','rats','mice','redpolls'],
    'tussock':          ['tussock','mice','rats','rabbits'],
    'albatrosses':      ['albatrosses'],
    'herbfield':        ['herbfield','rabbits'],
    'grassland':        ['grassland'],
    'redpolls':         ['redpolls'],
}

# Reponse to increase in rabbits
validation = {
    'rabbits': +1,
    'tussock': -1,
}

control_spp = 'rabbits'
