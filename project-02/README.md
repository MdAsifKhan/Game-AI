# Project-02

In this project we implement game trees and path planning algorithm.

## Task 2.1 Game-Tree
In this task we grow the complete game tree for Tic-Tac-Toe and do the combinatorial analysis for the upper bound on number of nodes and leaves.
We also computed game statistics to understand winning situations. 
```python  task_2_1.py	```
## Task 2.2 MiniMax
In this task we implemented MiniMax search for simple trees with utility defined for leaf nodes.

```python  task_2_2.py	```

## Task 2.3 Connect-4
In this task we implemented minimax search for connect four. Change to folder Connect4. Some notes on development contained in dev_notes.txt

```python  minimax.py	```

## Task 2.4 Breakout
In this task we implemented mechanics of breakout. Further we implemented a simple controller which uses coordinates of ball to move the paddle.Change to folder Breakout.

```python  breakout.py	```

## Task 2.5 Path Planning
In this task we realize two algorithms namely: A* and Dijkstra's for the problem of path planning on grid graph. We use it for 2D game map.

Game map consists of 0's and 1's, where 0 is location where player can be and 1 represents wall. We convert map to grid graph in simple four steps.

### Graph Reading

1. Read data into a 2d array.
2. Create a 2d grid graph using networkx.
3. Create a mapping  to relabel coordinates  in  the grid graph.
4. Iteratively  remove nodes with  value  “1”.

```python path_planning_Task2_5.py```


## Requirements
* [PyGame](https://www.pygame.org/news)
* Networkx
* Graphviz
* Python3+
