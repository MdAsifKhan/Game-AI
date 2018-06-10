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
Reads the graph from a file into a 2D array.

***create_graph(matrix)***  
Creates the graph using networkx and 2D array created from the file.

***dist(point1, point2)***  
Calculates the euclidean distance between two nodes in a graph.

***color_map(graph, path, point1, point2)***  
Returns a color map for the graph.
