# This File was Created by: Tanish Yadlapalli
import pygame as pg
import random
from settings import *
from utils import *
import os
from os import path
import sys


game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'Spritesheet2.png'))
        self.load_images()
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.speed = PLAYER_SPEED
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 100
        self.moneybags = 0
        self.current_frame = 0
        self.last_update = 0

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x   
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_movable(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.movable, False)
        for hit in hits:
            if dir == 'x':
                if self.vx > 0:  # Moving right
                    while pg.sprite.spritecollide(self, self.game.movable, False):
                        hit.rect.left += 1
                elif self.vx < 0:  # Moving left
                    while pg.sprite.spritecollide(self, self.game.movable, False):
                        hit.rect.right -= 1
            elif dir == 'y':
                if self.vy > 0:  # Moving down
                    while pg.sprite.spritecollide(self, self.game.movable, False):
                        hit.rect.top += 1
                elif self.vy < 0:  # Moving up
                    while pg.sprite.spritecollide(self, self.game.movable, False):
                        hit.rect.bottom -= 1

    #collide with any group
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            #check what is being hit, what class (coin in this case).
            if str(hits[0].__class__.__name__) == "Coin":
                #increase coin count
                self.moneybags += 1
            
            #check for hit with Grow
            if str(hits[0].__class__.__name__) == "Grow":
                self.image = pg.Surface((self.rect.height * 2, self.rect.width * 2))
                self.image.fill((GREEN))
                self.rect.width = self.rect.width * 2
                self.rect.height = self.rect.height * 2
                #decrease speed, or set back to original
                self.speed = self.speed / 1.667
                
            #check for hit with shrink
            if str(hits[0].__class__.__name__) == "Shrink":
                self.image = pg.Surface((self.rect.height / 2, self.rect.width / 2))
                self.image.fill((GREEN))
                self.rect.width = self.rect.width / 2
                self.rect.height = self.rect.height / 2
                #increase speed, or set back to original
                self.speed = self.speed * 1.667
            
            #collide with enemy, die.
            if str(hits[0].__class__.__name__) == "Ghost":
                self.hitpoints -= 10
                if self.hitpoints == 0:
                    sys.exit()
            #collide with spike, die
            if str(hits[0].__class__.__name__) == "Gost":
                self.hitpoints -= 2.5
                if self.hitpoints == 0:
                    sys.exit()

    #gets all key inputs
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_e]:
            self.vx = -self.speed #PLAYER SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_f]:
            self.vx = self.speed #PLAYER SPEED
        if keys[pg.K_UP] or keys[pg.K_r]:
            self.vy = -self.speed #PLAYER SPEED
        if keys[pg.K_DOWN] or keys[pg.K_d]:
            self.vy = self.speed #PLAYER SPEED
        if keys[pg.K_v]:
            self.game.change_level(self.game.map)

    #updated update (new update)
    def update(self):
        self.get_keys()
        self.animate()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.collide_with_movable('x')
        self.collide_with_movable('y')
        self.collide_with_group(self.game.grow, True)
        self.collide_with_group(self.game.shrink, True)
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.ghost, False)
        self.collide_with_group(self.game.gost, False)

#write a wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class RightW(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallBR_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class DownW(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallBD_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class UpW(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallBU_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class LeftW(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wallBL_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
#class grow (same as wall)
class Grow(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grow
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grow_img
        self.rect = self.image.get_rect()
        self.x = y
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#make player shrink
class Shrink(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shrink
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shrink_img
        self.rect = self.image.get_rect()
        self.x = y
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ghost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.ghost_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 4
        
    def move(self):
        #pythag formula for making enemy
        self.distance_x = self.game.player.x - self.rect.x
        self.distance_y = self.game.player.y - self.rect.y
        self.distance = (self.distance_x ** 2 + self.distance_y ** 2) ** 0.5

        #make stop chasing
        if self.distance >= 250 or self.distance <= 5:
            self.speed = 0
        elif self.distance <= 200:
            self.speed = 4

        #make enemy "chase" player
        if self.distance != 0:
            self.rect.x += self.speed * self.distance_x / self.distance
            self.rect.y += self.speed * self.distance_y / self.distance

    def update(self):
        self.move()
        

#enemy type, pathfinding -- test (experimental)
class Gost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.gost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.gost_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Movable(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.movable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.movable_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    def update(self):
        self.x = self.rect.x
        self.y = self.rect.y