# Game-AI Project-03

## Task 3.1 Connect-4
```python  filename	```
## Task 3.2 Breakout
Change to folder Breakout
```python  breakout.py	```
## Task 3.3 SelfOrganizingMap (SOM)
task_3.py: COntains mmplementation of SOM. Consists of following methods
a) weight_init: method to initializa SOM. We support two techniques: random weight and SVD low rank approximation.

b) topological_distance: To calculate length of shortest path with circular topology.

c) winner_neuron: to find the winner neuron

d) plot_data: to visualize data points.

e) save_weights: save weights learned by SOM

f) som: implementation of learning method for SOM.

g) evaluate: evaluate quality of SOM.

```python  task_3.py	```

Will generate the visualization of SOM.
 
## Task 3.4 Bayesian Imitation Learning
task_4.py: Contains implementation of bayesian imitation learning for trajectory planning. 
Our implementation consists of following methods.
clustering: Cluster location data into 'l' states using SOM Weights
learning1: COmpute joint probability of location and action state using bayesian learning.
learning2: Use conditional probabilites to plan trajectory. 
```python  task_4.py	```