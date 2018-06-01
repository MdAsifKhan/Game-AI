import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Reads the file and creates 2D array.
def read_file(file):

	stack = []
	with open(file, "r") as file_object:
		for line in file_object:
			stack.append(line.split())

	file_object.close()
	return np.array(stack)

# Creates a 2d grid graph using the 2D array.
def create_graph(matrix):
	# Create a 2D grid graph.
	rows, columns = matrix.shape
	g = nx.grid_2d_graph(rows, columns)

	# Create representation of x,y coordinates in graph.
	index_list = np.zeros((rows, columns), dtype=(int,2))
	r, c, t = index_list.shape
	for x, y in np.ndindex((r,c)):
		index_list[x][y] = (y,x)
	index_list = np.flip(index_list, 0)

	# Create mapping to relabel nodes in the graph.
	mapping = dict()
	for x, y in g.nodes():
		xx, yy = index_list[x][y]
		mapping[(x, y)] = (xx, yy)

	g = nx.relabel_nodes(g, mapping)

	# Remove nodes that should not occur in the graph which is equal to "1" in the file.
	indexes = [(x, y) for x, y in np.ndindex((rows, columns))]
	indexes = list(filter(lambda x: matrix[x[0]][x[1]] == "1", indexes))
	nodes_to_remove = list(map(lambda x: mapping[(x[0], x[1])], indexes))
	g.remove_nodes_from(nodes_to_remove)

	return g 

# Calculates the euclidean distance between two nodes in the graph.
def dist(point1, point2):

	 (x1, y1) = point1
	 (x2, y2) = point2

	 return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Produces a color map for the nodes in the graph.
def color_map(graph, path):
	return list(map(lambda n: "yellow" if n in path else ("red" if n == (0, 10) else ("green" if n == (15, 1) else "black")), graph.nodes()))

if __name__== "__main__":

	file = "simpleMap-1-20x20.txt"
	# Second graph file to validate logic
	#file = "simpleMap-4-22x34.txt"

	# Create a matrix.
	matrix = read_file(file)
	rows, columns = matrix.shape

	# Create the graph based on the 2d matrix.
	graph = create_graph(matrix)
	pos = dict(zip(graph, graph))
	path = []
	node_sizes = list(map(lambda n: 50 if n == (0, 10) or n == (15, 1) else 20, graph.nodes()))

	# Points between which path needs to be calculated.
	point1 = (0, 10)
	point2 = (15, 1)

	# Plot graph.
	plt.subplot(221)
	plt.title("Graph")
	nx.draw(graph, pos, node_color = color_map(graph, []), node_size = node_sizes)	

	# Calculate the path between the two points using Dijkstra's algorithm.
	path = nx.dijkstra_path(graph, point1, point2)
	print("Dijkstra Path")
	print(path)

	# Plot Dijkstra's path.
	plt.subplot(222)
	plt.title("Dijkstra Path")
	nx.draw(graph, pos, node_color = color_map(graph, path[1:-1]), with_labels=False, node_size = node_sizes)

	# Calculate the path between the two points using A* algorithm.
	path = nx.astar_path(graph, point1, point2, dist)
	print("A* Path")
	print(path)

	# Plot A* path.
	plt.subplot(223)
	plt.title("A* Path")
	nx.draw(graph, pos, node_color = color_map(graph, path[1:-1]), with_labels=False, node_size = node_sizes)

	# Shows all three graphs.
	plt.show()
