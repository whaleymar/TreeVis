# TreeVis
A simple tool for visualizing n-ary trees formatted as "Parent(child1(...), child2(...), ...)", with leaves represented by "()"
Created to visualize individuals created by EMADE

### How to use:
- Clone repo
- Download graphviz (free) and add it to your system's path: https://graphviz.org/download/
- Add each individual you want to visualize to its own line in individuals.txt
- run ```python tree_vis.py``` and pngs will be created for each tree

### Sample Input: (on 1st line of individuals.txt)
NNLearner(ARG0, OutputLayer(Conv1DLayer(6, eluActivation, 3, 32, myNot(trueBool), 44, LSTMLayer(16, defaultActivation, 0, ifThenElseBool(falseBool, trueBool, trueBool), trueBool, EmbeddingLayer(97, ARG0, glorotNormalWeights, InputLayer())))), 150, RMSpropOptimizer)
### Output:
![image](https://user-images.githubusercontent.com/63699160/116300912-73bd6d00-a76d-11eb-8103-5a8fb4017750.png)
### The ```else``` block in the ```make_nodes``` function can be altered to change node colors, shapes, etc

### Advanced Usage:
- You can specify a different .txt file of individuals to visualize
- You can specify a .txt file with names for the PNGs created (one name per line, don't include a file extension)
- sample command: ```python tree_vis.py --tree_file_path new_individuals.txt --name_file_path names.txt```
