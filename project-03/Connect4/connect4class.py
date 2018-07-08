import numpy as np
import matplotlib.pyplot as plt
from gameState import move_still_possible, move_was_winning_move, possible_moves
from minimax import calculate_minmax_move
import time
import pausabletimer

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
        self.gameState.fill(0) # empty the board
    
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
        self.wins_losses_draws = []

    def __init__(self, players_to_use_MinMax = [], board_size = [6,7], max_depth = []):
        # Allocate array for connect4 board of the size given.
        # The traditional size is 6 x 7.
        self.gameState = np.zeros(board_size, dtype=int)
        
        # Defines which players use minmax and which move at random:
        self.players_to_use_MinMax = players_to_use_MinMax # can be [], [-1], [1] or [-1,1]
        
        # It has as many elements as players_to_use_MinMax, and for each player using 
        # MinMax it specifies how deep they build their MinMax tree, before a heuristic
        # is used.
        self.max_depth = max_depth
        
        self.start_new_game()
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
        
    def play_next_move(self, debug_print=False):
            def printif(s,b=True):
                if b:
                    print(s)
            b=debug_print
            
            # get player symbol
            name = self.symbols[self.player]

            # For storing previous game state and move in case of winning move
            prev_gameState = self.gameState
            
            if (self.player in self.players_to_use_MinMax):
                # Player Blue and Player red might not be equally "smart". If both play
                # MinMax, maybe one grows a tree of depth 1 before using heuristics and
                # the other grows a tree of depth 3 before using heuristics.
                player_depth = self.max_depth[self.players_to_use_MinMax.index(self.player)]
                reward, move = calculate_minmax_move(self.gameState, max_depth=player_depth, player=self.player)
                self.gameState[move] = self.player
                printif("Player " + name + " moves using MinMax to "
                      + str(move) + " with reward " + str(reward),b)
            else: # let player -1 move at random
                move = self.move_at_random()
                printif("Player " + name + " moves at random to " + str(move),b)
            
            if b: self.print_game_state()
            printif('\n\n',b)
            
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
        #plt.show()
    
    def collect_stats(self, num_games, experiment_name='UnnamedExperiment', polt_every_nth=1):
        tt = pausabletimer.PausableTimer()
        for i in range(num_games):
            tt.resume()
            self.play()
            self.start_new_game()
            tt.pause()
            
            if (i+1) % polt_every_nth == 0:
                '''
                Only print and save every once in a while for games that can be 
                played fast. Save every time or at least more often for games that take very long.
                '''
                # SAVING DATA TO FILE:
                # Save results thus far (because some experiments might run very
                # long and need to be stopt but I'd like to have the results thus far)
                print(self.wins_losses_draws)
                self.plot_histogram()
                plt.savefig(experiment_name + '_plot'+str(i+1)+'.png')
                plt.show()
                
                average_time_per_game = tt.t / (i+1)
                eta = (num_games - (i+1)) * average_time_per_game
                sRed, sYellow, sDraw = self.get_game_score()
                games_played = (i+1) / num_games * 100
                
                std_game = 'Game ' + str(i+1)
                str_progress = str(games_played) + ' % done ( i.e. ' + str(i) + ' games done; ' + str(num_games - i) + ' left to go; total of ' + str(num_games) + ' games)'
                str_avgTimePerGame = 'Average time per Game: ' + str(average_time_per_game)
                str_timeThusFar = 'Time thus far: ' + str(tt.t) + 's or ' + str(tt.t/60/60)+'h'
                str_eta = 'Estimated time left: ' + str(eta) + 's or ' + str(eta/60/60)+'h'
                str_score = 'Red: ' + str(sRed) + ' Yellow: ' + str(sYellow) + ' Draw: ' + str(sDraw)
                 
                textList = ['\n',std_game ,str_score, str_progress, str_eta, str_avgTimePerGame, str_timeThusFar, str_eta]
                outF = open(experiment_name  + "_StatsAndData.txt", "a")
                for line in textList:
                  # write line to output file
                  outF.write(line)
                  outF.write("\n")
                outF.close()
                
                
                # GIVE USER FEEDBACK ON HOW LONG HE WILL HAVE TO WAIT:
                # Show progress:
                '''
                #Test data for output here:
                i = 30
                num_games = 1000
                tt = pausabletimer
                tt.t = 42.42432020340202
                '''
                
                print(str_progress)
                
                # show eta:
                average_time_per_game = tt.t / (i+1)
                print(str_score)
                print(str_avgTimePerGame)
                print(str_timeThusFar)
                print(str_eta)
                
                print('---------------------------------------------------------\n\n')
            

def run_experiment(experiment_name='UnnamedExperiment', num_games = 10, players_to_use_MinMax = [], max_depth = [], board_size = [6,7], polt_every_nth=1):
    start = time.time()
    model = connect4class(players_to_use_MinMax = players_to_use_MinMax, max_depth = max_depth, board_size = board_size)
    model.collect_stats(num_games, experiment_name=experiment_name,polt_every_nth=polt_every_nth)
    end = time.time()
    str_timeWithPlot = 'Time includig plotting: ' + str(end - start)
    print(str_timeWithPlot)
    
    outF = open(experiment_name + "_StatsAndData.txt", "a")
    outF.write(str_timeWithPlot)
    outF.write("\n")
    outF.close()
    
if __name__ == '__main__':
    run_experiment(experiment_name='UnnamedExperiment', num_games = 10, players_to_use_MinMax = [], max_depth=[], board_size = [6,7])
    

