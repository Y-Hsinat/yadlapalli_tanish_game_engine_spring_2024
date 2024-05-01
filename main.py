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
from time import *
import sys
import os
from os import path
import random

"""
Goals:
Get more graphics.
Randomized Maps 
Get Border (sprites facing the right way, facing inward)

BETA Goals:
Gameplay goal: Changing Levels
(Maybe) Add more puzzle-based powerups (like something that allows you to move blocks, etc.)
Secondary Goals: repurpose ghost into static 'spike,' get small and enlarge powerup working.
"""

#draws health bar above player
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    #length of bar, visual representation of health
    BAR_LENGTH = 250
    BAR_HEIGHT = 35
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
        #map, current map

    #load data method
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'images')
        self.map_folder = path.join(game_folder, 'maps')
        self.map_data = []
        self.current_map = 0
        self.map = str(os.listdir(self.map_folder)[self.current_map])
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
        self.gost_img = pg.image.load(path.join(img_folder, 'gost.png')).convert_alpha()
        self.movable_img = pg.image.load(path.join(img_folder, 'Movable.png')).convert_alpha()
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''

        #create map from file
        with open(path.join(self.game_folder, self.map_folder, self.map), 'rt') as f:
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
        self.movable = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.particles = pg.sprite.Group()
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
                if tile == '%':
                    Movable(self, col, row)

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
        if self.player.moneybags == 9:
            self.current_map += 1
            self.map = str(os.listdir(self.map_folder)[self.current_map])
            self.change_level(self.map)
            
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
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        draw_health_bar(self.screen, 27, 10, self.player.hitpoints)
        pg.display.flip()

    #events, and checks if we clicked 'X'
    def events(self):
        for event in pg.event.get():
            #Hit X: Game Closes.
            if event.type == pg.QUIT:
                self.quit()
                print("GAME HAS ENDED")
    
    def change_level(self, lvl):
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(game_folder, 'maps')
        #remove everything from screen
        for s in self.all_sprites:
            s.kill()
        # make sure that money is 0; levels work
        self.player.moneybag = 0
        # set self.map data to 0
        self.map_data = []
        with open(path.join(self.game_folder, self.map_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # put things on screen
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
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
                #spawn movable
                if tile == '%':
                    Movable(self, col, row)

    def die(self):
        self.change_level("map.txt")
        self.current_map = 0
        
##############Calling Class "Game"/Instantiating Game#############
g = Game()
# g.show_go_screen()
while True:
    g.new() 
    g.run()
    # go.show_go_screen()
