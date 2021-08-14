import pygame
import os
import sys

class pause_play(object):

    def __init__(self, x, y, width, height, WIDTH, HEIGHT):
        self.PLAY_B = pygame.image.load(os.path.join("Assets", "play_b.png"))
        self.PLAY_BCLICKED = pygame.image.load(os.path.join("Assets", "play_bclicked.png"))
        self.PAUSE_B = pygame.image.load(os.path.join("Assets", "pause_b.png"))
        self.PAUSE_BCLICKED = pygame.image.load(os.path.join("Assets", "pause_bclicked.png"))
        self.SETTINGS_PLAY_B = pygame.image.load(os.path.join("Assets", "settings_play_b.png"))
        self.SETTINGS_PLAY_BCLICKED = pygame.image.load(os.path.join("Assets", "settings_play_bclicked.png"))
        self.SETTINGS_WIDTH, self.SETTINGS_HEIGHT = 202, 163
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.SETTINGS_X = WIDTH//2 - self.SETTINGS_WIDTH//2
        self.SETTINGS_Y = HEIGHT//2 - self.SETTINGS_HEIGHT//2

        
    def draw_pause(self, WIN, mouse):
        if 10 <= mouse[0] <= self.width + 10 and 10 <= mouse[1] <= self.height + 10:
            WIN.blit(self.PAUSE_BCLICKED, (self.x, self.y))
        else:
            WIN.blit(self.PAUSE_B, (self.x, self.y))
        
    def settings_window(self, WIN):
        settings_run = True
        while settings_run == True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.SETTINGS_X + 82 <= mouse[0] < self.SETTINGS_X + 82 + self.width and self.SETTINGS_Y + 60 <= mouse[1] < self.SETTINGS_X + 60 + self.height:
                        settings_run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        settings_run = False

            mouse = pygame.mouse.get_pos()
            if (self.SETTINGS_X + 82) <= mouse[0] <= (self.SETTINGS_X + 82 + self.width) and (self.SETTINGS_Y + 60) <= mouse[1] <= (self.SETTINGS_Y + 60 + self.height):
                WIN.blit(self.SETTINGS_PLAY_BCLICKED, (self.SETTINGS_X, self.SETTINGS_Y))
            else:
                WIN.blit(self.SETTINGS_PLAY_B, (self.SETTINGS_X, self.SETTINGS_Y))

            pygame.display.update()