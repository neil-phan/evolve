from PIL import Image
import opensimplex as simplex
import random
import pygame

# initialize biome colors
WATER = (0, 0, 255)
BEACH = (249, 209, 153)
FOREST = (144, 169, 85)
JUNGLE = (79, 119, 45)
SAVANNAH = (49, 87, 44)
DESERT = (236, 243, 158)
SNOW = (240, 234, 210)

# randomizing seed of generator
simplex.seed(random.randrange(0, 10000))

"""
Each of the terrain generation functions returns a pygame-usable image.
This can be mapped onto the background.
"""

# generates a noise value
def noise(nx, ny):
    return simplex.noise2(nx, ny) / 2.0 + 0.5

# semi-limited but simple terrain generation
def simple_terrain(width, height, frequency):
    im = Image.new('RGB', (width, height))
    for y in range(0, height):
        for x in range(0, width):
            nx = x / width - 0.5
            ny = y / height - 0.5
            # value = noise(FREQUENCY * nx, FREQUENCY * ny)
            e = 1 * noise(frequency * 1 * nx, frequency * 1 * ny)
            + 0.5 * noise(frequency * 2 * nx, frequency * 2 * ny)
            + 0.25 * noise(frequency * 4 * nx, frequency * 4 * ny)
            value = e / (1 + 0.5 + 0.25)
            if value < 0.1:
                color = WATER
            elif value < 0.2:
                color = BEACH
            elif value < 0.3:
                color = FOREST
            elif value < 0.5:
                color = JUNGLE
            elif value < 0.7:
                color = SAVANNAH
            elif value < 0.9:
                color = DESERT
            else:
                color = SNOW
            # color = (int(value * 256), int(value * 256), int(value * 256))
            # color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('terrain.png')
    terrain = pygame.image.load('terrain.png')
    return terrain

# gives much more control over how terrain is generated
def complex_terrain(width, height):
    im = Image.new('RGB', (width, height))
    genE = simplex.OpenSimplex(random.randrange(0, 1000))
    genM = simplex.OpenSimplex(random.randrange(0, 1000))

    def noiseE(nx, ny):
        return genE.noise2(nx, ny) / 2 + 0.5

    def noiseM(nx, ny):
        return genM.noise2(nx, ny) / 2 + 0.5
    for y in range(0, height):
        for x in range(0, width):
            nx = x / width - 0.5
            ny = y / height - 0.5
            e = (0.56 * noiseE(1 * nx, 1 * ny)
                 + 0.42 * noiseE(2 * nx, 2 * ny)
                 + 0.27 * noiseE(4 * nx, 4 * ny)
                 + 0.13 * noiseE(8 * nx, 8 * ny)
                 + 0.06 * noiseE(16 * nx, 16 * ny)
                 + 0.03 * noiseE(32 * nx, 32 * ny))
            e = e / (0.56 + 0.42 + 0.27 + 0.13 + 0.06 + 0.03)
            value = e ** 4.80
            if abs(value) < 0.005:
                color = WATER
            elif abs(value) < 0.02:
                color = BEACH
            elif abs(value) < 0.03:
                color = FOREST
            elif abs(value) < 0.05:
                color = JUNGLE
            elif abs(value) < 0.07:
                color = SAVANNAH
            elif abs(value) < 0.09:
                color = DESERT
            else:
                color = SNOW
            im.putpixel((x, y), color)
    im.save('terrain.png')
    terrain = pygame.image.load('terrain.png')
    return terrain

# greyscale barebones terrain generation
def bastard(width, height, feature):
    im = Image.new('L', (width, height))
    for y in range(0, height):
        for x in range(0, width):
            value = abs(simplex.noise2(x / feature, y / feature))
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('terrain.png')
    im.show()
    terrain = pygame.image.load('terrain.png')
    return terrain
