#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:35:15 2018

@author: Daniel Biskup
"""

import sys, pygame
import time
import connect4class
import numpy as np
pygame.init()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

COLOR_KEY = (255, 0, 255) # Transparent color

size = width, height = 1366, 768

speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

model = connect4class.connect4class()

# Show splash screen:


splash_screen = pygame.image.load("splash_screen.jpg")
splash_screen = pygame.transform.scale(splash_screen, (width, height) )
splash_screen_rect = splash_screen.get_rect()
splash_screen_rect.center = (width/2, height/2)

splash_screen.set_colorkey(COLOR_KEY)
pygame.draw.circle(splash_screen, COLOR_KEY, [0, 0], 40)

screen.fill(white)
screen.blit(splash_screen, splash_screen_rect)
#pygame.display.flip()
#time.sleep(2)


##### Setting up the board image:
board_height = height
cell_size = board_height / 6
board_width = cell_size * 7

board_image = pygame.image.load("trees.jpg")
board_image = pygame.transform.scale(board_image, (int(board_width), int(board_height) ))
board_rect  = board_image.get_rect()
board_rect.center = (width/2, height/2)
board_rect.topleft

# Screen coordinates are given in (x,y) and board coordinates in (i,j)
# (i,j) is (up, right)    matrix or array indices
# (x,y) is (right, down)  screen coordinates
y_coord_of_cell_i = np.linspace(cell_size/2, board_height - cell_size/2, 6)
y_coord_of_cell_i = y_coord_of_cell_i[::-1]
x_coord_of_cell_j = np.linspace(cell_size/2, board_width - cell_size/2, 7)

# Create holes in the board:
board_image.set_colorkey(COLOR_KEY)
for x in x_coord_of_cell_j:
    for y in y_coord_of_cell_i:
        pygame.draw.circle(board_image, COLOR_KEY, [int(x), int(y)], 40)

#screen.fill(white)
screen.blit(board_image, board_rect)
pygame.display.flip()

class chip():
    #image_red = pygame.image.load("ball.gif")
    #image_ = pygame.image.load("ball.gif")
    
    def __init__(self, player):
        ## GAME STATE:
        self.position = (0,0)
        self.destination = (0,0)
        self.speed = 1.0
        self.in_animation = False
        
        if player == 1:
            self.image = 0
        elif player == -1:
            self.image = 0
        
    def update(self):
        if(self.in_animation):
            pass

running = True
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

 #   ballrect = ballrect.move(speed)
#    if ballrect.left < 0 or ballrect.right > width:
#        speed[0] = -speed[0]
#    if ballrect.top < 0 or ballrect.bottom > height:
        #speed[1] = -speed[1]

    #screen.fill(black)
#    screen.blit(ball, ballrect)
    #pygame.display.flip()
 
pygame.quit()
            