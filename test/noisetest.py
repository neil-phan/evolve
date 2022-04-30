from opensimplex import OpenSimplex
import numpy as np
import pygame

# initialize pygame
pygame.init()
WIDTH, HEIGHT = 1000, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# noise stuff
gen = OpenSimplex()

def noise(nx, ny):
    return gen.noise2(nx, ny) / 2.0 + 0.5


value = np.zeros((WIDTH, HEIGHT))
for x in range(WIDTH):
    for y in range(HEIGHT):
        nx = x / WIDTH - 0.5
        ny = y / HEIGHT - 0.5
        value[x][y] = noise(ny, nx)
print(value)
shade = (value * 255).astype(np.ubyte)
print('-------------')
print(shade)
rgb = np.dstack([shade] * 3)
print('----------------')
print(rgb)
test = pygame.surfarray.make_surface(rgb)

# print('value')
# print(value)
# print('--------------')

# nv = (value * 255)  # .astype(np.ubyte)
# rgb = np.dstack([nv] * 3)

# print('rgb')
# print(rgb)
# print('------------------')


def terrain(noise):
    CHANNELS = 3
    RED = 0
    GREEN = 1
    BLUE = 2
    WATER_LEVEL = 0.20
    MOUNTAIN_LEVEL = 0.75

    shade = (noise * 255).astype(np.ubyte)
    # shade
    print('shade')
    print(shade)
    print('---------------')

    rgb = np.dstack([shade] * 3)
    print('rgb')
    print(rgb)
    print('----------------------')
    rgb[(WATER_LEVEL <= noise) & (noise <= MOUNTAIN_LEVEL), GREEN] = 255
    rgb[(noise < WATER_LEVEL), BLUE] = 255
    print('new rgb')
    print(rgb)
    surf = pygame.surfarray.make_surface(rgb)
    return surf


noise = np.random.random_sample((WIDTH, HEIGHT))
# print(noise)

#TERRAIN = terrain(noise)

def main():
    running = True
    clock = pygame.time.Clock()
    FPS = 30

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # WINDOW.fill("white")
        # pygame.display.update()

        WINDOW.blit(test, (0, 0))
        pygame.display.update()


main()
