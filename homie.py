import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Explosion Simulation")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)

# Particle class
class Particle:
    def __init__(self, x, y, size, color, speed, direction):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.direction = direction
        self.gravity = 0.1  # Apply gravity for a realistic arc motion
        self.time_to_live = random.randint(30, 60)  # Lifetime of the particle

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction) + self.gravity
        self.size -= 0.2  # Reduce size over time
        self.time_to_live -= 1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), max(0, int(self.size)))

# Explosion function
def explode(x, y):
    particles = []
    particle_count = 200
    for _ in range(particle_count):
        size = random.randint(2, 12)
        color = random.choice([YELLOW, ORANGE, RED, DARK_RED])
        speed = random.uniform(0.5, 2.5)
        direction = random.uniform(0, 2 * math.pi)
        particles.append(Particle(x, y, size, color, speed, direction))
    return particles

# Main function
def main():
    running = True
    clock = pygame.time.Clock()
    particles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Explode on mouse click
        if pygame.mouse.get_pressed()[0]:
            explosion_center = pygame.mouse.get_pos()
            particles.extend(explode(*explosion_center))

        # Update and draw particles
        for particle in particles:
            particle.move()
            particle.draw()

        # Remove particles that have expired
        particles = [particle for particle in particles if particle.time_to_live > 0]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()