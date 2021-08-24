import pygame
import random
import os
import numpy as np
import sys

from Player import player
from Enemies import Cactus, Bird
from Settings import pause_play
from Title_screen import Title_screen

pygame.init()
pygame.font.init()

# Defining the window dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors used
BLACK = (0, 0, 0)

# All game constants:
FPS = 60
DISTANCE_FONT = pygame.font.Font(os.path.join("Assets", "COMIC.TTF"), 30)
GAME_OVER_FONT = pygame.font.Font(os.path.join("Assets", "COMIC.TTF"), 100)
# Character variables and images
DINO_WIDTH, DINO_HEIGHT = 40, 44
ENEMY_VEL = 4
BG = pygame.image.load(
    os.path.join("Assets", "background.png"))

title_screen = Title_screen(WIDTH, HEIGHT)
show_hitbox = False

# Setting the window caption and icon
pygame.display.set_caption("Dino Dash")
pygame.display.set_icon(pygame.image.load(os.path.join("Assets", "dino.png")))

# Redraw and update window display function
def draw_game(saved_data, dino, distance, settings, mouse):
    WIN.blit(BG, (bgx, 0))
    WIN.blit(BG, (bgx2, 0))

    if saved_data["High score"] == 0:
        distance_text = DISTANCE_FONT.render("Distance: " + str(round(distance)), 1, BLACK)
    else:
        distance_text = DISTANCE_FONT.render("HI: " + str(saved_data["High score"]) + "  Distance: " + str(round(distance)), 1, BLACK)
    WIN.blit(distance_text, (WIDTH - distance_text.get_width() - 10, 10))

    for one_cactus in cacti:
        one_cactus.draw(WIN, show_hitbox)
    for one_bird in birds:
        one_bird.draw(WIN, show_hitbox)
    
    dino.draw(WIN, show_hitbox)
    settings.draw_pause(WIN, mouse)

    pygame.display.update()
    
def set_allowed_events(SPAWN_ENTITIES, DINO_HIT):
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([
        pygame.QUIT,
        pygame.KEYDOWN,
        pygame.MOUSEBUTTONDOWN,
        SPAWN_ENTITIES,
        DINO_HIT
        ])

# Mainloop function
def main():
    
    global bgx, bgx2, cacti, birds, show_hitbox
    bgx = 0
    bgx2 = WIDTH

    cacti = np.array([])
    birds = np.array([])
    distance = 0
    hit_dino = False
    
    SPAWN_ENTITIES = pygame.USEREVENT+1
    pygame.time.set_timer(SPAWN_ENTITIES, random.randrange(1250, 3000))
    DINO_HIT = pygame.USEREVENT+2

    set_allowed_events(SPAWN_ENTITIES, DINO_HIT)

    # Creating the character Rect
    dino = player(110, 316, DINO_WIDTH, DINO_WIDTH)
    settings = pause_play(10, 10, 34, 34, WIDTH, HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        if title_screen.show_title_screen:
            title_screen.title_screen_window(SPAWN_ENTITIES, WIN, BG, dino, ENEMY_VEL, DINO_HIT, settings, distance)

        else:
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
                        settings.settings_window(WIN, distance, title_screen)
            
                if event.type == SPAWN_ENTITIES:
                    x = random.randrange(0,5)
                    if x == 1:
                        cacti = np.append(cacti, Cactus(WIDTH, 316, CACTUS_WIDTH, CACTUS_HEIGHT))
                    elif x == 2:
                        birds = np.append(birds, Bird(WIDTH, 327, 41, 38))
                    elif x == 3:
                        birds = np.append(birds, Bird(WIDTH, 296, 41, 38))
                    elif x == 4:
                        birds = np.append(birds, Bird(WIDTH, 270, 41, 38)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 10 <= mouse[0] <= settings.width + 10 and 10 <= mouse[1] <= settings.height + 10:
                        settings.settings_window(WIN, distance, title_screen)

                if event.type == DINO_HIT:
                    hit_dino = True

            if hit_dino:
                dino.draw_hit(WIN, GAME_OVER_FONT, BLACK, WIDTH, HEIGHT)
                break
            if settings.exit_game:
                break

            distance += 0.2

            keys_pressed = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            dino.move(keys_pressed)
            for one_cactus in cacti:
                one_cactus.move(dino, ENEMY_VEL, DINO_HIT)
                if one_cactus.x < (0 - one_cactus.width):
                    cacti = np.delete(cacti, np.where(cacti == one_cactus))
            for one_bird in birds:
                one_bird.move(dino, ENEMY_VEL, DINO_HIT)
                if one_bird.x < (0 - one_bird.width):
                    birds = np.delete(birds, np.where(birds == one_bird))

            draw_window(settings.saved_data, dino, distance, settings, mouse)
                                          
    settings.save_data(distance)               
    
    main()

if __name__ == "__main__":
    main()
