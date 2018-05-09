
import numpy as np
import matplotlib.pyplot as plot

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
    print B

## ----------- TASK 1.2 ---------------

# Count accross game states
def iterateGameStateForCounts(gameState, counts):
    rows, columns = gameState.shape

    for x in range(0, rows):
        for y in range(0, columns):
            state = gameState[x][y]
            counts[x][y] += state

def plotHistogram(wins, draws):
    plot.hist(wins, label = "Wins")
    plot.hist(draws, label = "Draws")
    plot.xlabel("Value")
    plot.ylabel("Frequency")
    colors = ["red", "blue"]
    plot.legend(prop={"size": 10})
    plot.show()

# Determine probabilites for states that contributed to a win.
def determineWinMoveProbabilites(counts):
    sum = np.sum(counts.flatten())

    probabilities = np.zeros((3, 3))

    for x in range(0, 3):
        for y in range(0, 3):
            probabilities[x][y] = counts[x][y]/sum

    return probabilities

def moveXWithBestProbability(gameState, probabilities):
    x, y = np.where(gameState == 0)
    possibleMoveStates = zip(x, y)

    maxProbabilityState = (0, 0)
    maxProbability = 0

    for state in possibleMoveStates:
        x, y = state
        prob = probabilities[x][y]

        if prob >= maxProbability:
            maxProbabilityState = (x, y)
            maxProbability = prob

    x, y = maxProbabilityState
    gameState[x][y] = 1

    return gameState

def writeProbabilitiesToFile(probabilities):
    np.savetxt("probabilities.txt", probabilities)

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
       # print '%s moves' % name

        if player == 1:
            # move in state with best of probabilites if its x turn.
            gameState = moveXWithBestProbability(gameState, probabilities)
        else:
            # move at random if its 0 turn.
            gameState = move_at_random(gameState, player)

        # print current game state
        print_game_state(gameState)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            print 'player %s wins after %d moves' % (name, mvcntr)
            winningPlayer = player
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    #if noWinnerYet:
        #print 'game ended in a draw' 

    return (gameState, noWinnerYet, winningPlayer)

def randomTournament():
    counts = np.zeros((3, 3))

    wins = 0
    draws = 0

    for x in range(0, 1000):
        gameState, draw = playGame()

        if not draw:
            iterateGameStateForCounts(gameState, counts)
            wins += 1
        else:
            draws += 1

    return (np.ones(wins), np.zeros(draws), counts)

def winningProbabilitiesTournament():
    wins = 0
    draws = 0

    for x in range(0, 1000):
        gameState, noWinnerYet, winningPlayer = playGameWithWinningProbabilities(probabilities)

        if noWinnerYet:
            draws += 1
        else:
            wins += 1

    return (np.ones(wins), np.zeros(draws))

def playGame():
    gameState = np.zeros((3,3), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        #print '%s moves' % name

        # let player move at random
        gameState = move_at_random(gameState, player)

        # print current game state
        #print_game_state(gameState)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            #print 'player %s wins after %d moves' % (name, mvcntr)
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    #   if noWinnerYet:
        #print 'game ended in a draw' 

    return (gameState, noWinnerYet)

if __name__ == '__main__':
    wins, draws, counts = randomTournament()
    plotHistogram(wins, draws)

    probabilities = determineWinMoveProbabilites(counts)
    writeProbabilitiesToFile(probabilities)

    wins, draws = winningProbabilitiesTournament()
    plotHistogram(wins, draws)


    
