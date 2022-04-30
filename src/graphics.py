from opensimplex import OpenSimplex
from curses import window
from turtle import width
import pygame
from simple import organism, food, tree
import numpy as np
import matplotlib.pyplot as plt
import random

# initialize pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1200, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolve")

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


# noise stuff
gen = OpenSimplex()

def noise(nx, ny):
    return gen.noise2(nx, ny) / 2.0 + 0.5

def help(values):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            nx = x / WIDTH - 0.5
            ny = y / HEIGHT - 0.5
            values[x][y] = noise(ny, nx)
    shade = (values * 255).astype(np.ubyte)
    rgb = np.dstack([shade] * 3)
    surf = pygame.surfarray.make_surface(rgb)
    return surf


values = np.zeros((WIDTH, HEIGHT))
terrain2 = help(values)

# generate canvas with noise function
def terrain(noise):
    CHANNELS = 3
    RED = 0
    GREEN = 1
    BLUE = 2
    WATER_LEVEL = 0.20
    MOUNTAIN_LEVEL = 0.75

    shade = (noise * 255).astype(np.ubyte)
    rgb = np.dstack([shade] * 3)
    rgb[(WATER_LEVEL <= noise) & (noise <= MOUNTAIN_LEVEL), GREEN] = 255
    rgb[(noise < WATER_LEVEL), BLUE] = 255
    surf = pygame.surfarray.make_surface(rgb)
    return surf


noise = np.random.random_sample((WIDTH, HEIGHT))
TERRAIN = terrain(noise)

# Draw all the organisms, foods, trees, and statistics
def draw(orgs, foods, trees, generation_num):
    WINDOW.blit(terrain2, (0, 0))
    # pygame.display.update()
    # WINDOW.fill(BG_COLOR)

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
        draw(orgs, foods, trees, generation_num)


if __name__ == '__main__':
    main()
