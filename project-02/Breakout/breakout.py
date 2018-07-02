# -*- coding: utf-8 -*-

#!/usr/bin/env python

import numpy as np
import pygame
from pygame.locals import *
import sys
import time
from breakout_sprites import *
import matplotlib.pyplot as plt


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

if __name__ == '__main__':

    games = 100
    games_won = 0
    total_time = 0

    #Play game for 100 times
    for i in range (0, games):       
        # game init
        pygame.init()
        white = (255, 255, 255)
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout')
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        background_image = pygame.image.load('images/background.png').convert()    
        sound = pygame.mixer.Sound('audio/beep.wav')
        score = 0
        start_time = pygame.time.get_ticks()
        start = start_time
        
        # groups
        all_sprites_group = pygame.sprite.Group()
        player_bricks_group = pygame.sprite.Group()
        bricks_group = pygame.sprite.Group()
        
        # add sprites to their group
        ball = Ball('ball.png', BALL_SPEED, -BALL_SPEED)
        all_sprites_group.add(ball)
        
        player = Player('player.png', BALL_SPEED)
        all_sprites_group.add(player)
        player_bricks_group.add(player)
        
        for i in range(8):
            for j in range(8):
                brick = Brick('brick.png', (i+1)*BRICK_WIDTH + 5, (j+3)*BRICK_HEIGHT + 5)
                all_sprites_group.add(brick)
                bricks_group.add(brick)
                player_bricks_group.add(brick)
         
        # game loop
        while True:
            # game over if ball falls down
            if ball.rect.y > WINDOW_HEIGHT:  
                print('Game Over')
                message_display('Game Over')
                score = 0
                game_time = (pygame.time.get_ticks()-start)/1000
                total_time += game_time
                break
            
            # exit pygame if user closes the window
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            # player wins if all bricks can be broken
            if score == 64:
                print('You Win')
                message_display('You Win')
                games_won += 1
                game_time = (pygame.time.get_ticks()-start)/1000
                total_time += game_time
                break
        
            # collision detection (ball bounce against brick & player)
            hits = pygame.sprite.spritecollide(ball, player_bricks_group, False)
            if hits:
                sound.play()
                hit_rect = hits[0].rect
                # bounce the ball (according to side collided)
                if hit_rect.left > ball.rect.left or ball.rect.right < hit_rect.right:
                    ball.speed_y *= -1
                else:
                    ball.speed_x *= -1
        
                # collision with blocks
                if pygame.sprite.spritecollide(ball, bricks_group, True):
                    score += len(hits)
                    print("Score: %s" % score)   
                    
            # accelerate ball speed with time (in 15 seconds intervals)
            current_time = pygame.time.get_ticks()
            if (current_time-start_time>15000):
                ball.speed_x *= 2
                ball.speed_y *= 2
                start_time = current_time
            
            # move player horizontally
            player.move(ball.speed_x)
                    
            # render background image
            screen.blit(background_image, [0, 0])
            
            # render groups
            all_sprites_group.draw(window)
            
            # refresh screen
            all_sprites_group.update()
            clock.tick(60)
            pygame.display.flip()

    # quit pygame
    pygame.quit()
    #sys.exit()
            
    print("Number of Games Won: ", games_won)
    print("Average game time: ", total_time/games, "seconds")

    #Plot a histogram of games played vs games won
    plt.title("Frequency of games played vs games won")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.bar(-1, games, width=0.2, align='center', label="Played")
    plt.bar(1, games_won, width=0.2, align='center',label="Won")
    plt.legend(loc='upper center')
    plt.show()