import pygame
import random
import os
import numpy as np
import sys

from Player import player
from Enemies import Cactus, Bird
from Settings import pause_play

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Defining the window dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors used
BLACK = (0, 0, 0)

# Sound effects
JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "jump.mp3"))

# All game constants:
FPS = 60
DISTANCE_FONT = pygame.font.Font(os.path.join("Assets", "COMIC.TTF"), 40)
GAME_OVER_FONT = pygame.font.Font(os.path.join("Assets", "COMIC.TTF"), 100)
# Character variables and images
DINO_WIDTH, DINO_HEIGHT = 40, 44 # Dimensions of dino
CACTUS_WIDTH, CACTUS_HEIGHT = 24,44
BIRD_WIDTH, BIRD_HEIGHT = 41,38
ENEMY_VEL = 4
BG = pygame.image.load(
    os.path.join("Assets", "background.png"))

show_hitbox = False

pygame.time.set_timer(pygame.USEREVENT+1, random.randrange(1000, 2000))
DINO_HIT = pygame.USEREVENT+2

# Setting the window caption and icon
pygame.display.set_caption("Dino Game")

# Redraw and update window display function
def draw_window(dino, distance, settings, mouse):
    WIN.blit(BG, (bgx, 0))
    WIN.blit(BG, (bgx2, 0))

    distance_text = DISTANCE_FONT.render("Distance: " + str(round(distance)), 1, BLACK)
    WIN.blit(distance_text, (WIDTH - distance_text.get_width() - 10, 10))

    for one_cactus in cacti:
        one_cactus.draw(WIN, show_hitbox)
    for one_bird in birds:
        one_bird.draw(WIN, show_hitbox)
    
    dino.draw(WIN, show_hitbox)
    settings.draw_pause(WIN, mouse)

    pygame.display.update()

# Mainloop function
def main():
    
    global bgx, bgx2, cacti, birds, show_hitbox
    bgx = 0
    bgx2 = WIDTH

    cacti = np.array([])
    birds = np.array([])
    distance = 0
    hit_dino = False

    # Creating the character Rect
    dino = player(110, 316, DINO_WIDTH, DINO_WIDTH)
    settings = pause_play(10, 10, 34, 34, WIDTH, HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        bgx -= 1
        bgx2 -= 1
        if bgx < WIDTH*-1:
            bgx = WIDTH+1
        if bgx2 < WIDTH*-1:
            bgx2 = WIDTH+1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    if show_hitbox:
                        show_hitbox = False
                    else:
                        show_hitbox = True

                if event.key == pygame.K_p:
                    settings.settings_window(WIN)
            
            if event.type == pygame.USEREVENT+1:
                x = random.randrange(0,3)
                if x == 1:
                    cacti = np.append(cacti, Cactus(WIDTH, 316, CACTUS_WIDTH, CACTUS_HEIGHT))
                elif x == 0:
                    birds = np.append(birds, Bird(WIDTH, 270, BIRD_WIDTH, BIRD_HEIGHT))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= settings.width + 10 and 10 <= mouse[1] <= settings.height + 10:
                    settings.settings_window(WIN)

            if event.type == pygame.USEREVENT+2:
                hit_dino = True

        if hit_dino:
            dino.draw_hit(WIN, GAME_OVER_FONT, BLACK, WIDTH, HEIGHT)
            break

        distance += 0.2

        keys_pressed = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        dino.move(keys_pressed, JUMP_SOUND)
        for one_cactus in cacti:
            one_cactus.move(dino, ENEMY_VEL, DINO_HIT, cacti)
        for one_bird in birds:
            one_bird.move(dino, ENEMY_VEL, DINO_HIT, birds)

        draw_window(dino, distance, settings, mouse)
    
    main()

if __name__ == "__main__":
    main()