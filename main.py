import colorsys
import random

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
clock = pygame.time.Clock()

# Set up the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Falling Sand Simulation")

hue = 0
BLACK = (0, 0, 0)

cell_size = 30

grid = []
for i in range(0, HEIGHT, cell_size):
    row = []
    for j in range(0, WIDTH, cell_size):
        row.append(0)
    grid.append(row)


def right_available(grid, y, x):
    return y + 1 < HEIGHT // cell_size and x - 1 >= 0 and grid[y + 1][x - 1] == 0


def left_available(grid, y, x):
    return y + 1 < HEIGHT // cell_size and x + 1 < WIDTH // cell_size and grid[y + 1][x + 1] == 0


def hsl_to_rgb(h, s, l):
    h /= 360.0
    s /= 100.0
    l /= 100.0
    r, g, b = colorsys.hsv_to_rgb(h, s, l)
    return int(r*255), int(g*255), int(b*255)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_buttons = pygame.mouse.get_pressed()

    if mouse_buttons[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = max(0, min(mouse_x, WIDTH - 1))
        mouse_y = max(0, min(mouse_y, HEIGHT - 1))
        grid_x = mouse_x // cell_size
        grid_y = mouse_y // cell_size
        grid[grid_y][grid_x] = hue
        hue = (hue + 1) % 360

    screen.fill(BLACK)

    # copy_grid = grid.copy() it does it by reference
    copy_grid = []
    for i in grid:
        copy_grid.append(i[:])

    for y in range(0, HEIGHT, cell_size):
        new_y = y // cell_size
        for x in range(0, WIDTH, cell_size):
            new_x = x // cell_size
            if copy_grid[new_y][new_x] != 0:
                h = copy_grid[new_y][new_x]
                color = hsl_to_rgb(h, 100, 50)
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
                if new_y + 1 < HEIGHT // cell_size:
                    if grid[new_y + 1][new_x] == 0:
                        grid[new_y][new_x] = 0
                        grid[new_y + 1][new_x] = hue
                    else:
                        random_side = random.random()
                        if right_available(grid, new_y, new_x) and random_side >= 0.5:
                            grid[new_y][new_x] = 0
                            grid[new_y + 1][new_x - 1] = hue
                        elif left_available(grid, new_y, new_x):
                            grid[new_y][new_x] = 0
                            grid[new_y + 1][new_x + 1] = hue

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
