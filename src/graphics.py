from curses import window
from turtle import width
import pygame
from simple import organism, food, tree
import numpy as np
import matplotlib.pyplot as plt
import random
import opensimplex as simplex
from PIL import Image

# initialize pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1200, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolve")

# Terrain variables
FEATURE_SIZE = 100

# Environment variables
FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 5
INITIAL_FOOD_COUNT = 10
INITIAL_TREE_COUNT = 5
GEN_TIMER = 15

# Organism variables
FITNESS_COST = 1
REPRODUCTION_COST = 15
LITTER_COST = 5
LABOR_COST = 7
DEATH = 0
SIZE_COST = 15
SPEED_COST = 3

# Food variables
ENERGY_MAX = 4
FOOD_REPLENISH_FOOD = 5
FOOD_REPLENISH_TIME = 5
FOOD_SPOIL = 20

# Tree variables
TREE_REPLENISH_TIME = 2
TREE_REPLENISH_FOOD = 2

# Pygame variables
FONT = pygame.font.SysFont('Comic Sans MS', 30)
SUB_FONT = pygame.font.SysFont('Comic Sans MS', 15)

# Graphing variables
DATA = np.empty(0)

# Create N organisms with unique traits
def make_organisms(N):
    orgs = []
    for i in range(N):
        color = random_color()
        org = organism.Organism(color, {'x_max': WIDTH, 'y_max': HEIGHT})
        orgs.append(org)
    return orgs

# Create N food objects with energy=1
def make_foods(N):
    foods = []
    attributes = {
        'x_min': 0,
        'y_min': 0,
        'x_max': WIDTH,
        'y_max': HEIGHT
    }

    for i in range(N):
        f = food.Food(attributes)
        foods.append(f)
    return foods

# Create N trees with food_energy=ENERGY_MAX
def make_trees(N):
    trees = []
    for i in range(N):
        t = tree.Tree({'x_max': WIDTH, 'y_max': HEIGHT})
        trees.append(t)
    return trees

# Produce a random color combination
def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

def make_graph(orgs):
    count = 0
    average_speed = 0
    average_size = 0
    average_range = 0
    for org in orgs:
        average_speed += org.speed
        average_size += org.rad
        average_range += org.range
        count += 1
    if len(orgs) == 0:
        return 0, 0, 0
    return round(average_speed / count, 2), round(average_size / count, 2), round(average_range / count, 2)

# Generate pygame image using a noise function
def terrain(width, height):
    im = Image.new('L', (width, height))
    for y in range(0, HEIGHT):
        for x in range(0, width):
            value = simplex.noise2(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('noise1.png')
    map = pygame.image.load('noise1.png')
    return map

# Draw all the organisms, foods, trees, and statistics
def draw(orgs, foods, trees, generation_num, terrain):
    WINDOW.blit(terrain, (0, 0))

    for org in orgs:
        org.draw(WINDOW)
        org.target_move(foods, WIDTH, HEIGHT)

    for food in foods:
        food.draw(WINDOW)

    for tree in trees:
        tree.draw(WINDOW)

    # COLLISION DETECTION
    for org in orgs:
        for food in foods:
            if org.is_eating(food):
                foods.remove(food)

        # FOR CANABALISM
        # for org2 in orgs:
        #     if org.is_eating(org2):

    speed, size, rng = make_graph(orgs)
    np.append(DATA, (speed, size, rng))
    text = FONT.render(f"Generation: {generation_num}", 1, 'black')
    graph_text = SUB_FONT.render(
        f"Avg Speed: {speed}| Avg Size: {size} | Avg Range: {rng}", 1, 'black')
    WINDOW.blit(text, (WIDTH - 10 - text.get_width(), 10))
    WINDOW.blit(graph_text, (WIDTH - 10 - graph_text.get_width(), 50))
    pygame.display.update()

# create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    counter = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    orgs = make_organisms(INITIAL_ORGANISM_COUNT)
    foods = make_foods(INITIAL_FOOD_COUNT)
    trees = make_trees(INITIAL_TREE_COUNT)

    generation_num = 1
    TERRAIN = terrain(WIDTH, HEIGHT)

    # creating terrain

    while running:
        clock.tick(FPS)  # Caps game frames at desired FPS
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter += 1

                # Update generation num after enough time has passed
                if counter % GEN_TIMER == 0:
                    generation_num += 1

                # replenish food in areas without trees
                if counter % FOOD_REPLENISH_TIME == 0:
                    foods += make_foods(FOOD_REPLENISH_FOOD)

                # decrease fitness score for every tick
                for org in orgs:
                    org.fitness -= FITNESS_COST + float(org.rad / SIZE_COST)
                    + float(org.speed / SPEED_COST)
                    # print(org.fitness)
                    if org.fitness >= (REPRODUCTION_COST + (LITTER_COST * org.litter_size) - LITTER_COST):
                        child = org.reproduce()
                        orgs.append(child)
                        org.fitness -= LABOR_COST + \
                            (LITTER_COST * org.litter_size) - LITTER_COST
                    if org.fitness <= DEATH:
                        orgs.remove(org)  # DEAD

                # Every 5 seconds trees spawn food within its radius
                if counter % TREE_REPLENISH_TIME == 0:
                    for tree in trees:
                        attributes = {
                            'x_min': tree.x - (3 * tree.rad),
                            'y_min': tree.y - (3 * tree.rad),
                            'x_max': tree.x + (3 * tree.rad),
                            'y_max': tree.y + (3 * tree.rad),
                        }
                        for _ in range(TREE_REPLENISH_FOOD):
                            f = food.Food(attributes, energy_max=ENERGY_MAX)
                            foods.append(f)

                # Spoiling food to avoid having clusters of food if no organisms contest it
                for f in foods:
                    f.decay += 1
                    if f.decay == FOOD_SPOIL:
                        foods.remove(f)

            if event.type == pygame.QUIT:
                running = False

        # Display all objects on screen
        draw(orgs, foods, trees, generation_num, TERRAIN)


if __name__ == '__main__':
    main()
