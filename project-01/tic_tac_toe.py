import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time as t

def move_still_possible(S):
    return not (S[S==0].size == 0)

def move_at_random(S, p):
    xs, ys = np.where(S==0)
    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S

def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print(B)


##########################
##### Task 1.2.1 #########
#####			 #########
##########################

def playGameRandomly(player):
    gameState = np.zeros((3,3), dtype=int)

    mvcntr = 1
    # initialize flag that indicates win
    noWinnerYet = True
    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        #print '%s moves' % name

        # let player move at random
        gameState = move_at_random(gameState, player)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            #print 'player %s wins after %d moves' % (name, mvcntr)
            noWinnerYet = False
            winningPlayer = player
        # switch player and increase move counter
        player *= -1
        mvcntr +=  1

        if noWinnerYet:
            winningPlayer = 0
        #print 'game ended in a draw' 
    return (gameState, winningPlayer)

def randomTournament(start_player):
    # Count accross game states
    wins_x = 0
    wins_o = 0
    counts_x = np.zeros((3, 3))
    counts_o = np.zeros((3, 3))
    game_result = np.empty(1000)
    for x in range(0, 1000):
        gameState, winningPlayer = playGameRandomly(start_player)
        game_result[x] = winningPlayer
        if winningPlayer == 1:
            gameState[gameState==-1] = 0
            counts_x += gameState
            wins_x += 1
        elif winningPlayer == -1:
            gameState[gameState==1] = 0
            counts_o += np.abs(gameState)
            wins_o += 1
        else:
            continue
    return (game_result, counts_x, counts_o, wins_x, wins_o)
    
# Determine probabilites for states that contributed to a win.
def determineWinMoveProbabilites(counts_x, counts_o):
    
    counts_x = counts_x.flatten()
    probabilities_x = counts_x/np.sum(counts_x)

    counts_o = counts_o.flatten()
    probabilities_o = counts_o/np.sum(counts_o)

    return probabilities_x, probabilities_o

def writeProbabilitiesToFile(probabilities_x, probabilities_o, file):
    # Save Probabilities to disk
    data = {'probabilities_x':probabilities_x,'probabilities_o':probabilities_o}
    df = pd.DataFrame(data)
    df.to_csv(file)

def moveWithBestProbability(gameState, probabilities):

    x, y = np.where(gameState == 0)

    probabilities = probabilities.reshape(3,3)

    x_opt, y_opt = np.where(probabilities == np.max(probabilities[x,y]))
    if len(x_opt)>1:
        x_opt = x_opt[np.random.permutation(np.arange(x_opt.size))[0]]
    if len(y_opt)>1:
        y_opt = y_opt[np.random.permutation(np.arange(y_opt.size))[0]]
    
    gameState[x_opt,y_opt] = 1
    probabilities[x_opt,y_opt] = 0
    return gameState

def playGameWithWinningProbabilities(probabilities):
    gameState = np.zeros((3,3), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    winningPlayer = 0

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]

        if player == 1:
            # move in state with best of probabilites if its x turn.
            gameState = moveWithBestProbability(gameState, probabilities)
        else:
            # move at random if its 0 turn.
            gameState = move_at_random(gameState, player)

        # print current game state
        # print_game_state(gameState)
        # evaluate game state
        if move_was_winning_move(gameState, player):
            #print('player %s wins after %d moves' % (name, mvcntr))
            winningPlayer = player
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1

    if noWinnerYet:
        winningPlayer = 0
        #print 'game ended in a draw' 

    return winningPlayer


def winningProbabilitiesTournament(probabilistic_player, file):

    data = pd.read_csv(file)
    if probabilistic_player == 1:
        probabilities = data['probabilities_x'].values
    else:
        probabilities = data['probabilities_o'].values 
    game_result = np.empty(1000)           
    for x in range(0, 1000):
        probabilities_x = np.copy(probabilities)
        winningPlayer = playGameWithWinningProbabilities(probabilities_x)
        game_result[x] = winningPlayer

    return game_result




##########################
##### Task 1.2.2 #########
#####			 #########
##########################

# Find score of 'X' and 'O' if player 'p'='X' makes move at location x,y
def score(S,x,y,p):
    S[x,y] = p
    score_x = np.max(np.array([np.max(np.sum(S, axis=0)),np.max(np.sum(S, axis=1)),
        np.sum(np.diag(S)),np.sum(np.diag(np.rot90(S)))]))
    S[x,y] = 0
    S1 = np.copy(S)
    S1[S==1] = -1
    S1[S==-1] = 1
    S1[x,y] = p
    score_o = np.max(np.array([np.max(np.sum(S1, axis=0)),np.max(np.sum(S1, axis=1)),
        np.sum(np.diag(S1)),np.sum(np.diag(np.rot90(S1)))]))
    return score_x, score_o


# Evaluate all possible position and find best move for player P, here P is 'X'
def best_move(S, p):
    xs, ys = np.where(S==0)
    x_opt, y_opt = xs[0], ys[0]
    score_x = np.zeros(S.shape)
    score_o = np.zeros(S.shape)
    bestmove = False
    # Find score for all empty cells
    for x,y in zip(xs, ys):
        scr_x, scr_o = score(S, x, y, p)
        # Check if 'X' already is in winning state i.e. move can result in a score of 3
        if scr_x == 3:
            bestmove = True
            x_opt, y_opt = x, y
            break
        score_x[x,y] = scr_x
        score_o[x,y] = scr_o
        # If score of 'X' is not 3    
    if not bestmove:
        # Check if 'O' is in winning state i.e move can result in a score of 3
        if 3 in score_o:
            x_opt, y_opt = np.where(score_o==3)
        else:
        	# Find move which will maximize score of x 
            # Find Cell where score of x is maximum
            x_max, y_max = np.where(score_x==score_x.max())
            # If score is maximum for multiple cells, 
            # select one where score is greater than 'O'
            if len(x_max) or len(y_max)>1:
                for x,y in zip(x_max, y_max):
                    if score_x[x,y]>score_o[x,y]:
                        x_opt, y_opt = x, y
                        break
    return x_opt, y_opt

def move_heuristic(S, p):

    if p == -1:
        xs, ys = np.where(S==0)
        i = np.random.permutation(np.arange(xs.size))[0]
        S[xs[i],ys[i]] = p
        return S
    else:
        x_opt, y_opt = best_move(S,p)
        S[x_opt, y_opt] = p
    return S

def play_game_heuristic(start_player):
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)
    # initialize player number, move counter
    player = 1
    # initialize, move counter
    mvcntr = 1
    # initialize flag that indicates win
    noWinnerYet = True
    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        # print('%s moves' % name)
        # let player move at random
        gameState = move_heuristic(gameState, player)
        # print current game state
        # print_game_state(gameState)
        # evaluate game state
        if move_was_winning_move(gameState, player):
            game_result = player
            #print('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False
        # switch player and increase move counter
        player *= -1
        mvcntr +=  1
    if noWinnerYet:
        game_result = 0
        #print('game ended in a draw')
    return game_result

def heuristic_tournament(start_player=1, number_games=1000):

    game_result = np.empty(number_games)
    for game_count in range(number_games):  
        #print('Game {}'.format(game_count+1))
        result = play_game_heuristic(start_player)
        game_result[game_count] = result

    return game_result

# Plotting Histogram
def plot_histogram(game_result, title, figure):
    #print(game_result)
    plt.figure(figure)
    plt.hist(game_result[game_result==1], label='x')
    plt.hist(game_result[game_result==-1], label='o')
    plt.hist(game_result[game_result==0], label='draw')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')

    return plt

if __name__ == '__main__':

    seed = 88958
    np.random.seed(seed=seed)

    print("Three histograms would be plotted for the respective three tournaments.")
    print("Random Tournament")
    print("Winning Probabilities Tournament")
    print("Heuristic Tournament")

    # Random Tournament
    game_result, counts_x, counts_o, wins_x, wins_o = randomTournament(1)
    plot = plot_histogram(game_result, "Random Tournament - Histogram of wins and loses", 1)

    # Winning Probabilities Tournament
    probabilities_x, probabilities_o = determineWinMoveProbabilites(counts_x, counts_o)
    probabilitiesFile = "probabilities.txt"
    writeProbabilitiesToFile(probabilities_x, probabilities_o, probabilitiesFile)
    game_result = winningProbabilitiesTournament(1, probabilitiesFile)
    plot_histogram(game_result, "Winning Probabilities Tournament - Histogram of wins and loses", 2)

    # Heuristic Tournament
    game_result = heuristic_tournament()
    plot = plot_histogram(game_result, "Heuristic Tournament - Histogram of wins and loses", 3)

    plot.show()

