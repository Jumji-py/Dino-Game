import pygame
import numpy as np
import os
from pygame.rect import Rect

class Cactus(object):
    def __init__(self, x, y, width, height):
        self.CACTUS_IMAGE = pygame.image.load(
            os.path.join("Assets", "cactus.png"))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitBox = np.array([
            Rect(self.x + 7, self.y, 10, 44),
            Rect(self.x, self.y + 11, 8, 22),
            Rect(self.x + 16, self.y + 6, 8, 21)
            ])

    def draw(self, WIN, show_hitbox):
        WIN.blit(self.CACTUS_IMAGE, (self.x, self.y))
        self.hitBox = np.array([
            Rect(self.x + 7, self.y, 10, 44),
            Rect(self.x, self.y + 11, 8, 22),
            Rect(self.x + 16, self.y + 6, 8, 21)
            ])
        if show_hitbox:
            for chitBox in self.hitBox:
                pygame.draw.rect(WIN, (255, 0, 0), chitBox, 2)

    def move(self, dino, ENEMY_VEL, DINO_HIT):
        self.x -= ENEMY_VEL
        if dino.ducking:
            for chitBox in self.hitBox:
                if Rect(dino.duck_hitbox).colliderect(chitBox):
                    pygame.event.post(pygame.event.Event(DINO_HIT))
        else:
            for hitBox in dino.hitBoxs:
                for chitBox in self.hitBox:
                    if Rect(hitBox).colliderect(Rect(chitBox)):
                        pygame.event.post(pygame.event.Event(DINO_HIT))

class Bird(object):
    BIRD = [pygame.image.load(os.path.join("Assets", "bird_up.png")), pygame.image.load(os.path.join("Assets", "bird_down.png"))]

    def __init__(self, x, y, BIRD_WIDTH, BIRD_HEIGHT):
        self.x = x
        self.y = y
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.flyCount = 0
        self.hitBox = np.array([
            Rect(self.x, self.y, 41, 25),
            Rect(self.x, self.y + 10, 41, 19),
            Rect(self.x + 16, self.y + 29, 8, 9)
            ])

    def draw(self, WIN, show_hitbox):
        if self.flyCount + 1 >= 30:
            self.flyCount = 0
        if True:
            WIN.blit(self.BIRD[self.flyCount//15], (self.x, self.y))
            self.flyCount += 1
        self.hitBox = np.array([
            Rect(self.x, self.y, 41, 25),
            Rect(self.x, self.y + 10, 41, 19),
            Rect(self.x + 16, self.y + 29, 8, 9)
            ])
        if show_hitbox:
            if not self.flyCount//15:
                pygame.draw.rect(WIN, (255, 0, 0), self.hitBox[0], 2)
            else:
                pygame.draw.rect(WIN, (255, 0, 0), self.hitBox[1], 2)
                pygame.draw.rect(WIN, (255, 0, 0), self.hitBox[2], 2)

    def move(self, dino, ENEMY_VEL, DINO_HIT):
        self.x -= ENEMY_VEL
        if dino.ducking:
            if self.flyCount//15:
                if Rect(dino.duck_hitbox).colliderect(self.hitBox[1]) or Rect(dino.duck_hitbox).colliderect(self.hitBox[2]):
                    pygame.event.post(pygame.event.Event(DINO_HIT))
            else:
                if Rect(dino.duck_hitbox).colliderect(self.hitBox[0]):
                    pygame.event.post(pygame.event.Event(DINO_HIT))
        else:
            for hitBox in dino.hitBoxs:
                if self.flyCount//15:
                    if Rect(hitBox).colliderect(self.hitBox[1]) or Rect(hitBox).colliderect(self.hitBox[2]):
                        pygame.event.post(pygame.event.Event(DINO_HIT))
                else:
                    if Rect(hitBox).colliderect(self.hitBox[0]):
                        pygame.event.post(pygame.event.Event(DINO_HIT))
