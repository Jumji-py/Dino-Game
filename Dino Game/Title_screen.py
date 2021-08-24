import pygame
import random
import numpy as np
import sys
import os

from Enemies import Cactus, Bird

class Title_screen(object):
    def __init__(self, WIDTH, HEIGHT):
        self.logo = pygame.image.load(os.path.join("Assets", "logo.png"))
        self.logo_x = -self.logo.get_width()
        self.play = [pygame.image.load(
                        os.path.join("Assets", "play_text.png")),
                    pygame.image.load(
                        os.path.join("Assets", "play_text_clicked.png"))
                        ]
        self.play_x = -self.play[0].get_width()
        self.quit = [pygame.image.load(
                        os.path.join("Assets", "quit_text.png")),
                    pygame.image.load(
                        os.path.join("Assets", "quit_text_clicked.png"))
                        ]
        self.quit_x = -self.quit[0].get_width()
        self.intro_loaded = 0
        self.width, self.height = WIDTH, HEIGHT
        self.bgx, self.bgx2 = 0, WIDTH
        self.show_title_screen = True
        self.show_hitbox = False
        self.cacti = np.array([])
        self.birds = np.array([])

    def move(self, dino, ENEMY_VEL, DINO_HIT):
        dino.ai(self.cacti, self.birds)
        for one_cactus in self.cacti:
            one_cactus.move(dino, ENEMY_VEL, DINO_HIT)
            if one_cactus.x < (0 - one_cactus.width):
                self.cacti = np.delete(self.cacti, np.where(self.cacti == one_cactus))
        for one_bird in self.birds:
            one_bird.move(dino, ENEMY_VEL, DINO_HIT)
            if one_bird.x < (0 - one_bird.width):
                self.birds = np.delete(self.birds, np.where(self.birds == one_bird))

    def draw_title_screen(self, WIN, BG, dino):
        WIN.blit(BG, (self.bgx, 0))
        WIN.blit(BG, (self.bgx2, 0))

        for one_cactus in self.cacti:
            one_cactus.draw(WIN, self.show_hitbox)
        for one_bird in self.birds:
            one_bird.draw(WIN, self.show_hitbox)
        
        dino.draw(WIN, self.show_hitbox)

        if self.intro_loaded == 0:
            if self.logo_x >= 10:
                self.intro_loaded = 1
            else:
                self.logo_x += 5
        elif self.intro_loaded == 1:
            if self.play_x >= 10:
                self.intro_loaded = 2
            else:
                self.play_x += 5
        elif self.intro_loaded == 2:
            if self.quit_x >= 10:
                self.intro_loaded = 3
            else:
                self.quit_x += 5
        
        if self.intro_loaded == 3:
            WIN.blit(self.logo, (self.logo_x, 10))
            if self.play_x <= self.mouse[0] <= self.play_x + self.play[0].get_width() and  73 <= self.mouse[1] <= 73 + self.play[0].get_height():
                WIN.blit(self.play[1], (self.play_x, 73))
            else:
                WIN.blit(self.play[0], (self.play_x, 73))
            if self.quit_x <= self.mouse[0] <= self.quit_x + self.quit[0].get_width() and  133 <= self.mouse[1] <= 133 + self.quit[0].get_height():
                WIN.blit(self.quit[1], (self.quit_x, 133))
            else:
                WIN.blit(self.quit[0], (self.quit_x, 133))
        else:
            WIN.blit(self.logo, (self.logo_x, 10))
            WIN.blit(self.play[0], (self.play_x, 73))
            WIN.blit(self.quit[0], (self.quit_x, 133))

    def fade(self, dino, WIN, BG, ENEMY_VEL, DINO_HIT):
        fade = pygame.Surface((self.width, self.height))
        fade.fill((0, 0, 0))
        for alpha in range(0,300, 2):
            fade.set_alpha(alpha)
            self.move(dino, ENEMY_VEL, DINO_HIT)
            self.draw_title_screen(WIN, BG, dino)
            WIN.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

    def title_screen_window(self, SPAWN_ENTITIES, WIN, BG, dino, ENEMY_VEL, DINO_HIT, settings, distance):
        global run
        
        self.bgx -= 1
        self.bgx2 -= 1
        if self.bgx < self.width*-1:
            self.bgx = self.width+1
        if self.bgx2 < self.width*-1:
            self.bgx2 = self.width+1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                settings.save_data(distance)
                pygame.quit()
                sys.exit()
            
            if event.type == SPAWN_ENTITIES:
                x = random.randrange(0,5)
                if x == 1:
                    self.cacti = np.append(self.cacti, Cactus(self.width, 316, 24, 44))
                elif x == 2:
                    self.birds = np.append(self.birds, Bird(self.width, 327, 41, 38))
                elif x == 3:
                    self.birds = np.append(self.birds, Bird(self.width, 296, 41, 38))
                elif x == 4:
                    self.birds = np.append(self.birds, Bird(self.width, 270, 41, 38))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_x <= self.mouse[0] <= self.play_x + self.play[0].get_width() and  73 <= self.mouse[1] <= 73 + self.play[0].get_height():
                    self.show_title_screen = False
                if self.quit_x <= self.mouse[0] <= self.quit_x + self.quit[0].get_width() and  133 <= self.mouse[1] <= 133 + self.quit[0].get_height():
                    run = False
                    settings.save_data(distance)
                    pygame.quit()
                    sys.exit()
                

        self.mouse = pygame.mouse.get_pos()
        self.move(dino, ENEMY_VEL, DINO_HIT)

        if self.show_title_screen:
            self.draw_title_screen(WIN, BG, dino)
            pygame.display.update()
        else:
            self.fade(dino, WIN, BG, ENEMY_VEL, DINO_HIT)
            self.cacti = np.array([])
            self.birds = np.array([])