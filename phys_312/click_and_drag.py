import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Elastic Bouncing Balls')

# Colors
WHITE = (255, 255, 255)
BALL_COLOR = (0, 128, 255)

# Ball properties
num_balls = 20
balls = []
for _ in range(num_balls):
    # size = random.randint(10, 30)
    size = 10
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
    balls.append({'rect': pygame.Rect(x, y, size, size), 'velocity': velocity, 'size': size})

# Function to handle ball collisions
def handle_collisions():
    for i, ball in enumerate(balls):
        # Check for collisions with walls
        if ball['rect'].left < 0 or ball['rect'].right > width:
            ball['velocity'][0] = -ball['velocity'][0]
        if ball['rect'].top < 0 or ball['rect'].bottom > height:
            ball['velocity'][1] = -ball['velocity'][1]

        # Check for collisions with other balls
        for other_ball in balls[i+1:]:
            distance = pygame.math.Vector2(ball['rect'].center).distance_to(other_ball['rect'].center)
            if distance < ball['size'] + other_ball['size']:
                # Elastic collision
                m1, m2 = ball['size'], other_ball['size']
                v1, v2 = pygame.math.Vector2(ball['velocity']), pygame.math.Vector2(other_ball['velocity'])
                new_v1 = v1 - (2 * m2 / (m1 + m2)) * ((v1 - v2).dot(v1 - v2) / (v1 - v2).magnitude_squared()) * (v1 - v2)
                new_v2 = v2 - (2 * m1 / (m1 + m2)) * ((v2 - v1).dot(v2 - v1) / (v2 - v1).magnitude_squared()) * (v2 - v1)
                ball['velocity'], other_ball['velocity'] = new_v1, new_v2

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the balls
    for ball in balls:
        ball['rect'].x += ball['velocity'][0]
        ball['rect'].y += ball['velocity'][1]

    # Handle collisions
    handle_collisions()

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the balls
    for ball in balls:
        pygame.draw.circle(screen, BALL_COLOR, ball['rect'].center, ball['size'])

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(120)
