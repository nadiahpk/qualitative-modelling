Project in progress.

# Description

1. ```qualmod.py```: A python module containing QM functions 
2. ```web_SRI.py```: Python data structures defining the Santa Rosa
Island community and the plausibility constraints
3. ```santarosa.py```: A python script for searching the
plausible parameter space for unique species-response combinations to
invasion of the island scrub jay

# Quick Start

In iPython:
    %run santarosa.py

This will produce a file ```uniques.csv``` listing the first
10 unique species response combinations found.

Example contents of ```uniques.csv```:

    erad_manzanita,erad_understoryPlants,erad_willow,erad_fox,erad_scrubOak,erad_openCupNestingPasserines,erad_treesBig,erad_baldEagle,erad_raptorSmall,erad_raven,erad_skunk,erad_mouse,erad_gopherSnake,erad_goldenEagle,inv_manzanita,inv_understoryPlants,inv_willow,inv_fox,inv_scrubOak,inv_openCupNestingPasserines,inv_treesBig,inv_baldEagle,inv_raptorSmall,inv_raven,inv_skunk,inv_mouse,inv_gopherSnake,inv_goldenEagle
    pos,neg,pos,neg,pos,pos,pos,pos,pos,neg,pos,neg,pos,neg,neg,neg,pos,pos,pos,pos,neg,pos,pos,neg,pos,neg,pos,neg
    pos,neg,pos,pos,pos,neg,pos,neg,pos,pos,neg,pos,pos,pos,pos,pos,pos,pos,neg,neg,pos,neg,pos,pos,neg,neg,pos,neg
    ...

The output from ```uniques.csv``` can be used with
the apriori algorithm in ```R``` or the espresso algorithm
from ```pyeda``` to find implication rules for species
responses.
