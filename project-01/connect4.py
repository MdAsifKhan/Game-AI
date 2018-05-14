import numpy as np
import itertools
import matplotlib.pyplot as plt

#  1 --> R (Red)
# -1 --> Y (Yellow)
#  0 --> ' ' (Empty)
symbols = {
     1:'R', 
    -1:'Y', 
     0:' '
}

# To track good moves
penultimate_states = []
winning_moves = []
winning_player = []
#winning_conf = []
wins_losses_draws = []


def move_still_possible(S):
    return not (S[S==0].size == 0)

    
def move_at_random(S, F, p):
    # Looks for all vertical columns where number of pieces
    # is less than 6
    y = np.where(F < 6)
    
    # to select the column for next move out of the above columns 
    j = y[0][np.random.randint(len(y[0]))]
    
    # placing piece on the top of selected column
    i = F[j]
    S[i,j] = p
    
    # Increment the count of pieces of in chosen column
    F[j] += 1
    
    return S,F, (i,j)


def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print(B)


def move_was_winning_move(S, p, print_flag):
    c = 0
    
    # Checks for 4 consecutive pieces in horizontal rows
    for i in range(S.shape[0]):
        s = [sum(1 for _ in group) for key, group in itertools.groupby(S[i,:]) if key]
        if(len(s) > 0):
            c = np.max(s)
        else:
            c = 0
            
        if(c >= 4):
            if print_flag: print("Horizontal")
            return True
    
    # Checks for 4 consecutive pieces in vertical rows
    for i in range(S.shape[1]):
        s = [sum(1 for _ in group) for key, group in itertools.groupby(S[:,i]) if key]
        if(len(s) > 0):
            c = np.max(s)
        else:
            c = 0
            
        if(c >= 4):
            if print_flag: print("Vertical")
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
                if print_flag: print("Diagonal")
                return True
         
    return False
    
    

#if __name__ == '__main__':
def play(print_flag):
    # initialize 6x7 connect 4 board
    gameState = np.zeros((6,7), dtype=int)
    
    # to keep track of number of pieces each vertical column
    colScores = np.zeros(7, dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        if print_flag: print('%s moves' % name)

        # For storing previous game state and move in case of winning move
        prev_gameState = gameState

        # let player move at random
        gameState, colScore, move = move_at_random(gameState, colScores, player)

        # print current game state
        if print_flag:print_game_state(gameState)
        # print(colScores)
        
        # evaluate game state
        if move_was_winning_move(gameState, player,print_flag):
            if print_flag: print('player %s wins after %d moves' % (name, mvcntr))
            penultimate_states.append(prev_gameState)
            winning_moves.append(move)
            winning_player.append(player)
            wins_losses_draws.append(player)
            noWinnerYet = False
            
        # switch player and increase move counter
        player *= -1
        mvcntr +=  1


    if noWinnerYet:
        player = 0
        wins_losses_draws.append(0)
        if print_flag:print('game ended in a draw')
        
    return gameState, player


def plot_heatmap(data, figure, title):
    #plt.imshow(win_config, s, cmap='hot', interpolation='nearest')
    #data = win_configs/np.max(win_configs)
    plt.figure(figure)
    heatmap = plt.pcolor(data)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.4f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     )
    plt.title(title)
    plt.colorbar(heatmap)
    return plt


# Plotting Histogram
def plot_histogram(game_result, figure):
    #print(game_result)
    plt.figure(figure)
    plt.hist(game_result[game_result==1], label='R')
    plt.hist(game_result[game_result==-1], label='Y')
    plt.hist(game_result[game_result==0], label='draw')
    plt.title('Histogram of Wins and Loss')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')

    return plt

def collect_stats(print_flag=True):
    win_configs_1 = np.zeros((6,7), dtype=int)
    win_configs_2 = np.zeros((6,7), dtype=int)
    for i in range(1000):

        g, p = play(print_flag)
        count = 0

        if p==1:
            g[g==-1]=0
            win_configs_1 = win_configs_1 + g
        elif p==-1:
            g[g==1]=0
            win_configs_2 = win_configs_2 + np.abs(g)
        else:
            continue

    win_configs_1 = win_configs_1/1000
    win_configs_2 = win_configs_2/1000
    plot_histogram(np.array(wins_losses_draws), 1)
    plot_heatmap(win_configs_1, 2, "Statistics of Player 1")
    plot = plot_heatmap(win_configs_2, 3, "Statistics of Player 2")
    plot.show()
   
if __name__ == '__main__':
    #for i in range(1000):
    collect_stats(print_flag=True)
