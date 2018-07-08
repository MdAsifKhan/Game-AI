import numpy as np
import matplotlib.pyplot as plt
from gameState import move_still_possible, move_was_winning_move, possible_moves
from minimax import calculate_minmax_move
import time

class connect4class:
    """Models the game Connect 4 on a 6x7 board"""
    
    # Define color mapping as static class variables: 
    #  1 --> R (Red)
    # -1 --> Y (Yellow)
    #  0 --> ' ' (Empty)
    symbols = {
         1:'R', 
        -1:'Y', 
         0:' '
    }
        
    def start_new_game(self):
        # initialize 6x7 connect 4 board
        self.gameState = np.zeros((6,7), dtype=int)
        
        # to keep track of number of pieces each vertical column
        self.colScores = np.zeros(7, dtype=int) # TODO: Can this be deleted?
    
        # initialize player number, move counter
        self.player = 1
        self.mvcntr = 1
    
        # initialize flag that indicates win
        self.noWinnerYet = True
        
        # this flag indicates if the game is over yet:
        self.game_over = False
                
    def reset_statistics(self):
        # To track good moves
        self.penultimate_states = []
        self.winning_moves = []
        self.winning_player = []
        #winning_conf = []
        self.wins_losses_draws = []

    def __init__(self, players_to_use_MinMax = [1], board_size = [6,7]):
        ## GAME STATE:
        self.start_new_game()
        
        # Defines which players use minmax and which move at random:
        self.players_to_use_MinMax = players_to_use_MinMax # can be [], [-1], [1] or [-1,1]
        
        ## STATISTICAL DATA:
        self.reset_statistics()
        
    def move_still_possible(self):
        return move_still_possible(self.gameState)
           
    def move_at_random(self):
        S = self.gameState
        p = self.player
            
        # Obtain a list of all possible moves:
        possible = possible_moves(S)
        
        # and pick one at random:
        i = np.random.randint(len(possible))
        random_move = possible[i] 
        
        # place the players chip at the selected position:
        S[random_move] = p
        
        return random_move
    
    def print_game_state(self):
        B = np.copy(self.gameState).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = self.symbols[n]
        print(B)
    
    def move_was_winning_move(self):
        return move_was_winning_move(self.gameState)
        
    def play_next_move(self):
            # get player symbol
            name = self.symbols[self.player]

            # For storing previous game state and move in case of winning move
            prev_gameState = self.gameState
            
            if (self.player in self.players_to_use_MinMax):  # let player 1 move according to MinMax
                reward, move = calculate_minmax_move(self.gameState, max_depth=4, player=self.player)
                self.gameState[move] = self.player
                print("Player " + name + " moves using MinMax to "
                      + str(move) + " with reward " + str(reward))
            else: # let player -1 move at random
                move = self.move_at_random()
                print("Player " + name + " moves at random to " + str(move))
            
            self.print_game_state()
            print('\n\n')
            #move = self.move_at_random()
            
            # evaluate game state
            if self.move_was_winning_move():
                print('player %s wins after %d moves' % (name, self.mvcntr))
                self.penultimate_states.append(prev_gameState)
                self.winning_moves.append(move)
                self.winning_player.append(self.player)
                self.wins_losses_draws.append(self.player)
                self.noWinnerYet = False
                self.game_over = True
    
            # switch player and increase move counter
            player = self.player
            self.player *= -1
            self.mvcntr +=  1
            
            # Check if there will be another move in this round or if the round is over:
            if self.move_still_possible() and self.noWinnerYet:
                pass
            elif not self.move_still_possible() and self.noWinnerYet:
                self.wins_losses_draws.append(0)
                print('game ended in a draw') 
                self.game_over = True            
    
            return move, player 
    
    def play(self):
        while not self.is_game_over():
            self.play_next_move()
        
    def is_game_over(self):
        return self.game_over
    
    def get_game_score(self):
        game_result = np.array(self.wins_losses_draws)
        Red = np.size(game_result[game_result==1])
        Yellow = np.size(game_result[game_result==-1])
        Draw = np.size(game_result[game_result==0])
        return Red, Yellow, Draw 
    
    # Plotting Histogram
    def plot_histogram(self):
        game_result = np.array(self.wins_losses_draws)
        #print(game_result)
        plt.hist(game_result[game_result==1], label='R')
        plt.hist(game_result[game_result==-1], label='Y')
        plt.hist(game_result[game_result==0], label='draw')
        plt.title('Histogram of Wins and Loss')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.show()
    
    def collect_stats(self, num_games):
        
        
        for i in range(num_games):
            self.play()
            self.start_new_game()
        
        print(self.wins_losses_draws)
        self.plot_histogram()
   
if __name__ == '__main__':
    #model = connect4class(players_to_use_MinMax = [1], board_size = [6,7])
    #model.collect_stats(10)
    
    model = connect4class(players_to_use_MinMax = [1,-1], board_size = [19,19])
    model.collect_stats(10)
    
