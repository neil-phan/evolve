from opensimplex import OpenSimplex
import numpy as np

# initialize pygame
WIDTH, HEIGHT = 1000, 1000

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
shade = (value * 255).astype(np.ubyte)

# array needs to be in this shape
rgb = np.dstack([shade] * 3)
# print(rgb.shape)

nuts = gen.noise2array(10, 10)
print(nuts)

# test = pygame.surfarray.make_surface(rgb)


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

# TERRAIN = terrain(noise)
