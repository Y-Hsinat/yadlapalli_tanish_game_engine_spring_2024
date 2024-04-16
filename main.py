# This file was created by: Tanish Yadlapalli

# Sources/Credits:
# Mr. Cozort's Repository: https://github.com/ccozort/cozort_chris_game_engine_Spring_2024
# Makeuseof's Pygame Player-Following Algorithm: https://www.makeuseof.com/pygame-move-enemies-different-ways/#:~:text=To%20move%20the%20enemy%20toward,and%20direction%20toward%20the%20player.
# Pygame Documentation: https://www.pygame.org/docs/ref/draw.html 

##################Import Libraries and Files##################

import pygame as pg
from settings import *
from utils import *
from sprites import *
import sys
import os
from os import path
from random import randint

"""
Goals:
Get more graphics.
Randomized Maps 
Get Border (sprites facing the right way, facing inward)

BETA Goals:
Gameplay goal: Add more puzzle-based powerups (like something that allows you to move blocks, etc.)
Secondary Goals: repurpose ghost into static 'spike,' get small and enlarge powerup working.
"""

#draws health bar above player
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    #length of bar, visual representation of health
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    #white outline
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    #actually draws the health bar and stuff.
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

######################Create Game Class#######################

class Game:
    #Initialize Class Game
    def __init__(self):
        #initalize pygame
        pg.init()
        # Create Window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # Set Window Name to "Gaem."
        pg.display.set_caption("GeAM")
        # Get time
        self.clock = pg.time.Clock()
        #Set Running & Playing to True
        pg.key.set_repeat(500, 100)
        self.running = True
    #load data into and from, game
        self.load_data()

    #load data method
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map_data = []
        self.map = str(random.choice(os.listdir("maps")))
        self.player_img = pg.image.load(path.join(img_folder, 'thing.png')).convert_alpha()
        self.wallBD_img = pg.image.load(path.join(img_folder, 'Border_Down.png')).convert_alpha()
        self.wallBU_img = pg.image.load(path.join(img_folder, 'Border_Up.png')).convert_alpha()
        self.wallBL_img = pg.image.load(path.join(img_folder, 'Border_Left.png')).convert_alpha()
        self.wallBR_img = pg.image.load(path.join(img_folder, 'Border_Right.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'Wall.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.ghost_img = pg.image.load(path.join(img_folder, 'Ghost.png')).convert_alpha()
        self.shrink_img = pg.image.load(path.join(img_folder, 'Shrink.png')).convert_alpha()
        self.grow_img = pg.image.load(path.join(img_folder, 'Grow.png')).convert_alpha()
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''

        #create map from file
        with open(path.join(game_folder, map_folder, self.map), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
  

                
    #create everything, add player to 'all_sprites'
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grow = pg.sprite.Group()
        self.shrink = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.ghost = pg.sprite.Group()
        self.gost = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                #create walls if tile is one
                if tile == '#':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                #down border wall
                if tile == "d":
                    DownW(self, col, row)
                #right border wall
                if tile == "r":
                    RightW(self, col, row)
                #left border wall
                if tile == "l":
                    LeftW(self, col, row)
                #up border wall
                if tile == "u":
                    UpW(self, col, row)
                #spawn "Player"
                if tile == 'p':
                    self.player = Player(self, col, row)
                #spawn grow
                if tile == '>':
                    Grow(self, col, row)
                #spawn shrink
                if tile == '<':
                    Shrink(self, col, row)
                #spawn coin
                if tile == 'c':
                    print("coin at", row, col)
                    Coin(self, col, row)
                #spawn enemy
                if tile == 'g':
                    Ghost(self, col, row)
                #spawn pathfinding ;gost;
                if tile == ';':
                    Gost(self, col, row)

    #Run methods, causes the game to work.
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            #input, process, and output respectively. IPOS Model.
            self.events()
            self.update()
            self.draw()

    #quit method, exits game
    def quit(self):
        pg.quit()
        sys.exit()

    # methods
    def input(self):
        pass

    #updates all sprites
    def update(self):
        self.all_sprites.update()

    #draws the grid over screen
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0,), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    #draw text to the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('Consolas')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE,y * TILESIZE)
        surface.blit(text_surface, text_rect)

    #draws the acutal grid & backg
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybags), 48, WHITE, 1, 1)
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y - 15, self.player.hitpoints)
        pg.display.flip()

    #events, and checks if we clicked 'X'
    def events(self):
        for event in pg.event.get():
            #Hit X: Game Closes.
            if event.type == pg.QUIT:
                self.quit()
                print("GAME HAS ENDED")

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass            

##############Calling Class "Game"/Instantiating Game#############
g = Game()
# g.show_go_screen()
while True:
    g.new() 
    g.run()
    # go.show_go_screen()
