import pygame
import sys
import random
import math

# Constants
WIDTH = 1500
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RADIUS = 7
SPEED = 3
VECTOR_SCALE = 0  # Factor to scale the velocity vector

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Particle class
class Particle:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        self.angle = angle  # Angle of velocity vector
        self.speed = SPEED
        self.vector_length = self.speed * 5  # Length of velocity vector

    def draw(self):
        # Draw particle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), RADIUS)
        # Draw velocity vector
        dx = self.vector_length * math.cos(self.angle)
        dy = self.vector_length * math.sin(self.angle)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + dx, self.y + dy), 2)

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

# Create particles with equal masses
particles = []
num_particles = 300
for i in range(num_particles):
    angle = random.uniform(0, 2*math.pi)  # Random initial angle
    particle = Particle(random.randint(RADIUS, WIDTH - RADIUS), random.randint(RADIUS, HEIGHT - RADIUS), angle)
    particles.append(particle)

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update particles
    for particle in particles:
        particle.update()

    # Check collision with walls
    for particle in particles:
        if particle.x <= RADIUS or particle.x >= WIDTH - RADIUS:
            particle.angle = math.pi - particle.angle

        if particle.y <= RADIUS or particle.y >= HEIGHT - RADIUS:
            particle.angle = -particle.angle

    # Check collision between particles
    for i, particle in enumerate(particles):
        for other_particle in particles[i + 1:]:
            distance = math.sqrt((particle.x - other_particle.x)**2 + (particle.y - other_particle.y)**2)
            if distance <= 2 * RADIUS:
                # Adjust angles to simulate elastic collision
                angle_diff = particle.angle - other_particle.angle
                particle.angle -= angle_diff
                other_particle.angle += angle_diff

    # Draw particles
    for particle in particles:
        particle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
