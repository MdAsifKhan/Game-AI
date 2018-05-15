
import numpy as np
import pdb
import matplotlib.pyplot as plt

def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S


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

def best_move(S, p):
    xs, ys = np.where(S==0)
    x_opt, y_opt = xs[0], ys[0]
    score_x = np.zeros(S.shape)
    score_o = np.zeros(S.shape)
    bestmove = False
    # Find score for all empty cells
    for x,y in zip(xs,ys):
        scr_x, scr_o = score(S, x, y, p)
        # Check if 'x' already has a score of 3
        if scr_x == 3:
            bestmove = True
            x_opt, y_opt = x, y
            break
        score_x[x,y] = scr_x
        score_o[x,y] = scr_o
        # If score of 'x' is not 3    
    if not bestmove:
        # Check if 'o' can get a score of 3
        if 3 in score_o:
            x_opt, y_opt = np.where(score_o==3)
        else:
            # Find Cell with maximum score for x
            x_max, y_max = np.where(score_x==score_x.max())
            # If score maximum at more than 1 location, 
            # select cell with score greater than x
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

def play_game_heuristic(player):
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)
    # initialize, move counter
    mvcntr = 1
    # initialize flag that indicates win
    noWinnerYet = True
    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print('%s moves' % name)
        # let player move at random
        gameState = move_heuristic(gameState, player)
        # print current game state
        print_game_state(gameState)
        # evaluate game state
        if move_was_winning_move(gameState, player):
            game_result = player
            """
            for x,y in zip(xs,ys):
                field_player1[x,y] += 1
            """
            print('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False
        # switch player and increase move counter
        player *= -1
        mvcntr +=  1
    if noWinnerYet:
        game_result = 0
        print('game ended in a draw')
    return game_result    

def plot_histogram(game_result):
    #print(game_result)
    plt.hist(game_result[game_result==1], label='x')
    plt.hist(game_result[game_result==-1], label='o')
    plt.hist(game_result[game_result==0], label='draw')
    plt.title('Histogram of Wins and Loss')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()

def play_game_heuristic_tournament(number_games=1000):

    start_player = 1
    game_result = np.empty(number_games)
    for game_count in range(number_games):  
        #print('Game {}'.format(game_count+1))
        result = play_game_heuristic(start_player)
        game_result[game_count] = result

    return game_result
if __name__ == '__main__':

    #game_result = {'o':0,'x':0,'Draw':0}
    # Part 1.2.1
    """
    simulation = 1000
    strategy = 'random'
    game_simulate(simulation, strategy, hist=True)
    """
    # Part 1.2.2
    number_games=1000
    game_result = play_game_heuristic_tournament(number_games)
    plot_histogram(game_result)
    
        
        


