# Game-AI Project-01

Description of functions used in the tasks.

## Task 1.1: Acquaint yourself with python / numpy:
No functions implemented.

## Task 1.2: Simple strategies for tic tac toe:

### Task 1.2.1 Implement a probabilistic strategy:

```python
#Plays tic tac toe randomly.
def playGameRandomly(player)
```

```python
#Plays a tournament of 1000 tic tac toe games with random moves.
def randomTournament(start_player)
```

```python
#Determine probabilites for states that contributed to a win.
def determineWinMoveProbabilites(counts_x, counts_o)
```

```python
#Writes probabilities to a file.
def writeProbabilitiesToFile(probabilities_x, probabilities_o, file)
```

```python
#Determines the next move using the probabilites.
def moveWithBestProbability(gameState, probabilities)
```

```python
#Plays tic tac toe with winning probabilites.
def playGameWithWinningProbabilities(probabilities)
```

```python
#Plays a tournament of 1000 games, using winning probabilites 
for x while o moves randomly.
def winningProbabilitiesTournament(probabilistic_player, file)
```

### Task 1.2.2. Implement a heuristic strategy:

```python
#Find score of 'X' and 'O' if player 'p'='X' makes move at location x,y
def score(S,x,y,p)
```

```python
#Evaluate all possible position and find best move for player P, here P is 'X'
def best_move(S, p)
```

```python
#Determines next move with heuristic strategy.
def move_heuristic(S, p)
```

```python
#Plays tic tac toe with heuristic strategy.
def play_game_heuristic(start_player)
```

```python
#Plays a tournament of 1000 games with heuristic strategy.
def heuristic_tournament(start_player=1, number_games=1000)
```

```python
#Plotting Histogram
def plot_histogram(game_result, title, figure)
```

## Task 1.3: Connect four:

```python
#Checks if move is possible using the current game state.
def move_still_possible(S)
```

```python
#Determines next move randomly for the provided player in the current game state.
def move_at_random(S, F, p)
```

```python
#Prints provided game state.
def print_game_state(S)
```

```python
#Checks if move resulted into a win.
def move_was_winning_move(S, p)
```

```python
#Plays Connect 4.
def play()
```

```python
#Plots Histogram of wins and loses.
def plot_histogram(game_result)
```

```python
#Collect statistics.
def collect_stats()
```

## Task 1.4: Breakout:
No functions implemented.


