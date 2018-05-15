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

def init_game():
    global screen,BLACK,WHITE,COLOR_KEY,splash_screen,splash_screen_rect,size
    global board_height,cell_size,board_width,board_image, board_rect,background_image, background_image_rect
    global y_coord_of_cell_i, x_coord_of_cell_j, y_coord_of_cell_i, chip_radius, image_red, image_yellow 
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    COLOR_KEY = (255, 0, 255) # Transparent color

    size = width, height = 1366, 768
    screen = pygame.display.set_mode(size)

    # Show splash screen:
    splash_screen, splash_screen_rect = load_image_and_scale("splash_screen.jpg", 700, 700)
    splash_screen_rect.center = (width/2, height/2)
    screen.fill(BLACK)
    screen.blit(splash_screen, splash_screen_rect)
    pygame.display.flip()
    time.sleep(2)

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

    chip_radius = (cell_size/2) * 0.80
    image_red,_ = load_image_and_scale("chip_red.png", chip_radius*2, chip_radius*2)
    image_yellow,_ = load_image_and_scale("chip_yellow.png", chip_radius*2, chip_radius*2)

def load_image_and_scale(path, width, height):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (int(width), int(height) ))
    rect  = image.get_rect()
    return image, rect



def array_index_to_coordinates(i,j):
    x = x_coord_of_cell_j[j]
    y = y_coord_of_cell_i[i]
    return [int(x), int(y)]



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

def gui_game(chips):
    # Some flags for controlling the game loop:
    COUNT_ANIM = 0

    model = connect4class.connect4class()    
    getTicksLastFrame = pygame.time.get_ticks()
    simulation_speed = 1.0 # 1.0 is normal speed.
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

        screen.fill(WHITE)
        screen.blit(background_image, background_image_rect)     
        for chip in chips:
            chip.update(delta_time)
            chip.draw()
        
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
                if COUNT_ANIM == 0:
                    #TODO
                    COUNT_ANIM = COUNT_ANIM + 1
                if COUNT_ANIM == 1:
                    # move chips from the board:
                    for chip in chips:
                        chip.move_back_to_start()
                    COUNT_ANIM = COUNT_ANIM + 1
                if COUNT_ANIM == 2:
                    chips = []
                    COUNT_ANIM = 0
                    model.plot_histogram()
                    model.start_new_game()            
        
        '''    
        for chip in chips:
            if not chip.in_animation:
                chip.move_back_to_start()
        '''
            
        screen.blit(board_image, board_rect)
        pygame.display.flip()

def run_gui():
    pygame.init()
    global chips
    chips = []
    init_game()
    gui_game(chips) 
    pygame.quit()

if __name__ == '__main__':
    run_gui()