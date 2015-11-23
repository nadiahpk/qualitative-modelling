# NOTE: This is the main script that I run in ipython with:
# In [1]: %run searchallwebs.py

import itertools as it
import sys

# NOTE: the web_a1 file name might change, perhaps this
# should be an argument?
from web_TWN import ambig_edges_list, positive_edges_dict, negative_edges_dict, control_list, unmonitored_spp_list

from qualmod import initialise_foodweb
from searchweb import searchweb

# Nimrod begin
# Get ID for this nimrod task

myID = int(sys.argv[1])
#print 'myID: ', myID

# Nimrod end


# NOTE: Input variables, hardcoded here for the moment
search_terminator = 0.5 # *** NOTE: update both these once we're satisfied it's working
#t_max = 1e8 # For full run
t_max = 1e3+100 # For testing

# Get a list of all possible combinations of ambiguous links that could be removed
# NOTE: edge_removals_list produces a list of edges that can be removed
# from the full web to produce all the possible different
# subwebs. The outer loop iterates over this. For example, for web_a1.py and its inputs, it
# looks like this:
# [
#   [],
#   [('rat', 'goshawk')],
#   [[('flyingfox', 'cat'), ('cat', 'flyingfox'), ('flyingfox', 'flyingfox')]],
#   [[('flyingfox', 'cat'), ('cat', 'flyingfox'), ('flyingfox', 'flyingfox')], ('rat', 'goshawk')]
# ]
edge_removals_list = [ list(it.compress(ambig_edges_list,mask)) for mask in it.product([False,True], repeat=len(ambig_edges_list)) ]


# Create the full web, with all possible links. Each possible web will be a copy of this one with some links removed.
full_web = initialise_foodweb(positive_edges_dict, negative_edges_dict) 

# NOTE: This is the main outer loop, and there are no
# dependencies between the outputs it produces
# (embarrasingly parralelisable).
#for edges_removed in edge_removals_list: # Now search for unique outcomes for each possible web
    #ID = edge_removals_list.index(edges_removed)

edges_removed = edge_removals_list[myID]

# Here is the copy of the full web. We create each
# possible web by removing edges and nodes from it.
G = full_web.copy()

edges_removed = list(it.chain.from_iterable(edges_removed)) # Flatten the edge-removal list
G.remove_edges_from(edges_removed) # Remove edges

solitary=[ species for species,d in G.degree_iter() if d==0 ] # Identify solitary species
G.remove_nodes_from(solitary) # Remove solitary species

monitored_spp_list = list(filter(lambda spp: spp not in unmonitored_spp_list, G.nodes()))

# NOTE: This is the function that analyses each possible
# web and produces two output files for each web. I've
# made the search_terminator variable quite small so that it will
# run quickly for you.
searchweb(G, myID, control_list, monitored_spp_list, search_terminator, t_max) # Final number is the "search_terminator", 0.1 is pretty fast, 0.5 is pretty reasonable

