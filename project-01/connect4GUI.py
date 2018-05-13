#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:35:15 2018

@author: Daniel Biskup
"""

import sys, pygame
import time
pygame.init()

size = width, height = 320, 240
size = width, height = 1366, 768
# fix window size

speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

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
            