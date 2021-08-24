import pygame
import os
import sys
import json

pygame.font.init()

class Settings(object):

    def __init__(self, x, y, width, height, WIDTH, HEIGHT):
        self.PLAY_B = pygame.image.load(os.path.join("Assets", "play_b.png"))
        self.PLAY_BCLICKED = pygame.image.load(os.path.join("Assets", "play_bclicked.png"))
        self.PAUSE_B = pygame.image.load(os.path.join("Assets", "pause_b.png"))
        self.PAUSE_BCLICKED = pygame.image.load(os.path.join("Assets", "pause_bclicked.png"))
        self.EXIT_B = pygame.image.load(os.path.join("Assets", "exit_b.png"))
        self.EXIT_BCLICKED = pygame.image.load(os.path.join("Assets", "exit_bclicked.png"))
        self.SETTINGS_WINDOW = pygame.image.load(os.path.join("Assets", "settings_window.png"))
        self.SETTINGS_WIDTH, self.SETTINGS_HEIGHT = 404, 326
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.SETTINGS_X = WIDTH//2 - self.SETTINGS_WIDTH//2
        self.SETTINGS_Y = HEIGHT//2 - self.SETTINGS_HEIGHT//2
        self.COUNT_FONT = pygame.font.Font(os.path.join("Assets", "COMIC.TTF"), 100)
        self.exit_game = False
        with open("Settings.json") as data:
            self.saved_data = json.load(data)
            
    def save_data(self, distance):
        if distance > self.saved_data["High score"]:
            self.saved_data["High score"] = round(distance)
            with open("Settings.json", "w") as store_data:
                json.dump(self.saved_data, store_data, indent=4, sort_keys=False)

    def draw_pause(self, WIN, mouse):
        if 10 <= mouse[0] <= self.width + 10 and 10 <= mouse[1] <= self.height + 10:
            WIN.blit(self.PAUSE_BCLICKED, (self.x, self.y))
        else:
            WIN.blit(self.PAUSE_B, (self.x, self.y))
            
    def draw_settings(self, WIN, mouse):
        if 10 <= mouse[0] <= self.width + 10 and 10 <= mouse[1] <= self.height + 10:
            WIN.blit(self.PAUSE_BCLICKED, (self.x, self.y))
        else:
            WIN.blit(self.PAUSE_B, (self.x, self.y))
        
        WIN.blit(self.SETTINGS_WINDOW, (self.SETTINGS_X, self.SETTINGS_Y))
        
        if (self.SETTINGS_X + 148 <= mouse[0] <= self.width + self.SETTINGS_X + 148) and (self.SETTINGS_Y + 146 <= mouse[1] <= self.height + self.SETTINGS_Y + 146):
            WIN.blit(self.PLAY_BCLICKED, (self.SETTINGS_X + 148, self.SETTINGS_Y + 146))
        else:
            WIN.blit(self.PLAY_B, (self.SETTINGS_X + 148, self.SETTINGS_Y + 146))

        if (self.SETTINGS_X + 222 <= mouse[0] <= self.width + self.SETTINGS_X + 222) and (self.SETTINGS_Y + 146 <= mouse[1] <= self.height + self.SETTINGS_Y + 146):
            WIN.blit(self.EXIT_BCLICKED, (self.SETTINGS_X + 222, self.SETTINGS_Y + 146))
        else:
            WIN.blit(self.EXIT_B, (self.SETTINGS_X + 222, self.SETTINGS_Y + 146))
            
    def timer(self, WIN):
        for count_down in range(3, 0, -1):
            WIN.blit(self.PAUSE_B, (self.x, self.y))
            WIN.blit(self.SETTINGS_WINDOW, (self.SETTINGS_X, self.SETTINGS_Y))
            WIN.blit(self.PLAY_B, (self.SETTINGS_X + 148, self.SETTINGS_Y + 146))
            WIN.blit(self.EXIT_B, (self.SETTINGS_X + 222, self.SETTINGS_Y + 146))
            counter = self.COUNT_FONT.render(str(count_down), 1, (0, 0, 0))
            WIN.blit(counter, (450 - counter.get_width()//2, 250 - counter.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
        
    def settings_window(self, WIN, distance, title_screen):
        settings_run = True
        while settings_run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_data(distance)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.SETTINGS_X + 148 <= mouse[0] <= self.width + self.SETTINGS_X + 148) and (self.SETTINGS_Y + 146 <= mouse[1] <= self.height + self.SETTINGS_Y + 146):
                        settings_run = False
                        self.timer(WIN)
                    if (self.SETTINGS_X + 222 <= mouse[0] <= self.width + self.SETTINGS_X + 222) and (self.SETTINGS_Y + 146 <= mouse[1] <= self.height + self.SETTINGS_Y + 146):
                        settings_run = False
                        title_screen.show_title_screen = True
                        self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        settings_run = False
                        self.timer(WIN)

            mouse = pygame.mouse.get_pos()
            self.draw_settings(WIN, mouse)

            pygame.display.update()
