#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:35:15 2018

@author: Daniel Biskup
"""

import pygame
import time
import connect4class
import numpy as np

SIMULATION_SPEED = 10.0
SPLASH_SCREEN_TIME = 0.0

pygame.init()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
COLOR_KEY = (255, 0, 255) # Transparent color

size = width, height = 1366, 768
screen = pygame.display.set_mode(size)

def load_image_and_scale(path, width, height):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (int(width), int(height) ))
    rect  = image.get_rect()
    return image, rect

# Show splash screen:
splash_screen, splash_screen_rect = load_image_and_scale("splash_screen.jpg", 700, 700)
splash_screen_rect.center = (width/2, height/2)
screen.fill(BLACK)
screen.blit(splash_screen, splash_screen_rect)
pygame.display.flip()
time.sleep(SPLASH_SCREEN_TIME)


##### Setting up the board image:
board_height = height
cell_size = board_height / 6
board_width = cell_size * 7

board_image, board_rect = load_image_and_scale("board.jpg", board_width, board_height)
board_rect.center = (width/2, height/2)

# Screen coordinates are given in (x,y) and board coordinates in (i,j)
# (i,j) is (up, right)    matrix or array indices
# (x,y) is (right, down)  screen coordinates
y_coord_of_cell_i = np.linspace(cell_size/2, board_height - cell_size/2, 6)
y_coord_of_cell_i = y_coord_of_cell_i[::-1]
x_coord_of_cell_j = np.linspace(cell_size/2, board_width - cell_size/2, 7)

def array_index_to_coordinates(i,j):
    x = x_coord_of_cell_j[j]
    y = y_coord_of_cell_i[i]
    return [int(x), int(y)]

# Create holes in the board:
hole_radius = int( (cell_size/2) * 0.75 )

board_image.set_colorkey(COLOR_KEY)
for x in x_coord_of_cell_j:
    for y in y_coord_of_cell_i:
        pygame.draw.circle(board_image, COLOR_KEY, [int(x), int(y)], hole_radius)
# Afterwards shift those values by the board position:
x_coord_of_cell_j = x_coord_of_cell_j + board_rect.topleft[0]
y_coord_of_cell_i = y_coord_of_cell_i + board_rect.topleft[1]

background_image, background_image_rect = load_image_and_scale("background.jpg", width, height)
background_image_rect.center = (width/2, height/2)

score_image, score_image_rect = load_image_and_scale("board.jpg", 150, 100)
score_image_rect.topleft = (0,0)

##### Create the chips:
class Chip():
    # Coordinates in this class are given in screen coordinates.
    # start and destination or positions refering to the center of the chip.
    def __init__(self, image, player, start, destination):
        self.image = image
        self.rect = image.get_rect()
        self.start = start
        self.destination = destination
        self.position = start
        self.speed = 1.0
        self.in_animation = True
        self.t = 0.0
        self.speed = 1.0

    def move_back_to_start(self):
        self.destination = self.start
        self.start = self.position
        self.in_animation = True
        
    def move_to(self, destination):
        self.destination = destination
        self.start = self.position
        self.in_animation = True
        
    def update(self, delta_time):
        if(self.in_animation):
            self.t = self.t + delta_time
            if self.t <= 1.0:
                direction = self.destination - self.start
                self.position = self.start + self.t*direction
            else:
                self.t = 0.0
                self.position = self.destination
                self.in_animation = False
        
    def draw(self):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)        
        
chips = []
chip_radius = (cell_size/2) * 0.80
image_red,_ = load_image_and_scale("chip_red.png", chip_radius*2, chip_radius*2)
image_yellow,_ = load_image_and_scale("chip_yellow.png", chip_radius*2, chip_radius*2)
    
def add_chip(move, player):
    # For move (i,j) coordinates are expected as array index.
    i,j = move
    destination = np.asarray(array_index_to_coordinates(i,j))
    start = np.array([destination[0], 0 - chip_radius])
    
    if player == 1:
        image = image_red;
    elif player == -1:
        image = image_yellow;
    chips.append(Chip(image, 0, start, destination))

# Some flags for controlling the game loop:
COUNT_ANIM = 0

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans', 40)

model = connect4class.connect4class()    
getTicksLastFrame = pygame.time.get_ticks()
simulation_speed = SIMULATION_SPEED # 1.0 is normal speed.
running = True
while running:
    # get the time delta to last frame in seconds.
    t = pygame.time.get_ticks()
    delta_time = (t - getTicksLastFrame) / 1000.0
    delta_time = delta_time * simulation_speed
    getTicksLastFrame = t

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                simulation_speed = 1.0
            if event.key == pygame.K_2:
                simulation_speed = 2.0
            if event.key == pygame.K_3:
                simulation_speed = 3.0
            if event.key == pygame.K_4:
                simulation_speed = 4.0
            if event.key == pygame.K_5:
                simulation_speed = 5.0
            if event.key == pygame.K_6:
                simulation_speed = 6.0
            if event.key == pygame.K_7:
                simulation_speed = 7.0
            if event.key == pygame.K_8:
                simulation_speed = 8.0
            if event.key == pygame.K_9:
                simulation_speed = 100.0
            if event.key == pygame.K_0:
                simulation_speed = 0.0

    # Draw everythin:
    screen.fill(WHITE)
    screen.blit(background_image, background_image_rect)     
    for chip in chips:
        chip.update(delta_time)
        chip.draw()
    screen.blit(board_image, board_rect)
    # Draw the Score:
    screen.blit(score_image, score_image_rect)
    Red, Yellow, Draw = model.get_game_score()
    TextColor = (0, 255, 0)
    textRed = myfont.render('Red: ' + str(Red), False, TextColor)
    textYellow = myfont.render('Yellow: ' + str(Yellow), False, TextColor)
    textDraw = myfont.render('Draw: ' + str(Draw), False, TextColor)
    text_x = 10
    text_y = 10
    text_offset = 30
    screen.blit(textRed,(text_x ,text_y + text_offset*0))
    screen.blit(textYellow,(text_x ,text_y + text_offset*1))
    screen.blit(textDraw,(text_x ,text_y + text_offset*2))
    pygame.display.flip()
    
    # Check if any chip is in animation right now:
    any_chip_in_animation = False
    for chip in chips:
        if chip.in_animation == True:
            any_chip_in_animation = True
    
    if not any_chip_in_animation:
        if not model.is_game_over():
            move, player = model.play_next_move()
            add_chip(move,player)
        else:
            # render the score as text
            if COUNT_ANIM == 0:
                #TODO Mark four winning chips animation.
                COUNT_ANIM = COUNT_ANIM + 1
            elif COUNT_ANIM == 1:
                # move chips from the board:
                for chip in chips:
                    chip.move_back_to_start()
                COUNT_ANIM = COUNT_ANIM + 1
            elif COUNT_ANIM == 2:
                chips = []
                COUNT_ANIM = 0
                model.plot_histogram()
                model.start_new_game()            


 
pygame.quit()
            