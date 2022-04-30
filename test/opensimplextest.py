from PIL import Image  # Depends on the Pillow lib
import numpy as np
import opensimplex as simplex

WIDTH = 1200
HEIGHT = 1000
FEATURE_SIZE = 50

def noise(nx, ny):
    return simplex.noise2(nx, ny) / 2.0 + 0.5

def main():
    print('Generating 2D image...')
    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    # im.save('noise1.png')

    values = []
    for y in range(0, HEIGHT):
        values.append([0] * WIDTH)
        for x in range(0, WIDTH):
            nx = x / WIDTH - 0.5
            ny = y / HEIGHT - 0.5
            values[y][x] = noise(nx, ny)
    values = int(value + 1 * 128)
    img = Image.fromarray(values)
    img.save('noise3.png')


if __name__ == '__main__':
    main()
