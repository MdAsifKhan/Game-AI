# Game-AI Project-02

## Task 2.1 Game-Tree
```python  task_2_1.py	```
## Task 2.2 MiniMax
```python  task_2_2.py	```
## Task 2.3 Connect-4
Change to folder Connect4. Some notes on development contained in dev_notes.txt
```python  minimax.py	```

## Task 2.4 Breakout

Change to folder Breakout
```python  breakout.py	```

## Task 2.5 Path Planning
```python path_planning_Task2_5.py```

### Graph Reading

1. Read data into a 2d array.
2. Create a 2d grid graph using networkx.
3. Create a mapping  to relabel coordinates  in  the grid graph.
4. Iteratively  remove nodes with  value  “1”.

### Functions

***read_file(path)***  
Reads the graph from a file into a 2D array.

***create_graph(matrix)***  
Creates the graph using networkx and 2D array created from the file.

***dist(point1, point2)***  
Calculates the euclidean distance between two nodes in a graph.

***color_map(graph, path, point1, point2)***  
Returns a color map for the graph.
