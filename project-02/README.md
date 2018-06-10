# Game-AI Project-02

## Task 2.5 Path Planning

### Graph Reading

1. Read the graph into a 2D array.
2. Create a general 2d Grid graph using networkx.
3. Create a representation of nodes using a 2D array where:  
      a. Rows increase from left to right.  
      b. Columns increase from bottom to top.
4. Iterate the graph removing the nodes with values “1”.

### Functions

***read_file(path)***  
Reads the graph from the file into a 2D array.

***create_graph(matrix)***  
Creates the graph using networkx and 2D array created from the file.

***dist(point1, point2)***  
Calculates the euclidean distance between two nodes in a graph.

***color_map(graph, path, point1, point2)***  
Returns a color map for the graph.

### Path Output
#### Points ***(0, 10)*** and ***(15, 1)***.  
File: ***simpleMap-1-20x20.txt***.

***Dijkstra***  
(0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1)

***A star***  
(0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (6, 9), (7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (14, 1), (15, 1)

#### Points ***(1, 20)*** and ***(25, 5)***.  
File: ***simpleMap-4-22x34.txt***.

***Dijkstra***  
(1, 20), (1, 19), (1, 18), (1, 17), (1, 16), (1, 15), (2, 15), (3, 15), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6), (20, 6), (21, 6), (22, 6), (23, 6), (24, 6), (25, 6), (25, 5)

***A star***  
(1, 20), (1, 19), (1, 18), (1, 17), (1, 16), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (19, 14), (19, 13), (19, 12), (19, 11), (20, 11), (21, 11), (21, 10), (21, 9), (22, 9), (23, 9), (23, 8), (23, 7), (23, 6), (24, 6), (25, 6), (25, 5)

