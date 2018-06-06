#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 17:49:41 2018

@author: Daniel Biskup
"""
import numpy as np
import itertools

def evaluate(gameState, player=1):
    '''
    Returns the difference between the positions that could make "player" win
    and the ones that could make his oponent win.
    gameState: Two dimensional numpy array representing the board. Each entry
               is occupied with 1 or -1 indicationg that it's taken by player
               1 or -1 respectively. Empty fields have the value 0.
    player: The number of the player concidered to be "Player MAX"
    '''
 
    def get_diagonals(M, n=0):
        '''
        Returns a list of all diagonals of matrix M, which go from upper left to
        lower right. Only returns diagonals which have at least n elements.
        '''
        start = -(M.shape[0]-1)
        stop  = M.shape[1]
        
        # Get all diagionals:
        d = [M.diagonal(i) for i in range(start, stop)]
        return [d[i] for i in range(len(d)) if len(d[i]) >= n]
    
    def n_winning(gameState, player = 1):
        '''
        This function returns the number of possible winning positions on the board
        which could still be reached.
        gameState: Two dimensional numpy array representing the board. Each entry
                   is occupied with 1 or -1 indicationg that it's taken by player
                   1 or -1 respectively. Empty fields have the value 0.
        player: the player for for which to evaluate the number of left possible chains of
                four on the board. Can be 1 or -1.
        '''
        g = np.copy(gameState)
        g[g == 0] = player
        M = g==player
                
        # Collect all lines. Vertical, horizontal and diagonals:
        l1 = get_diagonals(M, 4)                 # diagonal lines from up to down
        l2 = get_diagonals(np.fliplr(M), 4)      # diagonal lines from down to up
        l3 = [M[i,:] for i in range(M.shape[0])] # horizontal lines
        l4 = [M[:,i] for i in range(M.shape[1])] # vertical lines
        L = itertools.chain(l1,l2,l3,l4)
        
        # Count the length of the segments in each array which are populated by
        # consecutive "True" values:
        count_list = []
        for l in L:
            last = False
            count = 0
            for x in l:
                if x:
                    count=count + 1
                    last = True
                else:
                    if last and not x: # There was a switch from True to False
                        count_list.append(count)    # add count to list
                        count = 0
                        last = False
            if last:
                count_list.append(count)
                
        # Get rid of the ones which are smaller than 4:
        a = np.array([x for x in count_list if x >= 4])
        
        # From this compute the amount of possible winning positions:
        return (a-4+1).sum()

    opponent = player * -1
    I   = n_winning(gameState, player=player)
    Him = n_winning(gameState, player=opponent)
    return I - Him

#%%
def test1337evaluate():
    gameState_list = [[0, -1, 1, -1, -1, 1, -1], [0, 1, 1, 0, 1, -1, 0], [0, -1, -1, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    gameState = np.array(gameState_list)
    result = evaluate(gameState)
    print(result)