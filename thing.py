import pygame
import sys
import random
import math

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Explosion Effect")

# Define the list of colors
COLORS = [(255, 69, 0), (255, 165, 0), (255, 255, 0), (255, 255, 255), (255, 215, 0), (255, 140, 0), (255, 0, 0), (135, 206, 235)]

# Define the Particle class
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, size, angle, speed):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.color = random.choice(COLORS)
        pygame.draw.circle(self.image, self.color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(speed, 0).rotate(angle)
        self.pos = pygame.math.Vector2(pos)
        self.size = size
        self.alpha = 255

    def update(self):
        self.vel *= 0.95  # Air resistance
        self.vel.y += 0.1  # Gravity
        self.pos += self.vel
        self.rect.center = self.pos
        self.alpha -= 3  # Fade out
        if self.alpha < 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

# Define the Explosion class
class Explosion(pygame.sprite.Group):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.create_particles()

    def create_particles(self):
        for _ in range(300):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 10)
            size = random.randint(2, 8)
            particle = Particle(self.pos, size, angle, speed)
            self.add(particle)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    explosions = []

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Create explosion at mouse position
                explosion = Explosion(pygame.mouse.get_pos())
                explosions.append(explosion)

        for explosion in explosions[:]:
            explosion.update()
            explosion.draw(screen)
            if not explosion:
                explosions.remove(explosion)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
