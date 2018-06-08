#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 20:10:44 2018

@author: boris
"""
import itertools
import numpy as np

def move_was_winning_move(gameState):
        S = gameState
        c = 0
        
        # Checks for 4 consecutive pieces in horizontal rows
        for i in range(S.shape[0]):
            s = [sum(1 for _ in group) for key, group in itertools.groupby(S[i,:]) if key]
            if(len(s) > 0):
                c = np.max(s)
            else:
                c = 0
                
            if(c >= 4):
                #print("Horizontal")
                return True
        
        # Checks for 4 consecutive pieces in vertical rows
        for i in range(S.shape[1]):
            s = [sum(1 for _ in group) for key, group in itertools.groupby(S[:,i]) if key]
            if(len(s) > 0):
                c = np.max(s)
            else:
                c = 0
                
            if(c >= 4):
                #print("Vertical")
                return True
        
        # Checks for 4 consecutive pieces in diagonals with length more than 4 
        diags = [S[::-1,:].diagonal(i) for i in range(-S.shape[0]+1,S.shape[1])]
        diags.extend(S.diagonal(i) for i in range(S.shape[1]-1,-S.shape[0],-1))
        
        for n in diags:
            if(len(n) > 3):
                s = [sum(1 for _ in group) for key, group in itertools.groupby(n) if key]
                if(len(s) > 0):
                    c = np.max(s)
                else:
                    c = 0
                    
                if(c >= 4):
                    #print("Diagonal")
                    return True
             
        return False
    
def move_still_possible(gameState):
        S = gameState
        return not (S[S==0].size == 0)
    
def game_over(gameState):
    r = move_was_winning_move(gameState) or not move_still_possible(gameState)  
    return r
    
def print_game_state(gameState, symbols={1:'R', -1:'Y', 0:' '}):
    B = np.copy(gameState).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print(B)

def possible_moves(gameState):
        '''
        Looks for all columns which are not filled yet.
        Returns a list of 2-tuples where the first element indicates the 
        (row, column) coordinates in the gameState array, where a chip can
        still be placed.
        '''
        occupied = gameState.copy()
        occupied[occupied!=0] = 1
        col_fill = sum(occupied)
        possible = [(col_fill[i], i) for i in range(occupied.shape[1]) if col_fill[i] < occupied.shape[0]]
        return possible
        
def test1337possible_moves():
    gameState_list = [[0, -1, 1, -1, -1, 1, -1], [0, 1, 1, 0, 1, -1, 0], [0, -1, -1, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    gameState = np.array(gameState_list)
    print(possible_moves(gameSt))