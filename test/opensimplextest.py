from PIL import Image  # Depends on the Pillow lib
import numpy as np
import opensimplex as simplex
import random

WIDTH = 1200
HEIGHT = 1000
FEATURE_SIZE = 100

def noise(nx, ny):
    return simplex.noise2(nx, ny) / 2.0 + 0.5

def main():
    print('Generating 2D image...')
    im = Image.new('RGB', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2(x / FEATURE_SIZE, y / FEATURE_SIZE)
            if abs(value) < 0.1:
                color = (0, 0, 255)
            else:
                gradient = int((value + 1) * 128)
                color = (gradient, gradient, gradient)
            # color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    # im.save('noise1.png')
    im.show()


FREQUENCY = 3
WATER = (0, 0, 255)
BEACH = (249, 209, 153)
FOREST = (144, 169, 85)
JUNGLE = (79, 119, 45)
SAVANNAH = (49, 87, 44)
DESERT = (236, 243, 158)
SNOW = (240, 234, 210)

def main2():
    print('Generating 2D image...')
    im = Image.new('RGB', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            nx = x / WIDTH - 0.5
            ny = y / HEIGHT - 0.5
            # value = noise(FREQUENCY * nx, FREQUENCY * ny)
            e = 1 * noise(FREQUENCY * 1 * nx, FREQUENCY * 1 * ny)
            + 0.5 * noise(FREQUENCY * 2 * nx, FREQUENCY * 2 * ny)
            + 0.25 * noise(FREQUENCY * 4 * nx, FREQUENCY * 4 * ny)
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
    im.save('newnoise.png')
    # im.show()

# more complex noise generation
# values are super low though for some reason
def main3():
    im = Image.new('RGB', (WIDTH, HEIGHT))
    genE = simplex.OpenSimplex(random.randrange(0, 1000))
    genM = simplex.OpenSimplex(random.randrange(0, 1000))

    def noiseE(nx, ny):
        return genE.noise2(nx, ny) / 2 + 0.5

    def noiseM(nx, ny):
        return genM.noise2(nx, ny) / 2 + 0.5
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            nx = x / WIDTH - 0.5
            ny = y / HEIGHT - 0.5
            e = (0.56 * noiseE(1 * nx, 1 * ny)
                 + 0.42 * noiseE(2 * nx, 2 * ny)
                 + 0.27 * noiseE(4 * nx, 4 * ny)
                 + 0.13 * noiseE(8 * nx, 8 * ny)
                 + 0.06 * noiseE(16 * nx, 16 * ny)
                 + 0.03 * noiseE(32 * nx, 32 * ny))
            e = e / (0.56 + 0.42 + 0.27 + 0.13 + 0.06 + 0.03)
            value = e ** 4.80
            # value = e / (1 + 0.5 + 0.25)
            # print(value)
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
            # color = (int(value * 256), int(value * 256), int(value * 256))
            im.putpixel((x, y), color)
    im.show()


if __name__ == '__main__':
    # main()
    # main2()
    main3()
