# Project-01

In this project we implement simple strategies for turn based games.

## Task 1.1: Probabilistic Strategy for player 'X' in Tic-Tac-Toe. We implement it in easy 4 steps:
* Play a tournament of 1000 games where ‘X’ and ‘O’ moves randomly.
* Determine count of winning field of ‘X’ and ‘O’.
* Normalize count to obtain probabilities.
* Move ‘X’ with probabilities obtain in Step-3 and ‘O’ uniformly at randomly.

```python tic-tac-toe_Task1-2.py ```

## Task 1.2: Implement simple heuristiic to decide move of player 'X' in Tic-Tac-Toe.

We implement following heuristic:

First we define criteria and measure of winning.
* Reward: Consecutive 1's either row, column or diagonal wise.
* Winning Situation: Reward of ‘3’.

Steps to find auspicious move for player ‘X’.

* For every empty field check if it can result in a winning situation of player ‘X’.
	IF True, location of field is an auspicious move. Break! ELSE, Continue to Step 2. 
* For every empty field check if it can result in a winning situation of player ‘O’.
	IF True, location of field is an auspicious move. Break! ELSE, Continue to Step 3.
* Find empty field which can result in a maximum reward of player ‘X’.
	IF more than 1, Field where reward of ‘X’ is greater than ‘O’ is an auspicious move.
	ELSE, Location of field is an auspicious move.


```python tic_tac_toe.py```



## Task 1.3: Implement mechanics of Connect four.

Game Mechanics for connect 4:
* Red always starts first.
* A counter is kept to keep track of number of dices filled in every column.
* The player in turn chooses a unfilled column randomly.
* Winning condition:
	Whether the horizontal rows have similar consecutive dices > 4.
	Whether the vertical columns have similar consecutive dices > 4.
	Whether the diagonals with size > 4 have similar consecutive dices > 4.

```python connect4.py```

## Requirements
* [PyGame](https://www.pygame.org/news)
* Python3+