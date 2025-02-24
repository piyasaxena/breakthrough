import pygame
import sys
import math
import random
pygame.init()
WIDTH, HEIGHT = 600, 600
GAP = 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Upward Gravity Maze Game")
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
clock = pygame.time.Clock()
BALL_RADIUS = 10
ball_x = WIDTH // 2
GROUND_Y = HEIGHT // 2 - 50
ball_y = GROUND_Y
BALL_SPEED = 5
GRAVITY_SPEED = 2
jumping = False
ball_vel_y = 0
JUMP_STRENGTH = -15
GRAVITY_ACC = 1
def create_maze():
    walls = []
    wall_height = 1
    y = GAP
    while y < HEIGHT + GAP:
        gap_location = random.randint(0, WIDTH - 100)
        wall_l = pygame.Rect(0, y, gap_location, wall_height)
        wall_r = pygame.Rect(gap_location + 100, y, WIDTH - gap_location - 100, wall_height)
        walls.append(wall_l)
        walls.append(wall_r)
        y += GAP
    return walls
maze_walls = create_maze()
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not jumping:
                jumping = True
                ball_vel_y = JUMP_STRENGTH
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
    if ball_x - BALL_RADIUS < 0:
        ball_x = BALL_RADIUS
    elif ball_x + BALL_RADIUS > WIDTH:
        ball_x = WIDTH - BALL_RADIUS
    if jumping:
        ball_y += ball_vel_y
        ball_vel_y += GRAVITY_ACC
        if ball_vel_y > 0:
            for wall in maze_walls:
                if circle_rect_collision(ball_x, ball_y, BALL_RADIUS, wall):
                    ball_y = wall.top - BALL_RADIUS
                    jumping = False
                    ball_vel_y = 0
                    break
        if ball_y >= GROUND_Y:
            ball_y = GROUND_Y
            jumping = False
            ball_vel_y = 0
    collision = False
    for wall in maze_walls:
        shifted_rect = wall.copy()
        shifted_rect.y -= GRAVITY_SPEED
        if circle_rect_collision(ball_x, ball_y, BALL_RADIUS, shifted_rect):
            collision = True
            break
    if not collision:
        for wall in maze_walls:
            wall.y -= GRAVITY_SPEED
    for wall in maze_walls:
        if wall.bottom < 0:
            wall.y = HEIGHT
    screen.fill(BLACK)
    for wall in maze_walls:
        pygame.draw.rect(screen, GRAY, wall)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)
