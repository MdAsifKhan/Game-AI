import numpy as np
import pdb
import graphviz as gv

# Class to represent Node in a tree 
class Node:
    def __init__(self, nodeid, player):
        self.id = nodeid
        self.player = player
        self.children = []
        self.score = None
        
    def add_childlren(self, child):
        self.children.append(child)

    def score(self, score):
        self.score = score

# Class to create a tree
class Tree:
    
    def __init__(self, leaf_score):
        self.nodes = []
        self.leaf_score = leaf_score   
    # Method for tree-1 of Task2-2
    def grow_tree_1(self):
        n0 = Node('n0', 1)
        n1 = Node('n1', -1)
        n2 = Node('n2', -1)
        n3 = Node('n3', -1)
        n4 = Node('n4', -1)
        n5 = Node('n5', -1)
        n0.add_childlren(n1)
        n0.add_childlren(n2)
        n0.add_childlren(n3)
        n0.add_childlren(n4)
        n0.add_childlren(n5)
        n6 = Node('n6', 1)
        n7 = Node('n7', 1)
        n8 = Node('n8', 1)
        n9 = Node('n9', 1)
        n1.add_childlren(n6)
        n1.add_childlren(n7)
        n1.add_childlren(n8)
        n1.add_childlren(n9)
        n10 = Node('n10', 1)
        n11 = Node('n11', 1)
        n2.add_childlren(n10)
        n2.add_childlren(n11)
        n12 = Node('n12', 1)
        n13 = Node('n13', 1)
        n3.add_childlren(n12)
        n3.add_childlren(n13)
        n14 = Node('n14', 1)
        n15 = Node('n15', 1)
        n16 = Node('n16', 1)
        n4.add_childlren(n14)
        n4.add_childlren(n15)
        n4.add_childlren(n16)
        n17 = Node('n17', 1)
        n18 = Node('n18', 1)
        n19 = Node('n19', 1)
        n5.add_childlren(n17)
        n5.add_childlren(n18)
        n5.add_childlren(n19)

        self.nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19]

    # Method for tree-2 of Task2-2
    def grow_tree_2(self):
        n0 = Node('n0', 1)
        n1 = Node('n1', -1)
        n2 = Node('n2', -1)
        n3 = Node('n3', -1)
        n4 = Node('n4', -1)
        n0.add_childlren(n1)
        n0.add_childlren(n2)
        n0.add_childlren(n3)
        n0.add_childlren(n4)
        n5 = Node('n5', 1)
        n6 = Node('n6', 1)
        n7 = Node('n7', 1)
        n8 = Node('n8', 1)
        n9 = Node('n9', 1)
        n1.add_childlren(n5)
        n1.add_childlren(n6)
        n1.add_childlren(n7)
        n1.add_childlren(n8)
        n1.add_childlren(n9)
        n10 = Node('n10', 1)
        n11 = Node('n11', 1)
        n2.add_childlren(n10)
        n2.add_childlren(n11)
        n12 = Node('n12', 1)
        n13 = Node('n13', 1)
        n14 = Node('n14', 1)
        n3.add_childlren(n12)
        n3.add_childlren(n13)
        n3.add_childlren(n14)
        n15 = Node('n15', 1)
        n16 = Node('n16', 1)
        n4.add_childlren(n15)
        n4.add_childlren(n16)

        self.nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16]

    def add_leaf_score(self):
        for node in self.nodes:
            if not node.children:
                node.score = self.leaf_score[node.id]
            else:
                node.score = None

# Class to implement MiniMax search on a tree
class MiniMax:
    def __init__(self, tree):
        self.tree = tree  

    # Method to implement minimax search
    def minimax(self, node):
        max_score = self.max_value(node) 
        children = self.get_children(node)
        print('MiniMax: Score of Node {0:} is {1:}'.format(node.id, max_score))
        move = None
        for child in children:   
            if child.score == max_score:
                move = child
                break
        return move

    # Method to find max value
    def max_value(self, node):
        print('MAX Node {}'.format(node.id))
        if self.isleaf(node):
            return self.get_score(node)
        mmv = -np.inf
        for child in self.get_children(node):
            mmv = max(mmv, self.min_value(child))
        node.score = mmv
        return mmv

    # Method to find min value
    def min_value(self, node):
        print('MIN Node {}'.format(node.id))
        if self.isleaf(node):
            return self.get_score(node)
        else:
            mmv = np.inf
            for child in self.get_children(node):
                mmv = min(mmv, self.max_value(child))
        node.score = mmv
        return mmv

    # Method to get children of a node
    def get_children(self, node):
        return node.children

    # Method to check if node is a leaf
    def isleaf(self, node):
        if not node.children:
            return True
        return False

    # Method to find score of a node
    def get_score(self, node):
        return node.score          

    # Method to traverse tree and add nodes and edges to a dot file
    def traverse_tree(self, tree_dot):
        # Root Node
        tree_dot.attr('node', shape='box')
        root = self.tree.nodes[0]
        tree_dot.node(root.id,color='blue', label= root.id+' '+str(root.score))
        # Children Nodes
        for node in self.tree.nodes:
            if node.children:
                for child in node.children:
                    tree_dot.attr('node', shape='box')
                    if child.player == 1:
                        tree_dot.node(child.id,color='blue',label=child.id +' '+str(child.score))
                    else:
                        tree_dot.node(child.id,color='orange',label=child.id +' '+str(child.score))               
                    tree_dot.edge(node.id, child.id)
            else:
                tree_dot.attr('node', shape='box')
                if node.player == 1:
                    tree_dot.node(name = node.id, color='blue',label=node.id +' '+str(node.score))
                else:
                    tree_dot.node(name = node.id, color='orange',label=node.id +' '+str(node.score))

    # Method to save tree as a dot file 
    def plot_tree(self, filename):
        #Save Dot file for tree
        tree_dot = gv.Digraph(format='svg',engine='dot')
        self.traverse_tree(tree_dot)
        f = open(filename,'w+')
        f.write(tree_dot.source)
        f.close() 

if __name__ == '__main__':

    leaf_score_1 = {'n6':15,'n7':20,'n8':1,'n9':3,'n10':3,'n11':4,
                            'n12':15,'n13':10,'n14':16,'n15':4,'n16':12,
                            'n17':15,'n18':12,'n19':8}  
    # Tree 1
    tree = Tree(leaf_score_1)
    tree.grow_tree_1()
    tree.add_leaf_score()
    minmax = MiniMax(tree)
    move = minmax.minimax(tree.nodes[0])
    minmax.plot_tree('tree1.dot')

    # Tree 2
    leaf_score_2 = {'n5':18,'n6':6,'n7':16,'n8':6,'n9':5,'n10':7,
                            'n11':1,'n12':16,'n13':16,'n14':5,'n15':10,
                            'n16':2}  
    tree2 = Tree(leaf_score_2)
    tree2.grow_tree_2()
    tree2.add_leaf_score()
    minmax = MiniMax(tree2)
    move = minmax.minimax(tree2.nodes[0])
    minmax.plot_tree('tree2.dot')