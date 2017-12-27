import imp
import os
import networkx as nx

# NOTE: Have to reverse the signs, as the search was done
# for positive rabbit rather than negative

figureName = 'uniques_web1_rabbits_pcus'
niceNames = {
        'rabbits': 'rabbits',
        'petrels': 'petrels',
        'mice': 'mice',
        'burrowSeabirds': 'burrow-nest seabirds',
        'macroInverts': 'macroinvertebrates',
        'herbfield': 'herbfield',
        'redpolls': 'redpolls',
        'skuas': 'skuas',
        'rats': 'rats',
        'surfaceSeabirds': 'surface-nest seabirds',
        'penguins': 'penguins',
        'prions': 'prions',
        'albatrosses': 'albatrosses',
        'tussock': 'tussock'
        }

f = open('uniques_web1_rabbits_pcus.py')
data = imp.load_source('data', '', f)
f.close()

PCUList = data.PCUList

andCounter = 0
orCounter = 0
edgesList = list()

for PCU in PCUList:

    # make a special type of figure that shows both
    # directions of implications; this works well in this
    # specific example because the outcomes are related in a very
    # simple way
    for p in PCU:

        if len(PCU) == 1:

            ante = 'True'

            # consequents need to be negated
            if p[:3] == 'pos':
                notpp = 'neg' + p[3:]
            else:
                notpp = 'pos' + p[3:]

            consList = [notpp]

        else:

            ante = p # The antecedent is p
            consList = list()

            # list of p to be turned into consequents
            qs = list(filter(lambda x: x != p, PCU))

            # consequents need to be negated
            for q in qs:

                if q[:3] == 'pos':
                    notqq = 'neg' + q[3:]
                else:
                    notqq = 'pos' + q[3:]

                consList.append(notqq)

        # Now create the edges list

        if len(consList) == 1:

            # The antecedent is linked to that single response
            edgesList.append( (ante, consList[0]) )

        else:

            # The antecedent is linked to the orNode
            orNode = 'or' + str(orCounter)
            edgesList.append( (ante, orNode) )
            orCounter += 1 # increment for next time

            # Each consequent must be linked from the orNode
            for c in consList:
                edgesList.append( (orNode, c) )


G = nx.DiGraph()
G.add_edges_from(edgesList)

# Each node needs a label, a shape, and may need a style

for node, att in G.nodes(data=True):

    if node[:3] == 'pos' or node[:3] == 'neg': # Response node

        if node[:3] == 'neg': # NOTE: sign reverse done here
            respSign = '+'
            att['fillcolor'] = 'white'
        else:
            respSign = "&#8210;"
            att['fillcolor'] = 'gray' # Negative responses are filled

        # The label of responses is a combination of contSpp, respSpp, and respSign
        contSpp, respSpp = node[3:].split('_')
        att['label'] = '< <font point-size="10">&darr; ' + niceNames[contSpp] + '</font><br align="left"/> &nbsp; &nbsp; ' + niceNames[respSpp] + ' ' + respSign + ' >'

        # She wants the rats in boxes and the cats in ovals
        if contSpp == 'cat':
            att['shape'] = 'ellipse'
        else:
            att['shape'] = 'box'


    else: # Boolean operator node

        att['shape'] = 'circle'
        att['fillcolor'] = 'white'

        if node == 'True':
            att['label'] = 'True'
        else:
            if node[:2] == 'or':
                att['label'] = 'or'
            else:
                att['label'] = '"&"'

# Write dot file

fName = figureName
f = open(fName + '.dot','w')


# Preamble
f.write('digraph {\n')
f.write('\n')
f.write('\tnode[style="rounded,filled", width=0, margin=0];\n\n')
f.write('\n')

# Write each node's qualities
for node, att in G.nodes(data=True):

    f.write('\t' + node + ' [')

    for k, v in att.items():
        f.write(k + ' = ' + v + ';')

    f.write('];\n')
f.write('\n')

# Write each edge
for edge in G.edges():

    f.write(edge[0] + '->' + edge[1] + ';\n')
f.write('\n')

# Closing bracket
f.write('}')

f.close()

# Run pdf maker and delete dot file 
os.system('dot -Tpdf ' + fName + '.dot > ' + fName + '.pdf')
# os.system('rm ' + fName + '.dot')
