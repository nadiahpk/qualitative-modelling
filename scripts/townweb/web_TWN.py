# Labelled according to the .dia file Yi sent my gmail account
# in July 2015

spp_list = [
'cat',
'rat',
'crab',
'goshawk',
'hawkOwl',
'tropicBird',
'flyingFox',
'feralChicken',
'kestrel',
'groundCultivars',
'canopyCultivars',
'diurnalInsectResources',
'nocturnalInsectResources'
]

positive_edges_dict = {
    'cat': ['tropicBird', 'flyingFox', 'diurnalInsectResources', 'feralChicken', 'rat'],
    'rat': ['tropicBird', 'groundCultivars', 'canopyCultivars', 'diurnalInsectResources', 'nocturnalInsectResources', 'feralChicken'],
    'crab': ['groundCultivars'],
    'goshawk': ['rat', 'tropicBird', 'diurnalInsectResources', 'feralChicken'],
    'hawkOwl': ['rat', 'nocturnalInsectResources'],
    'flyingFox': ['canopyCultivars'],
    'feralChicken': ['diurnalInsectResources'],
    'kestrel': ['rat', 'diurnalInsectResources'],
}
negative_edges_dict = {
    'cat': ['cat'],
    'rat': ['rat', 'cat', 'crab', 'goshawk', 'hawkOwl', 'kestrel'],
    'crab': ['crab'],
    'goshawk': ['goshawk'],
    'hawkOwl': ['hawkOwl'],
    'tropicBird': ['tropicBird', 'cat', 'rat', 'goshawk'],
    'flyingFox': ['flyingFox', 'cat'],
    'feralChicken': ['feralChicken', 'cat', 'rat', 'goshawk'],
    'kestrel': ['kestrel'],
    'groundCultivars': ['groundCultivars', 'crab', 'rat'],
    'canopyCultivars': ['canopyCultivars', 'flyingFox', 'rat'],
    'diurnalInsectResources': ['diurnalInsectResources', 'cat', 'rat', 'goshawk', 'feralChicken', 'kestrel'],
    'nocturnalInsectResources': ['nocturnalInsectResources', 'rat', 'hawkOwl'],
}

unmonitored_spp_list = ['crab', 'kestrel', 'groundCultivars', 'canopyCultivars', 'diurnalInsectResources', 'nocturnalInsectResources']

control_list = ['cat','rat']

# Receiver of interaction is second in tuple
ambig_edges_list = [
    ('crab', 'rat'),
    [
        ('rat', 'kestrel'), ('kestrel', 'rat'), # Remove interactions between rat and kestrel
    ],
]

