#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 18:07:21 2018

@author: Daniel Biskup
"""
import numpy as np
from gameState import move_still_possible, move_was_winning_move, possible_moves, game_over, print_game_state
from evaluate import evaluate

gameState_list = [[0, -1, 1, -1, -1, 1, -1], [0, 1, 1, 0, 1, -1, 0], [0, -1, -1, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
gameState = np.array(gameState_list)
    
# DFS recursive
# Return 

# TODO: Depth
# TODO: player

def terminal_value(gameState, player_who_caused_this_state, depth=0):
    '''
    player_who_caused_this_state is MAX or MIN represented by 1 and -1 respectively.
    Returns the value of a terminal game state
    
    The values get modified by the depth of the node, to make early winns more
    attractive than late ones. And to make late losses more attractive than 
    early ones.
    '''
    if move_was_winning_move(gameState):
        #Win:
        if player_who_caused_this_state == 1:
            value = 10000 - depth
        #Loss
        else:
            value = -10000 + depth
    #Draw:
    else:
        value = 0
    '''   
    print('-------------------------')
    print(gameState)
    print("Terminal Value: " + str(value))
    '''
    return value                

def possible_next_game_states(gameState, player=1):
    possible = possible_moves(gameState)   
    next_states = []
    for move in possible:
        new_gameState = gameState.copy()
        new_gameState[move] = player
        next_states.append(new_gameState)
    return next_states, possible

def rand_argmin(a):
    'Randomly returns the index of one of multiple minimum numbers in an array'
    ## Test Data:
    '''    
    moves = [(2, 0), (1, 1), (0, 2), (0, 3), (0, 4), (1, 5), (0, 6)]
    rewards = [-5, -6, -4, -2, -3, -2, -6]
    
    moves = [(4, 0), (0, 1), (0, 2), (0, 3), (0, 4), (2, 5), (0, 6)]
    rewards = [-3, -4, -5, -4, -3, -2, -4]
    #Player R moves using MinMax to (4, 0) with reward -3
    a = rewards
    '''
    a = np.array(a) # TODO: This cast is HACKY!
    ix = [i for i in range(len(a)) if a[i] == np.min(a)]
    i = np.random.randint(len(ix))
    return ix[i]
    
def rand_argmax(a):
    'Randomly returns the index of one of multiple minimum numbers in an array'
    a = np.array(a) # TODO: This cast is HACKY!
    ix = [i for i in range(len(a)) if a[i] == np.max(a)]
    i = np.random.randint(len(ix))
    return ix[i]

def rewardEstimate(gameState, player, max_depth=4, depth=0, debug_print=False):
    '''
    This is the recursive function.
    It returns the 'value' of a gameState and the first move to take
    accourding to minmax.
    '''

    # 'player' identify the current player:
    MAX = 1  # 1 is player MAX
    MIN = -1 # -1 is player MIN
        
    if( game_over(gameState) ):
        # It was a terminal state. Pick min or maximum value
        reward = terminal_value(gameState, player_who_caused_this_state=player*(-1), depth=depth)
        move  = None # because from gameState not move need to be taken to get
                     # the reward, since gameState is a terminal state.
    elif depth == max_depth:
        # Use the evaluation function for this state:
        reward = evaluate(gameState, player=1) # We are always interested in
                # estimating the reward for player MAX (i.e. player 1)
        move  = None
    else:  
        # Here we already know, that possible moves do exist, because the game
        # is not over yet.
        # For each possible move find the move yielding the minimum or maximum
        # reward:
        game_states, moves = possible_next_game_states(gameState, player)                          
        
        rewards = []
        for g in game_states:
            r, _ = rewardEstimate(g, player*(-1), max_depth=max_depth, depth= depth+1)
            #  ^ We don't need the returned move here, so we ignore it.
            rewards.append(r)  
        
        #pick min/max reward depending on if it's player MAX or player MINs
        #turn:
        if (depth == 0): # for the last return value, return a random move
                         # out of the minimum (or maximum) moves. This is to
                         # make the A.I. less predictable. I.e. it will not do
                         # the same over and over again in a given situation.
            i = rand_argmax(rewards) if player==MAX else rand_argmin(rewards)
            if debug_print:
                print(moves)
                print(rewards)
        else: # for the others return the first, because it doesn't matter.
            i = np.argmax(rewards) if player==MAX else np.argmin(rewards)
        reward = rewards[i]
        move   = moves[i]
    return reward, move




def calculate_minmax_move(gameState, max_depth=3, player=1):
    '''Note: This function assumes gameState to be NOT terminal'''
    # 'player' (1 or -1) is the player to make the next move.
    # TODO: It should work like this if we pass 'player', but we could infer 'player' from the
    #       gameState.
    # This function should be useable for both player 1 and player -1.
    # Thus we switch encoding:
    # 1  represents player MAX (the one who uses this algorithm)
    # -1 represents player MIN (the opponent of player MIN)
    # We don't really care anymore, if player was 1 or -1 from here on out.
    # We just care if it's MAXs or MINs turn.
    g = gameState.copy()
    g = g * player
    curent_player = 1 # And the first move is always player MAX, because
                      # he's the one calling this function to find out which
                      # move he should take.
    reward, move = rewardEstimate(gameState, curent_player, max_depth=max_depth, depth=0)
    return reward, move

def test1337_calculate_minmax_move():
    gameState_list = \
    [[0  ,-1 ,1  ,-1 ,-1 , 1 ,-1 ], \
    [0  ,1  ,1  ,0  ,1  ,-1 ,0  ], \
    [0  ,-1 ,-1 ,0  ,1  ,1  ,0  ], \
    [0  ,0  ,1  ,0  ,0  ,0  ,0  ], \
    [0  ,0  ,-1 ,0  ,0  ,0  ,0  ], \
    [0  ,0  ,0  ,0  ,0  ,0  ,0  ]]
    gameState = np.array(gameState_list)
    x = calculate_minmax_move(gameState, max_depth=4, player=1)
    print(x)
    
    
    