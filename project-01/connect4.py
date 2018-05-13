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


def move_was_winning_move(S, p):
    c = 0
    
    # Checks for 4 consecutive pieces in horizontal rows
    for i in range(S.shape[0]):
        s = [sum(1 for _ in group) for key, group in itertools.groupby(S[i,:]) if key]
        if(len(s) > 0):
            c = np.max(s)
        else:
            c = 0
            
        if(c >= 4):
            print("Horizontal")
            return True
    
    # Checks for 4 consecutive pieces in vertical rows
    for i in range(S.shape[1]):
        s = [sum(1 for _ in group) for key, group in itertools.groupby(S[:,i]) if key]
        if(len(s) > 0):
            c = np.max(s)
        else:
            c = 0
            
        if(c >= 4):
            print("Vertical")
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
                print("Diagonal")
                return True
         
    return False
    
    

#if __name__ == '__main__':
def play():
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
        print('%s moves' % name)

        # For storing previous game state and move in case of winning move
        prev_gameState = gameState

        # let player move at random
        gameState, colScore, move = move_at_random(gameState, colScores, player)

        # print current game state
        print_game_state(gameState)
        # print(colScores)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            print('player %s wins after %d moves' % (name, mvcntr))
            penultimate_states.append(prev_gameState)
            winning_moves.append(move)
            winning_player.append(player)
            wins_losses_draws.append(player)
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    if noWinnerYet:
        wins_losses_draws.append(0)
        print('game ended in a draw')


# Plotting Histogram
def plot_histogram(game_result):
    #print(game_result)
    plt.hist(game_result[game_result==1], label='R')
    plt.hist(game_result[game_result==-1], label='Y')
    plt.hist(game_result[game_result==0], label='draw')
    plt.title('Histogram of Wins and Loss')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()

def collect_stats():
    for i in range(10):
        play()
    
    print(wins_losses_draws)
    plot_histogram(np.array(wins_losses_draws))

   
if __name__ == '__main__':
    #for i in range(1000):
    collect_stats()
