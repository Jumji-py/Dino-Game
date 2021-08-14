import pygame
import numpy as np
import os
from pygame.rect import Rect

class player(object):
    
    DINO_RUNNING = [
    pygame.image.load(
        os.path.join("Assets", "dino_back_leg_up.png")),
    pygame.image.load(
        os.path.join("Assets", "dino_front_leg_up.png"))]
    DINO_CHAR = pygame.image.load(
        os.path.join("Assets", "dino.png"))
    DINO_HIT = pygame.image.load(
        os.path.join("Assets", "dino_hit.png"))
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 30
        self.running = True
        self.runCount = 0
        self.hitBoxs = np.array([
            Rect(self.x + 10, self.y + 36, 14, 8), # Legs
            Rect(self.x + 20, self.y, 20, 14), # Head
            Rect(self.x + 28, self.y + 18, 4, 4), # Hand
            Rect(self.x, self.y + 14, 28, 22), # Body
            ])

    def draw(self, WIN, show_hitbox):
        if self.runCount + 1 >= 20:
            self.runCount = 0
        if self.running:
            WIN.blit(self.DINO_RUNNING[self.runCount//10], (self.x, self.y))
            self.runCount += 1
        else:
            WIN.blit(self.DINO_CHAR, (self.x, self.y))
        self.hitBoxs = np.array([
            Rect(self.x + 10, self.y + 36, 14, 8), # Legs
            Rect(self.x + 20, self.y, 20, 14), # Head
            Rect(self.x + 28, self.y + 18, 4, 4), # Hand
            Rect(self.x, self.y + 14, 28, 22), # Body
            ])
        if show_hitbox:
            for hitBox in self.hitBoxs:
                pygame.draw.rect(WIN, (255, 0, 0), hitBox, 2)

    def move(self, keys_pressed, jump_sound):
        if not self.isJump:
            self.running = True
            if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP]:
                self.isJump = True
                self.running = False
                self.runCount = 0
                jump_sound.play()
        else:
            self.jumpCount -= 1
            if self.jumpCount >= -30:
                self.y = 316 - (round(((pow(self.jumpCount, 2)) * (-25/432)) + 52 + (1/12)))
                if -6 <= self.jumpCount <= 6:
                    self.y = 316 - 50
            else:
                self.isJump = False
                self.jumpCount = 30

    def draw_hit(self, WIN, GAME_OVER_FONT, BLACK, WIDTH, HEIGHT):
        game_over_text = GAME_OVER_FONT.render("GAME OVER!", 1, BLACK)
        WIN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))

        pygame.display.update()
        pygame.time.delay(2000)