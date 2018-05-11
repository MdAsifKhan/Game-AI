import numpy as np
import itertools

#  1 --> R (Red)
# -1 --> Y (Yellow)
#  0 --> ' ' (Empty)
symbols = {
     1:'R', 
    -1:'Y', 
     0:' '
}



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
    
    return S,F


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
    # initialize 3x3 tic tac toe board
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

        # let player move at random
        gameState, colScore = move_at_random(gameState, colScores, player)

        # print current game state
        print_game_state(gameState)
        # print(colScores)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            print('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    if noWinnerYet:
        print('game ended in a draw')
        
        
if __name__ == '__main__':
    #for i in range(1000):
    play()
