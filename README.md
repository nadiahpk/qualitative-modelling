# Qualitative Modelling

This repository stores code used for three Qualitative Modelling projects (below),
including code used for a Boolean approach.
The main functions can be found in the `qualmod/` directory:
1. `qualmod.py`: A module containing Qualitative Modelling functions 
2. `findpcu.py`: A module containing Boolean analysis functions

## Project 1: Introducing the Boolean approach to Qualitative Modelling

[![DOI](https://zenodo.org/badge/36830558.svg)](https://zenodo.org/badge/latestdoi/36830558)

### About the manuscript

Kristensen, N.P., Chishom, R.A., and McDonald-Madden, E. (2019) Dealing with high uncertainty in qualitative network
models using Boolean analysis, *Methods in Ecology and Evolution*

**Abstract**

1. Models for predicting ecological behaviour typically require large volumes of data for parameterisation, which is a problem because data are scarce.  Qualitative modelling (QM) provides an alternative by exploring the entire range of possible parameter values.  When a parameter value is completely unknown, QM typically invokes the Principle of Indifference (PoI), for example by sampling the parameter from a uniform prior distribution.  However, if PoI is invoked in this probabilistic way, there may be multiple possible methods for defining a parameter space and sampling values from it, and, worryingly, two different but equally defensible methods can lead to different predictions about ecosystem responses.
1. We investigated how probabilistic PoI can give rise to problems in QM, and developed an alternative method based on Boolean PoI that does not suffer the same limitations.  We used a case study that involved predicting the responses of multiple species to the suppression of a pest.  The unknown model parameters were interaction strengths between species.  For the standard probabilistic method, we drew the parameters randomly from uniform (PoI) and other distributions.  For our new Boolean PoI method, we instead simply specified the ranges of ``possible'' parameter values, and developed a Boolean analysis technique to summarise model predictions.
1. As expected, invoking probabilistic QM yielded different predictions (species response probabilities) for different but equally defensible parameterisation and sampling schemes.  Sometimes differences were large enough to impact decision making.  In contrast, our new Boolean PoI approach simply classifies outcomes (species responses) as certain, possible, or impossible.  Encouragingly, some species responses that were not consistently resolved under probabilistic PoI were shown by our method to be in fact governed by simple rules.  Our method can also identify key species whose responses determine whole-system outcomes.
1. Our non-probabilistic representation of uncertainty circumvents the philosophical problems in standard implementations of PoI for QM.  Our Boolean analysis method summarises results in a way that is interpretable and potentially useful to conservation decision makers.  A priority for future research is to increase the efficiency of our Boolean approach to allow it to deal with problems of higher complexity (more interactions).

**Key figures**

![Figure 3](https://raw.githubusercontent.com/nadiahpk/qualitative-modelling/master/scripts/ray_final/selected.png)

Figure 3: Selected results for Macquarie Island from the different Monte Carlo simulation methods. Predictions for some species differed between methods and was sensitive to the strength of the stability constraint.

![Figure 4](https://raw.githubusercontent.com/nadiahpk/qualitative-modelling/master/scripts/macq/res2_final/uniques_web1_rabbits_pcus_final_rearrange.png)

Figure 4: Logical implication network for Macquarie Island from the Boolean approach.
Species whose responses were ambiguous according to the Monte Carlo simulations or differed between sampling methods are governed by simple deterministic rules.

### About the repository

The code specific to this project can be found in the following directories:
1. `tutorials/`: Tutorials (in Jupyter) for the Boolean approach to Qualitative Modelling
1. `res2_final/`: Scripts used to for the Boolean approach on the Macquarie Island case study
1. `ray_final/`: Scripts used to for Monte Carlo simulations on the Macquarie Island case study

## Project 2: Christmas Island rat and cat control 

Investigating the control of cats and rats in the Town interaction network for Christmas Island.
In submission.

The code specific to this project can be found in `scripts/townweb`.

## Project 3: Scrub Jay reintroduction

Investigating the reintroduction of Island Scrub Jay to Santa Rosa Island.
Unpublished.

The code specific to this project can be found in the following directories:
1. `scripts/scrubjay/`: Scripts used.
1. `docs/species_additions.ipynb`: A summary of the mathematical approach.

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
