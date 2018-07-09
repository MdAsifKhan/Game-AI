# Project-03

## Task 3.1 Connect-4
In this task we implement connect four on a large board of 19X19.
Change to folder Connect-4.
```python  connect4GUI.py ```

## Task 3.2 Breakout
In this task we implement a fuzzy controller for the breakout game. Rules fire with certain degree of acceptance. Define membership functions.
* Antecedent: Distance of the ball from the paddle.
* Consequent:  Movement of Paddle.

Change to folder Breakout.
```python  breakout.py	```

## Task 3.3 SelfOrganizingMap (SOM)
Here we implement SOM with circular topology to represent player movements in a game.
task_3.py: Contains implementation of SOM. Consists of following methods
a) weight_init: method to initializa SOM. We support two techniques: random weight and SVD low rank approximation.

b) topological_distance: To calculate length of shortest path with circular topology.

c) winner_neuron: to find the winner neuron

d) plot_data: to visualize data points.

e) save_weights: save weights learned by SOM

f) som: implementation of learning method for SOM.

g) evaluate: evaluate quality of SOM.

```python  task_3.py	```
 
## Task 3.4 Bayesian Imitation Learning
In this task we implement an agent to find the trajectory in the game.
We use bayesian learning and use SOM weights for the user location. We found agent encounters following two problems.
* Shooting up or down from the trajector. We address this problem by restricting agent within maximum and minimum possible range in game engine.
* Difficulty in finding trajectory with multiple loops. We resolve it by using previous action of agent. This is done by using 2nd order markov dependency.  

task_4.py: Contains implementation of bayesian imitation learning for trajectory planning. 
Our implementation consists of following methods.
clustering: Cluster location data into 'l' states using SOM Weights
learning1: Compute joint probability of location and action state using bayesian learning.
learning2: Use conditional probabilites with 2nd order markov dependency to plan trajectory. 

```python  task_4.py	```


## Requirements
* [PyGame](https://www.pygame.org/news)
* [SciKit-Fuzzy](https://pythonhosted.org/scikit-fuzzy/)
* Python3+