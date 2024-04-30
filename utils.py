import pygame as pg
from random import *
from settings import *

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        # use code below if scaling is necessary
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    
class Particle(pg.sprite.Sprite):
    def __init__(self, game, pos, color, radius):
        self.groups = game.all_sprites, game.particles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.radius = radius
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)  # Make the surface transparent
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = pg.math.Vector2(random.uniform(-2, 5), random.uniform(-3, 6))  # Random initial velocity
        self.pos = pg.math.Vector2(pos)
        self.size_decay_rate = 0.1  # Rate at which size decreases over time
        self.alpha_decay_rate = 2  # Rate at which alpha decreases over time

        # Draw a circle on the surface
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

    def update(self):
        # Apply gravity
        self.vel.y += 0.1  # Adjust gravity strength as needed

        # Update position
        self.pos += self.vel
        self.rect.center = self.pos

        # Fade out and decrease size
        self.image.set_alpha(max(0, self.image.get_alpha() - self.alpha_decay_rate))
        self.radius = max(0, self.radius - self.size_decay_rate)
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        # Kill particle if it becomes too small or completely transparent
        if self.image.get_alpha() <= 0:
            self.kill()
        
        self.vx = self.vel.x
        self.vy = self.vel.y

        
