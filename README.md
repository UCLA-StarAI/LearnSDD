# LearnSDD
Tractable learning of probability distributions with Sentential Decision Diagrams

Tractable learning’s goal is to learn probabilistic graphical models where inference is guaranteed to be efficient. However, the particular class of queries that is tractable depends on the model and underlying representation. Usually this class is MPE or conditional probabilities Pr(x|y) for joint assignments x, y. We propose LearnSDD: a tractable learner that guarantees efficient inference for a broader class of queries. It simultaneously learns a Markov network and its tractable circuit representation, in order to guarantee and measure tractability. A key difference with earlier work is that LearnSDD uses Sentential Decision Diagrams (SDDs) as the tractable language instead of Arithmetic Circuits (AC). SDDs have desirable properties that are absent in more general representations such as ACs. Their additional properties enable basic primitives for Boolean circuit compilation, which allows us to support a broader class of complex probability queries, including counting, threshold, and parity, all in polytime.


This is part of the extra material of the following paper:

  Tractable Learning for Complex Probability Queries, Bekker et al., NIPS, 2015

It contains the code for the complex query experiments.

If you use this code or datasets, please cite this paper


## Content ##

 - code: code for executing experiments
 - datasets: datasets used for experiments
 - acs: arithmetic circuits used for experiments
 - sdds: sentential decision diagrams used for experiments
 - lib: contains sdd library
 - out: the output of the example commands is stored here
 
 - experiment_commands.txt: The commands that need to be run for executing the experiments of the paper [Tractable Learning for Complex Probability Queries, Bekker et al., NIPS, 2015]


## Running Experiments ##

experiment_commands.txt contains the exact commands for running the experiments.

Voting experiment:
python code/votingExperiments.py sdd|ac <model_path> <model_name> <outpath> <timeout_in_s> <testdata_path>

Movie experiments:
python code/movieExperiments.py sdd|ac pos|neg|group|parity|conj|wthresh <model_path> <model_name> <outpath> <timeout_in_s> <testdata_path> <evidence_path>
 
 
Before running the experiments:
1. compile sdd query c code
`gcc -std=gnu99 -Wall -o lib/sddQuery sddQueryPackage/sddQuery.c -IsddQueryPackage/include -Llib -lsdd -lm`

2. set necessary path variables
`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:lib/`
`export PATH=$PATH:lib/`


## Third Party Libraries ##

- acquery binary from the Libra Toolkit (http://libra.cs.uoregon.edu/)
- sdd library from the SDD Package (http://reasoning.cs.ucla.edu/sdd/)

Both libraries are included in this packages.

## Bibtex ##

```
@inproceedings{BekkerNIPS15,
  author = "Bekker, Jessa and Davis, Jesse and Choi, Arthur and Darwiche, Adnan and Van den Broeck, Guy",
  title = "Tractable Learning for Complex Probability Queries",
  booktitle = "Advances in Neural Information Processing Systems 28 (NIPS)",
  month = Dec,
  year = "2015",
}
```
