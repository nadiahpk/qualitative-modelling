# Method

1. ```macq1.py```: Defines the interaction network used, a Macquarie Island ecosystem
2. ```searchresponses.py```: Sweeps the parameter space looking for unique species response combinations to a press perturbation of rabbits. The results are written to ```uniques_web1_rabbits.csv```. Summary information about the run is also written to ```info_web1.txt```.
3. ```simple_pcu_search.py```: Uses the results in ```uniques_web1_rabbits.csv``` to obtain the PCUs, which are written to ```uniques_web1_rabbits_pcus.py```
4. ```draw_implications.py```: Uses the results in ```uniques_web1_rabbits_pcus.py``` to draw the logical implication network, written to a graphviz file ```uniques_web1_rabbits_pcus.dot```


# Results

1. ```uniques_web1_rabbits_pcus_final_rearrange.pdf```: figures used for manuscript, generated from ```uniques_web1_rabbits_pcus.dot``` and then rearranged for aesthetics.

