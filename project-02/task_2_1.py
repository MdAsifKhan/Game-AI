import numpy as np
import copy
import math
from tic_tac_toe import print_game_state, move_still_possible, move_was_winning_move, plot_histogram
import pdb


class Tree:
    def __init__(self):
        self.nodes = []
        self.leaf_nodes = []
        self.wins_x = 0
        self.wins_o = 0
        self.branches = 0
        self.leaves_count = 0
        self.draws = 0
        self.upper_bound = math.factorial(9)

    def grow_tree(self, node):
        self.nodes.append(node)

    def statistics(self):
        for node in self.nodes:
            self.branches += len(node.children)
            if not node.children:
                self.leaf_nodes.append(node)
                self.leaves_count += 1
        
        self.branching_factor = self.branches/len(self.nodes)
        self.draws = len(self.leaf_nodes) - (self.wins_x+self.wins_o)
        
        fifth_move = 8*math.factorial(3)*6*5
        sixth_move = fifth_move*4 - 6*math.factorial(3)*2*math.factorial(3)
        seventh_move = 8*3*6*math.factorial(3)*5*4*3 - 6*3*6*math.factorial(3)*math.factorial(3) 
        eight_move = 8*3*6*math.factorial(3)*5*4*3*2 - 6*3*6*math.factorial(3)*2*math.factorial(4) 
        ninth_move = 2*3*8*math.factorial(4)*math.factorial(4) + 6*3*4*math.factorial(4)*math.factorial(4) + 22*1*math.factorial(4)*math.factorial(4)+ 16*math.factorial(5)*math.factorial(4) 
 
        self.upper_bound = fifth_move+sixth_move+seventh_move+eight_move+ninth_move


class Node:
    def __init__(self, S, player):
        self.S = S
        self.player = player
        self.children = []

    def get_children(self, tree):
        if move_still_possible(self.S):
            xs, ys = np.where(self.S==0)
            for x,y in zip(xs, ys):
                next_S = copy.deepcopy(self.S)
                next_S[x,y] = self.player
                child = Node(next_S, self.player *-1)
                tree.grow_tree(child)
                self.children.append(child)

            for child in self.children:
                if move_was_winning_move(child.S, self.player):
                    if child.player == 1:
                        tree.wins_o += 1
                    else:
                        tree.wins_x += 1                    
                else:
                    #Recursively add childrens
                    child.get_children(tree)


if __name__ == '__main__':

    S = np.zeros((3,3))
    player = 1
    node = Node(S, player)
    tree = Tree()
    node.get_children(tree)
    tree.statistics()
    print('Upper Bound on Number of Nodes {}'.format(tree.upper_bound))
    print('Wins of player X {}'.format(tree.wins_x))
    print('Wins of player O {}'.format(tree.wins_o))
    print('Draws {}'.format(tree.draws))
    print('Number of Nodes {}'.format(len(tree.nodes)))
    print('Number of Leaf Nodes {}'.format(tree.leaves_count))
    print('Number of Branches {}'.format(tree.branches))
    print('Branching Factor {}'.format(tree.branching_factor))
    data = np.concatenate((np.ones(tree.wins_x),-np.ones(tree.wins_x),np.zeros(tree.draws)))
    plot = plot_histogram(data,'MinMax Statistics',1)
    plot.show()