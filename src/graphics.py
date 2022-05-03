import pygame
from simple import organism, predator, food, tree
from simple.terrain import simple_terrain
import numpy as np
import matplotlib.pyplot as plt
import graph
import random
from PIL import Image

"""
Helper class to make the buttons for the menu variables.
"""
class Button():
    def __init__(self, win, size, coords, color, text, font_size):
        self.win = win
        self.w, self.h = size
        self.x, self.y = coords
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)

        self.button_surface = pygame.Surface((self.w, self.h))
        self.button_surface.fill(color)
        self.button_rect = self.button_surface.get_rect(
            center=(self.x, self.y))

        self.text_surface = self.font.render(self.text, False, 'black')
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

    def draw(self):
        self.win.blit(self.button_surface, self.button_rect)
        self.win.blit(self.text_surface, self.text_rect)

    def action(self, func, variable):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return func(variable)
        return variable


# initialize pygame
pygame.init()
pygame.font.init()
WINDOW = pygame.display.set_mode((1300, 900))
WIDTH, HEIGHT = WINDOW.get_size()
offset = WIDTH // 3
SIM_WIDTH = WIDTH - offset
pygame.display.set_caption("Evolve")

# Terrain variables
FEATURE_SIZE = 100  # controls "resolution" (higher means more blurry)
FREQUENCY = 2  # controls noise level (higher means more noise)
MUD = (112, 84, 62)  # this can also be water
BEACH = (212, 209, 181)
GRASS = (183, 217, 104)
HILL = (157, 201, 88)
FOREST = (95, 149, 55)
DARK_FOREST = (77, 124, 45)

# Environment variables
FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 10
INITIAL_PRED_COUNT = 0
INITIAL_FOOD_COUNT = 20
INITIAL_TREE_COUNT = 5
GEN_TIMER = 20

# Organism variables
O_FITNESS_COST = 0
O_REPRODUCTION_COST = 15
O_LITTER_COST = 5
O_LABOR_COST = 7
O_DEATH = 0
O_SIZE_COST = 15
O_SPEED_COST = 3

# Organism neural networks
o_settings = {
    'input': 1,
    'hidden': 5,
    'output': 2
}

# Predator variables
P_FITNESS_COST = 1
P_REPRODUCTION_COST = 20
P_LITTER_COST = 7
P_LABOR_COST = 10
P_DEATH = -10
P_SIZE_COST = 20
P_SPEED_COST = 4

# Predator neural networks
p_settings = {
    'input': 1,
    'hidden': 5,
    'output': 1
}

# Food variables
ENERGY_MAX = 4
FOOD_REPLENISH_FOOD = 5
FOOD_REPLENISH_TIME = 5
FOOD_SPOIL = 20

# Tree variables
TREE_REPLENISH_TIME = 10
TREE_REPLENISH_FOOD = 2

# Pygame variables
FONT = pygame.font.SysFont('Comic Sans MS', 30)
SUB_FONT = pygame.font.SysFont('Comic Sans MS', 15)

# Graphing variables
DATA = np.empty(0)
menu_surface = pygame.Surface((offset, HEIGHT))
menu_surface.fill('aliceblue')
menu_rect = menu_surface.get_rect(topleft=(SIM_WIDTH, 0))

graph_text_surface = FONT.render('Graph', False, 'black')
graph_text_surface_rect = graph_text_surface.get_rect(
    midtop=(SIM_WIDTH + offset // 2, 0))
variables_text_surface = FONT.render('Variables', False, 'black')
variables_text_surface_rect = variables_text_surface.get_rect(
    midtop=(SIM_WIDTH + offset // 2, HEIGHT // 2))

pause_surface = pygame.Surface((offset * 0.30, HEIGHT * 0.05))
pause_surface.fill('antiquewhite3')
pause_surface_rect = pause_surface.get_rect(
    bottomleft=(WIDTH - offset // 2 + 50, HEIGHT - 20))
pause_text = SUB_FONT.render('Pause', False, 'black')
pause_text_rect = pause_text.get_rect(center=(WIDTH-offset//2+50+offset*0.15, HEIGHT-20-HEIGHT*0.025))

generate_surface = pygame.Surface((offset * 0.30, HEIGHT * 0.05))
generate_surface.fill('antiquewhite2')
generate_surface_rect = generate_surface.get_rect(
    bottomright=(WIDTH - (offset // 2) - 50, HEIGHT - 20))
generate_text = SUB_FONT.render('Generate', False, 'black')
generate_text_rect = generate_text.get_rect(center=(WIDTH-offset//2-50-offset*0.15, HEIGHT-20-HEIGHT*0.025))

# GRAPH STUFF
graph = graph.Graph(WINDOW, ((SIM_WIDTH, WIDTH), (HEIGHT // 2, 0)))

# SIMULATION OVER
simulation_over_text = FONT.render('Simulation Over.', False, 'black')
simulation_over_text_rect = simulation_over_text.get_rect(
    center=(SIM_WIDTH // 2, HEIGHT // 2))

range_plus_button = Button(WINDOW, (offset * 0.06, HEIGHT * 0.02), (SIM_WIDTH +
                           offset // 2 - offset * 0.25, HEIGHT // 2 + HEIGHT * 0.1), 'aquamarine3', 'PLUS', 10)
# Produce a random color combination
def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

# Create N organisms with unique traits
def make_organisms(N, mutation_rate):
    orgs = []
    env_map = {
        'x_max': SIM_WIDTH,
        'y_max': HEIGHT,
    }
    for i in range(N):
        color = random_color()
        org = organism.Organism(
            color, env_map, mutation_rate, settings=o_settings)
        orgs.append(org)
    return orgs

# Create N predators with unique traits
def make_predators(N):
    preds = []
    env_map = {
        'x_max': WIDTH,
        'y_max': HEIGHT,
    }
    for _ in range(N):
        color = 'red'
        pred = predator.Predator(color, env_map)
        preds.append(pred)
    return preds

def make_foods(N):
    foods = []
    attributes = {
        'x_min': 0,
        'y_min': 0,
        'x_max': SIM_WIDTH,
        'y_max': HEIGHT
    }

    for _ in range(N):
        f = food.Food(attributes)
        foods.append(f)
    return foods

# Create N trees with food_energy=ENERGY_MAX
def make_trees(N):
    trees = []
    for _ in range(N):
        t = tree.Tree({'x_max': SIM_WIDTH, 'y_max': HEIGHT})
        trees.append(t)
    return trees

def generation_done(orgs, speed, size):
    for org in orgs:
        if org.fitness < 1:
            orgs.remove(org)
        else:
            if org.fitness >= 2:
                for i in range(org.fitness - 1):
                    child = org.reproduce()
                    orgs.append(child)
            org.fitness = 0
            # org.reset_energy()

    # UPDATE GRAPH
    graph.add_point(speed, size)

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

# Draw all the organisms, foods, trees, and statistics
def draw(orgs, preds, foods, trees, generation_num, terrain, pix):
    surface = pygame.image.load(terrain)
    WINDOW.blit(surface, (0, 0))
    for org in orgs:
        # changing speed based on terrain
        color = pix[org.x, org.y]
        if color == MUD:
            org.speed = org.speeds[8]
        elif color == BEACH:
            org.speed = org.speeds[0]
        elif color == GRASS:
            org.speed = org.speeds[1]
        elif color == HILL:
            org.speed = org.speeds[2]
        elif color == FOREST:
            org.speed = org.speeds[3]
        elif color == DARK_FOREST:
            org.speed = org.speeds[5]

        org.draw(WINDOW)
        org.nearest_food(foods)
        org.think()
        org.move(SIM_WIDTH, HEIGHT)

    for pred in preds:
        pred.draw(WINDOW)
        pred.target_move(orgs, SIM_WIDTH, HEIGHT)

    for food in foods:
        food.draw(WINDOW)

    for tree in trees:
        tree.draw(WINDOW)

    # COLLISION DETECTION
    for org in orgs:
        for food in foods:
            if org.is_eating(food):
                foods.remove(food)

    for pred in preds:
        for org in orgs:
            if pred.is_eating(org):
                orgs.remove(org)

    WINDOW.blit(menu_surface, menu_rect)
    pygame.draw.line(WINDOW, 'black', (SIM_WIDTH, 0), (SIM_WIDTH, HEIGHT), 1)
    pygame.draw.line(WINDOW, 'black', (SIM_WIDTH, HEIGHT // 2),
                     (WIDTH, HEIGHT // 2), 1)

    WINDOW.blit(graph_text_surface, graph_text_surface_rect)
    WINDOW.blit(variables_text_surface, variables_text_surface_rect)
    WINDOW.blit(pause_surface, pause_surface_rect)
    WINDOW.blit(generate_surface, generate_surface_rect)
    WINDOW.blit(pause_text, pause_text_rect)
    WINDOW.blit(generate_text, generate_text_rect)

def pause_simulation(paused, orgs):
    for org in orgs:
        org.paused = paused

def generate_simulation(org_count, new_mutation_rate, food_count, tree_count):
    orgs = make_organisms(org_count, new_mutation_rate)
    foods = make_foods(food_count)
    trees = make_trees(tree_count)
    counter = GEN_TIMER
    generation_num = 1
    paused = False
    graph.speed_vals, graph.size_vals = [], []
    graph.num_vals = 0
    return orgs, foods, counter, generation_num, paused, trees

def simulation_over():
    WINDOW.blit(simulation_over_text, simulation_over_text_rect)

def add(count):
    return count + 1

def smaller_add(count):
    return round(count + 0.05, 2)

def subtract(count):
    if count > 0:
        return count - 1
    return count

def smaller_subtract(count):
    if count > 0:
        return round(count - 0.05, 2)
    return count

def random_terrain():
    image_string = '../generated_terrains/terrain' + \
        str(random.randrange(1, 13)) + '.jpg'
    im = Image.open(image_string)
    pix = im.load()
    return image_string, pix

# create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    # MENU VARIABLES
    mutation_rate = 0.50
    new_mutation_rate = mutation_rate
    food_count = INITIAL_FOOD_COUNT
    new_food_count = food_count
    initial_org_count = INITIAL_ORGANISM_COUNT
    new_initial_org_count = initial_org_count
    tree_count = INITIAL_TREE_COUNT
    new_tree_count = tree_count

    counter = GEN_TIMER
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    orgs = make_organisms(initial_org_count, mutation_rate)
    preds = make_predators(INITIAL_PRED_COUNT)
    foods = make_foods(food_count)
    trees = make_trees(tree_count)
    generation_num = 1
    paused = False

    # MENU BUTTONS
    mutation_plus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH +
                           offset // 2 + offset * 0.30, HEIGHT // 2 + HEIGHT * 0.1), 'green', 'PLUS', 10)
    mutation_minus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH +
                            offset // 2 - offset * 0.30, HEIGHT // 2 + HEIGHT * 0.1), 'red', 'SUB', 10)

    food_plus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH + offset //
                       2 + offset * 0.30, HEIGHT // 2 + HEIGHT * 0.15), 'green', 'PLUS', 10)
    food_minus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH +
                        offset // 2 - offset * 0.30, HEIGHT // 2 + HEIGHT * 0.15), 'red', 'SUB', 10)

    org_plus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH + offset //
                      2 + offset * 0.35, HEIGHT // 2 + HEIGHT * 0.20), 'green', 'PLUS', 10)
    org_minus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH +
                       offset // 2 - offset * 0.35, HEIGHT // 2 + HEIGHT * 0.20), 'red', 'SUB', 10)

    tree_plus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH + offset //
                       2 + offset * 0.35, HEIGHT // 2 + HEIGHT * 0.25), 'green', 'PLUS', 10)
    tree_minus = Button(WINDOW, (offset * 0.05, HEIGHT * 0.02), (SIM_WIDTH +
                        offset // 2 - offset * 0.35, HEIGHT // 2 + HEIGHT * 0.25), 'red', 'SUB', 10)

    speed, size, rng = make_graph(orgs)
    np.append(DATA, (speed, size, rng))

    # RANDOM TERRAIN
    image_string, pix = random_terrain()

    while running:
        org_num = len(orgs)
        clock.tick(FPS)  # Caps game frames at 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # VARIABLES ACTIONS
            new_mutation_rate = mutation_plus.action(
                smaller_add, new_mutation_rate)
            new_mutation_rate = mutation_minus.action(
                smaller_subtract, new_mutation_rate)

            new_food_count = food_plus.action(add, new_food_count)
            new_food_count = food_minus.action(subtract, new_food_count)

            new_initial_org_count = org_plus.action(add, new_initial_org_count)
            new_initial_org_count = org_minus.action(
                subtract, new_initial_org_count)

            new_tree_count = tree_plus.action(add, new_tree_count)
            new_tree_count = tree_minus.action(subtract, new_tree_count)

            if pause_surface_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                paused = not paused
                pause_simulation(paused, orgs)

            # UPDATE ALL THE NEW VARIABLES
            if generate_surface_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                mutation_rate = new_mutation_rate
                food_count = new_food_count
                initial_org_count = new_initial_org_count
                tree_count = new_tree_count
                orgs, foods, counter, generation_num, paused, trees = generate_simulation(
                    initial_org_count, mutation_rate, food_count, tree_count)
                image_string, pix = random_terrain()

            if event.type == pygame.USEREVENT:

                # # replenish food in areas without trees
                # if counter % FOOD_REPLENISH_TIME == 0:
                #     foods += make_foods(FOOD_REPLENISH_FOOD)

                # # Every 5 seconds trees spawn food within its radius
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

                if not paused:
                    counter -= 1

                    # reset after 15 seconds per generation
                if counter == 0 and org_num > 0:
                    generation_num += 1
                    speed, size, rng = make_graph(orgs)
                    np.append(DATA, (speed, size, rng))
                    generation_done(orgs, speed, size)
                    foods = make_foods(food_count)
                    counter = GEN_TIMER

        if len(foods) == 0 and org_num > 0:
            generation_num += 1
            speed, size, rng = make_graph(orgs)
            np.append(DATA, (speed, size, rng))
            generation_done(orgs, speed, size)
            foods = make_foods(food_count)
            counter = GEN_TIMER

        # Display all objects on screen
        draw(orgs, preds, foods, trees, generation_num, image_string, pix)

        # MENU VARIABLES
        mutation_text_surface = SUB_FONT.render(
            f'Current Mutation Rate: {str(mutation_rate)}', False, 'black')
        new_mutation_text_surface = SUB_FONT.render(
            f'New Mutation Rate: {str(new_mutation_rate)}', False, 'black')
        mutation_text_rect = mutation_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.1))
        new_mutation_text_rect = new_mutation_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.1 + 15))

        food_text_surface = SUB_FONT.render(
            f'Current Initial Food Count: {str(food_count)}', False, 'black')
        new_food_text_surface = SUB_FONT.render(
            f'New Initial Food Count: {str(new_food_count)}', False, 'black')
        food_text_rect = food_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.15))
        new_food_text_rect = new_food_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.15 + 15))

        org_text_surface = SUB_FONT.render(
            f'Current Initial Organism Count: {str(initial_org_count)}', False, 'black')
        new_org_text_surface = SUB_FONT.render(
            f'New Initial Food Count: {str(new_initial_org_count)}', False, 'black')
        org_text_rect = org_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.20))
        new_org_text_rect = new_org_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.20 + 15))

        tree_text_surface = SUB_FONT.render(
            f'Current Initial Tree Count: {str(tree_count)}', False, 'black')
        new_tree_text_surface = SUB_FONT.render(
            f'New Initial Tree Count: {str(new_tree_count)}', False, 'black')
        tree_text_rect = tree_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.25))
        new_tree_text_rect = new_tree_text_surface.get_rect(
            center=(SIM_WIDTH + offset // 2, HEIGHT // 2 + HEIGHT * 0.25 + 15))

        # DRAW MENU BUTTONS AND TEXT
        WINDOW.blit(mutation_text_surface, mutation_text_rect)
        WINDOW.blit(new_mutation_text_surface, new_mutation_text_rect)
        WINDOW.blit(org_text_surface, org_text_rect)
        WINDOW.blit(new_org_text_surface, new_org_text_rect)
        WINDOW.blit(food_text_surface, food_text_rect)
        WINDOW.blit(new_food_text_surface, new_food_text_rect)
        WINDOW.blit(tree_text_surface, tree_text_rect)
        WINDOW.blit(new_tree_text_surface, new_tree_text_rect)

        mutation_plus.draw()
        mutation_minus.draw()
        food_plus.draw()
        food_minus.draw()
        org_plus.draw()
        org_minus.draw()
        tree_plus.draw()
        tree_minus.draw()

        # GRAPH
        text = FONT.render(f"Generation: {generation_num}", 1, 'black')
        graph_text = SUB_FONT.render(
            f"Avg Gen Speed: {speed}| Avg Gen Size: {size} | Avg Gen Range: {rng}", 1, 'black')
        WINDOW.blit(text, (SIM_WIDTH - 10 - text.get_width(), 10))
        WINDOW.blit(graph_text, (SIM_WIDTH - 10 - graph_text.get_width(), 50))
        graph.draw()

        if org_num == 0:
            simulation_over()
        pygame.display.update()


if __name__ == '__main__':
    main()
