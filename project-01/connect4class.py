import numpy as np
import itertools
import matplotlib.pyplot as plt

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
        self.colScores = np.zeros(7, dtype=int)
    
        # initialize player number, move counter
        self.player = 1
        self.mvcntr = 1
    
        # initialize flag that indicates win
        self.noWinnerYet = True
                
    def reset_statistics(self):
        # To track good moves
        self.penultimate_states = []
        self.winning_moves = []
        self.winning_player = []
        #winning_conf = []
        self.wins_losses_draws = []

    def __init__(self):
        ## GAME STATE:
        self.start_new_game()
        
        ## STATISTICAL DATA:
        self.reset_statistics()
        
    def move_still_possible(self):
        S = self.gameState
        return not (S[S==0].size == 0)
           
    def move_at_random(self):
        S = self.gameState
        F = self.colScores
        p = self.player
        
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
        
        return (i,j)
    
    def print_game_state(self):
        B = np.copy(self.gameState).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = self.symbols[n]
        print(B)
    
    def move_was_winning_move(self):
        S = self.gameState
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

    def play_next_move(self):
            # get player symbol
            name = self.symbols[self.player]
            print('%s moves' % name)
    
            # For storing previous game state and move in case of winning move
            prev_gameState = self.gameState
    
            # let player move at random
            move = self.move_at_random()
    
            # print current game state
            self.print_game_state()
            # print(colScores)
            
            # evaluate game state
            if self.move_was_winning_move():
                print('player %s wins after %d moves' % (name, self.mvcntr))
                self.penultimate_states.append(prev_gameState)
                self.winning_moves.append(move)
                self.winning_player.append(self.player)
                self.wins_losses_draws.append(self.player)
                self.noWinnerYet = False
    
            # switch player and increase move counter
            player = self.player
            self.player *= -1
            self.mvcntr +=  1
    
            return move, player 
    
    def play(self):
        while self.move_still_possible() and self.noWinnerYet:
            self.play_next_move()
        if self.noWinnerYet:
            self.wins_losses_draws.append(0)
            print('game ended in a draw')
        self.game_over = True
    
    def is_gmae_over(self):
        return not self.noWinnerYet
    
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
    model = connect4class()
    model.collect_stats(10)
