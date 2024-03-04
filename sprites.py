# This File was Created by: Tanish Yadlapalli
import pygame as pg
import random
from settings import *

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img
        # self.image.fill((GREEN))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.speed = PLAYER_SPEED
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybags = 0

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

    #gets all key inputs
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed #PLAYER SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed #PLAYER SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed #PLAYER SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed #PLAYER SPEED

    #updated update (new update)
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.grow, True)
        self.collide_with_group(self.game.shrink, True)
        self.collide_with_group(self.game.coins, True)

#write a wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass

#class grow (same as wall)
class Grow(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grow
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
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
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
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
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 7
        
    def move(self):
        #pythag formula for making enemy
        distance_x = self.game.player.x - self.rect.x
        distance_y = self.game.player.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if distance >= 350:
            self.speed = 0
        elif distance <= 200:
            self.speed = 7

        #make enemy "chase" player
        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance

    def update(self):
        self.move()