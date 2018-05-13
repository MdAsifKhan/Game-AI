#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:35:15 2018

@author: Daniel Biskup
"""

import sys, pygame
import time
import connect4class
pygame.init()

size = width, height = 320, 240
size = width, height = 1366, 768
# fix window size

speed = [2, 2]
black = 0, 0, 0
white = 1, 1, 1

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

model = connect4class.connect4class()

# Show splash screen:
splash_screen = pygame.image.load("splash_screen.jpg")
splash_screen_rect = splash_screen.get_rect()
splash_screen_rect.center = (width/2, height/2)
screen.fill(white)
screen.blit(splash_screen, splash_screen_rect)
pygame.display.flip()
time.sleep(2)

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

    screen.fill(black)
#    screen.blit(ball, ballrect)
    pygame.display.flip()
 
pygame.quit()
            