import pygame
import sys
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Upward Gravity Maze Game")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

clock = pygame.time.Clock()

# Red dot (ball) settings
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2  # y remains constant

# Movement speeds
BALL_SPEED = 5
GRAVITY_SPEED = 2  # how much the maze moves upward per frame

# Create a simple maze as a list of pygame.Rect obstacles
def create_maze():
    walls = []
    # Horizontal walls
    walls.append(pygame.Rect(50, 50, 500, 20))
    walls.append(pygame.Rect(50, 530, 500, 20))


    return walls

maze_walls = create_maze()

# Helper function to check collision between a circle and a rectangle.
def circle_rect_collision(cx, cy, radius, rect):
    # Find the closest point on the rectangle to the circle center.
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    # Calculate the distance between the circle's center and this closest point.
    distance = math.hypot(cx - closest_x, cy - closest_y)
    return distance < radius

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key presses for left/right movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ball_x -= BALL_SPEED
    if keys[pygame.K_d]:
        ball_x += BALL_SPEED

    # Keep ball within the screen bounds horizontally
    if ball_x - BALL_RADIUS < 0:
        ball_x = BALL_RADIUS
    elif ball_x + BALL_RADIUS > WIDTH:
        ball_x = WIDTH - BALL_RADIUS

    # Check if moving the maze upward by GRAVITY_SPEED creates a collision with the ball.
    collision = False
    for wall in maze_walls:
        # Create a temporary rect shifted upward (decreasing y by GRAVITY_SPEED)
        shifted_rect = wall.copy()
        shifted_rect.y -= GRAVITY_SPEED
        if circle_rect_collision(ball_x, ball_y, BALL_RADIUS, shifted_rect):
            collision = True
            break

    # Only apply gravity if no collision is detected
    if not collision:
        for wall in maze_walls:
            wall.y -= GRAVITY_SPEED

    # Draw everything
    screen.fill(BLACK)

    # Draw maze walls
    for wall in maze_walls:
        pygame.draw.rect(screen, GRAY, wall)

    # Draw red ball (dot)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(60)