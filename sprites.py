# This File was Created by: Tanish Yadlapalli
import pygame as pg
from settings import *

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((GREEN))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.speed = PLAYER_SPEED
        self.x = x * TILESIZE
        self.y = y * TILESIZE

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

    #check if hit 'grow' change by x2
    def collide_with_grow(self):
        checkCollision = pg.sprite.spritecollide(self, self.game.grow, True)
        if checkCollision:
            self.image = pg.Surface((self.rect.height * 2, self.rect.width * 2))
            self.image.fill((GREEN))
            self.rect.width = self.rect.width * 2
            self.rect.height = self.rect.height * 2
            #decrease speed, or set back to original
            self.speed = self.speed / 1.667
    
    #collide with shrink
    def collide_with_shrink(self):
        checkCollision = pg.sprite.spritecollide(self, self.game.shrink, True)
        if checkCollision:
            self.image = pg.Surface((self.rect.height / 2, self.rect.width / 2))
            self.image.fill((GREEN))
            self.rect.width = self.rect.width / 2
            self.rect.height = self.rect.height / 2
            #increase speed or set back to original
            self.speed = self.speed * 1.667
            

    #gets all key inputs
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed #PLAYER SPEED
            print(self.speed)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed #PLAYER SPEED
            print(self.speed)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed #PLAYER SPEED
            print(self.speed)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed #PLAYER SPEED
            print(self.speed)


    #old motion
    # def move(self, dx = 0, dy = 0):
    #     self.x += dx
    #     self.y += dy

    #updated update (new update)
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_grow()
        self.collide_with_shrink()

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
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = y
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE