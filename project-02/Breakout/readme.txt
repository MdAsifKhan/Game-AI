Breakout -> Working directory for Breakout game.

breakout.py -> Source code to run to main game loop
It initilizes a pygame window and renders the game objects (ball, bricks and paddle) and defines functions to update these. Also handles events in case of situation
when game is over.

breakout_sprites.py -> Source code to define the pygame sprites. It defines classes and functions to render the pygame objects.

images -> Sub folder which contains images required in the pygame
-background.png: Pygame window background image
-ball.png: Image of ball
-brick.png: Image of brick
-player.png: Image of player (paddle)

audio: Sub folder which contains audio files required in the pygame
-beep.wav: Audio file to play a beep sound when ball collides with other game objects

Execution:
Run the source code breakout.png
It opens a new pygame window, renders the objects on screen and starts the game play. The ball moves within the game window and tries to hit the bricks on order to
break them. The paddle movement is modified so that instead of an external user event the paddle moves by itself. Used a random number generator (0-1) at each step.
Based on the number the paddle either moves to the left (>=0.5) or to the right(<0.5). Game is over if the ball fails to hit the paddle and goes out of the bottom of
the window.
The speed of movement of the ball and paddle gets doubled every 10 seconds.