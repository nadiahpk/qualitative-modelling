
from qualmod import initialise_foodweb, draw_foodweb
import imp # for importing from a python file


# Get the data needed to define the full food web

f = open('macq1.py') # where the dictionary defining the foodweb we're using is defined
data = imp.load_source('data', '', f)
f.close()

# From macq1.py I have:
#   data.negative_edges_dict: key is the recipient of the negative edge and the value is a list of donors
#   data.positive_edges_dict: key is the recipient of the positive edge and the value is a list of donors

web = initialise_foodweb(data.positive_edges_dict, data.negative_edges_dict) # returns a networkx digraph
draw_foodweb(web, f_name = 'macq1.dot') # to create figure using graphviz: fdp -Tpdf macq1.dot > macq1.pdf
