from string import whitespace
import sys
import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((300, 300))

def terrain(noise):
    CHANNELS = 3
    RED = 0
    GREEN = 1
    BLUE = 2
    WATER_LEVEL = 0.20
    MOUNTAIN_LEVEL = 0.75

    shade = (noise * 255).astype(np.ubyte)

    rgb = np.dstack([shade] * 3)
    #rgb[(WATER_LEVEL <= noise) & (noise <= MOUNTAIN_LEVEL), GREEN] = 255
    #rgb[(noise < WATER_LEVEL), BLUE] = 255

    surf = pygame.surfarray.make_surface(rgb)
    return surf


noise = np.random.random_sample((WIDTH, HEIGHT))
TERRAIN = terrain(noise)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # screen.fill("white")
    # pygame.display.flip()

    screen.blit(TERRAIN, (0, 0))
    pygame.display.update()
