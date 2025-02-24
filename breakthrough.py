import pygame
import sys
import math
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
# Global maze constants
GAP = 150  # vertical gap between walls
NUM_WALLS = (HEIGHT // GAP) + 2  # extra wall to ensure coverage
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Upward Gravity Maze Game")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

# Red dot (ball) settings
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2 - 50  # y remains constant

# Movement speeds
BALL_SPEED = 5
GRAVITY_SPEED = 2  # how much the maze moves upward per frame

# Create a simple maze as a list of pygame.Rect obstacles.
# Here we generate several horizontal walls evenly spaced.
def create_maze():
    walls = []
    wall_height = 1
    gap = 150  # vertical gap between walls
    y = gap
    while y < HEIGHT + gap:  # ensure enough walls to fill screen and a little extra
        #wall = pygame.Rect(50, y, 500, wall_height)
        #walls.append(wall)
        gap_location = random.randint(0, WIDTH - 100)
        wall_l = pygame.Rect(0, y, gap_location, wall_height)
        wall_r = pygame.Rect(gap_location + 100, y, WIDTH - gap_location - 100, wall_height)
        walls.append(wall_l)
        walls.append(wall_r)

        y += gap
    return walls

maze_walls = create_maze()

# Helper function to check collision between a circle and a rectangle.
def circle_rect_collision(cx, cy, radius, rect):
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    distance = math.hypot(cx - closest_x, cy - closest_y)
    return distance < radius

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key presses for left/right movement
    keys = pygame.key.get_pressed()
    old_ball_x = ball_x
    if keys[pygame.K_a]:
        ball_x -= BALL_SPEED
    if keys[pygame.K_d]:
        ball_x += BALL_SPEED
    for wall in maze_walls:
        if circle_rect_collision(ball_x, ball_y, BALL_RADIUS, wall):
            ball_x = old_ball_x
            break

    # Keep ball within the screen bounds horizontally
    if ball_x - BALL_RADIUS < 0:
        ball_x = BALL_RADIUS
    elif ball_x + BALL_RADIUS > WIDTH:
        ball_x = WIDTH - BALL_RADIUS

    # Check if moving the maze upward by GRAVITY_SPEED creates a collision with the ball.
    collision = False
    for wall in maze_walls:
        shifted_rect = wall.copy()
        shifted_rect.y -= GRAVITY_SPEED
        if circle_rect_collision(ball_x, ball_y, BALL_RADIUS, shifted_rect):
            collision = True
            break

    # Only apply gravity if no collision is detected
    if not collision:
        for wall in maze_walls:
            wall.y -= GRAVITY_SPEED

    # Recycle walls: if a wall has moved off the top, move it to the bottom.
    for wall in maze_walls:
        if wall.bottom < 0:
            wall.y = HEIGHT

    # Draw everything
    screen.fill(BLACK)

    # Draw maze walls
    for wall in maze_walls:
        pygame.draw.rect(screen, GRAY, wall)

    # Draw red ball (dot)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(60)