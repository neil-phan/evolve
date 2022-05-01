import pygame
from simple import organism, food
import graph
import random

#initialize pygame
pygame.init()
pygame.font.init()
# SIM_WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((1300, 900))
WIDTH, HEIGHT = WINDOW.get_size()
offset = WIDTH // 3
SIM_WIDTH = WIDTH - offset
pygame.display.set_caption("Evolve")

FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 10
INITIAL_FOOD_COUNT = 10
FONT = pygame.font.SysFont('Comic Sans MS', 30)
SUB_FONT = pygame.font.SysFont('Comic Sans MS', 15)

menu_surface = pygame.Surface((offset, HEIGHT))
menu_surface.fill('aliceblue')
menu_rect = menu_surface.get_rect(topleft=(SIM_WIDTH, 0))

graph_text_surface = FONT.render('Graph', False, 'black')
graph_text_surface_rect = graph_text_surface.get_rect(midtop=(SIM_WIDTH+offset // 2, 0))
variables_text_surface = FONT.render('Variables', False, 'black')
variables_text_surface_rect = variables_text_surface.get_rect(midtop=(SIM_WIDTH+offset//2, HEIGHT//2))

pause_surface = pygame.Surface((offset*0.30, HEIGHT*0.05))
pause_surface.fill('antiquewhite3')
pause_surface_rect = pause_surface.get_rect(bottomleft=(WIDTH-offset//2+50, HEIGHT - 20))

generate_surface = pygame.Surface((offset*0.30, HEIGHT*0.05))
generate_surface.fill('antiquewhite2')
generate_surface_rect = generate_surface.get_rect(bottomright=(WIDTH-(offset//2)-50, HEIGHT-20))

# GRAPH STUFF
graph = graph.Graph(WINDOW, ((SIM_WIDTH, WIDTH), (HEIGHT//2, 0)))

#SIMULATION OVER
simulation_over_text = FONT.render('Simulation Over.', False, 'black')
simulation_over_text_rect = simulation_over_text.get_rect(center=(SIM_WIDTH//2, HEIGHT//2))

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
        self.button_rect = self.button_surface.get_rect(center=(self.x, self.y))

        self.text_surface = self.font.render(self.text, False, 'black')
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))
        
    def draw(self):        
        self.win.blit(self.button_surface, self.button_rect)
        self.win.blit(self.text_surface, self.text_rect)
    
    def action(self, func, variable):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return func(variable)
        return variable
range_plus_button= Button(WINDOW, (offset*0.06, HEIGHT*0.02), (SIM_WIDTH+offset//2-offset*0.25, HEIGHT//2+HEIGHT*0.1), 'aquamarine3', 'PLUS', 10)

def make_foods(N):
    foods = []
    for i in range (N):
        f = food.Food({'x_max': SIM_WIDTH, 'y_max': HEIGHT})
        foods.append(f)
    return foods

def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r,g,b)

def make_organisms(N, mutation_rate):
    orgs = []
    for i in range (N):
        color = random_color()
        org = organism.Organism(color, {'x_max': SIM_WIDTH, 'y_max': HEIGHT}, mutation_rate)
        orgs.append(org)
    return orgs

def generation_done(orgs, speed, size):
    for org in orgs:
        if org.num_eaten < 1:
            orgs.remove(org)
        else:
            if org.num_eaten >= 2:
                for i in range(org.num_eaten-1):
                    child = org.reproduce()
                    orgs.append(child)
            org.num_eaten = 0
            org.reset_energy()
    
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
        count+=1
    
    return round(average_speed / count, 2), round(average_size / count, 2), round(average_range / count, 2)
        
def draw(orgs, foods, generation_num):
    WINDOW.fill(BG_COLOR)

    for org in orgs:
        org.draw(WINDOW)
        # org.move(SIM_WIDTH, HEIGHT)
        org.target_move(foods, SIM_WIDTH, HEIGHT)
        # org.mouse_move()

    for food in foods:
        food.draw(WINDOW)
    
    #   COLLISION DETECTION
    for org in orgs:
        for food in foods:
            if org.is_eating(food):
                foods.remove(food)
        
        # FOR CANABALISM
        # for org2 in orgs:
        #     if org.is_eating(org2):
        #         orgs.remove(org2)

    WINDOW.blit(menu_surface, menu_rect)
    pygame.draw.line(WINDOW, 'black', (SIM_WIDTH, 0), (SIM_WIDTH, HEIGHT), 1)
    pygame.draw.line(WINDOW, 'black', (SIM_WIDTH, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)

    WINDOW.blit(graph_text_surface, graph_text_surface_rect)
    WINDOW.blit(variables_text_surface, variables_text_surface_rect)
    WINDOW.blit(pause_surface, pause_surface_rect)
    WINDOW.blit(generate_surface, generate_surface_rect)

def pause_simulation(paused, orgs):
    for org in orgs:
        org.paused = paused

def generate_simulation(org_count new_mutation_rate, food_count):
    orgs = make_organisms(org_count, new_mutation_rate)
    foods = make_foods(food_count)
    counter = 10
    generation_num = 1
    paused = False
    graph.speed_vals, graph.size_vals = [], []
    graph.num_vals = 0
    return orgs, foods, counter, generation_num, paused

def simulation_over():
    WINDOW.blit(simulation_over_text, simulation_over_text_rect)

def subtract_food(food_count):
    return food_count-1

def add_food(food_count):
    return food_count+1

def subtract_org(org_count):
    return org_count-1

def add_org(org_count):
    return org_count+1

#create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    # VARIABLES
    mutation_rate = 0.50
    new_mutation_rate = mutation_rate
    food_count = INITIAL_FOOD_COUNT
    new_food_count = food_count
    initial_org_count = INITIAL_ORGANISM_COUNT
    new_initial_org_count = initial_org_count

    counter = 15
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    orgs = make_organisms(INITIAL_ORGANISM_COUNT, mutation_rate)
    foods = make_foods(INITIAL_FOOD_COUNT)
    generation_num = 1
    paused = False

    plus_text_surface = pygame.Surface((offset*0.06, HEIGHT*0.02))
    plus_text_surface.fill('green')
    plus_text_rect = plus_text_surface.get_rect(center=(SIM_WIDTH+offset//2+offset*0.25, HEIGHT//2+HEIGHT*0.1))
    minus_surface = pygame.Surface((offset*0.06, HEIGHT*0.02))
    minus_surface.fill('red')
    minus_rect = minus_surface.get_rect(center=(SIM_WIDTH+offset//2-offset*0.25, HEIGHT//2+HEIGHT*0.1))

    food_plus = Button(WINDOW, (offset*0.05, HEIGHT*0.02), (SIM_WIDTH+offset//2+offset*0.30, HEIGHT//2+HEIGHT*0.15), 'green', 'PLUS', 10)
    food_minus = Button(WINDOW, (offset*0.05, HEIGHT*0.02), (SIM_WIDTH+offset//2-offset*0.30, HEIGHT//2+HEIGHT*0.15), 'red', 'SUB', 10)

    org_plus = Button(WINDOW, (offset*0.05, HEIGHT*0.02), (SIM_WIDTH+offset//2+offset*0.35, HEIGHT//2+HEIGHT*0.20), 'green', 'PLUS', 10)
    org_minus = Button(WINDOW, (offset*0.05, HEIGHT*0.02), (SIM_WIDTH+offset//2-offset*0.35, HEIGHT//2+HEIGHT*0.20), 'red', 'SUB', 10)

    
    speed, size, rng = make_graph(orgs)
    while running:
        org_num = len(orgs)
        clock.tick(FPS) #   Caps game frames at 60fps
        for event in pygame.event.get():

            # VARIABLES ACTIONS
            new_food_count = food_plus.action(add_food, new_food_count)
            new_food_count = food_minus.action(subtract_food, new_food_count)

            new_initial_org_count = org_plus.action(add_org, new_initial_org_count)
            new_initial_org_count = org_minus.action(subtract_org, new_initial_org_count)

            if pause_surface_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                paused = not paused
                pause_simulation(paused, orgs)

            # UPDATE ALL THE NEW VARIABLES
            if generate_surface_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                mutation_rate = new_mutation_rate
                food_count = new_food_count
                initial_org_count = new_initial_org_count
                orgs, foods, counter, generation_num, paused = generate_simulation(mutation_rate, food_count)

            if plus_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                new_mutation_rate = round(new_mutation_rate + 0.05, 2)

            if minus_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if new_mutation_rate > 0:
                    new_mutation_rate = round(new_mutation_rate - 0.05, 2)

            if event.type == pygame.USEREVENT:
                if not paused:
                    counter -= 1

                        #reset after 15 seconds per generation
                if counter == 0 and org_num > 0:
                    generation_num+=1
                    speed, size, rng = make_graph(orgs)
                    generation_done(orgs, speed, size)
                    foods = make_foods(food_count)
                    counter = 15
            
            if event.type == pygame.QUIT:
                running = False

        if len(foods) == 0 and org_num > 0: 
            generation_num+=1
            speed, size, rng = make_graph(orgs)
            generation_done(orgs, speed, size)
            foods = make_foods(food_count)
            counter = 15
        

        draw(orgs, foods, generation_num)

        # MENU VARIABLES
        mutation_text_surface = SUB_FONT.render(f'Current Mutation Rate: {str(mutation_rate)}', False, 'black')
        new_mutation_text_surface = SUB_FONT.render(f'New Mutation Rate: {str(new_mutation_rate)}', False, 'black')
        mutation_text_rect = mutation_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.1))
        new_mutation_text_rect = new_mutation_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.1+15))

        food_text_surface = SUB_FONT.render(f'Current Initial Food Count: {str(food_count)}', False, 'black')
        new_food_text_surface = SUB_FONT.render(f'New Initial Food Count: {str(new_food_count)}', False, 'black')
        food_text_rect = food_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.15))
        new_food_text_rect = new_food_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.15+15))

        org_text_surface = SUB_FONT.render(f'Current Initial Organism Count: {str(initial_org_count)}', False, 'black')
        new_org_text_surface = SUB_FONT.render(f'New Initial Food Count: {str(new_initial_org_count)}', False, 'black')
        org_text_rect = org_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.20))
        new_org_text_rect = new_org_text_surface.get_rect(center=(SIM_WIDTH+offset//2, HEIGHT//2+HEIGHT*0.20+15))
    

        WINDOW.blit(mutation_text_surface, mutation_text_rect)
        WINDOW.blit(new_mutation_text_surface, new_mutation_text_rect)
        WINDOW.blit(plus_text_surface, plus_text_rect)
        WINDOW.blit(minus_surface, minus_rect)
        WINDOW.blit(org_text_surface, org_text_rect)
        WINDOW.blit(new_org_text_surface, new_org_text_rect)

        WINDOW.blit(food_text_surface, food_text_rect)
        WINDOW.blit(new_food_text_surface, new_food_text_rect)
        food_plus.draw()
        food_minus.draw()
        org_plus.draw()
        org_minus.draw()

        # GRAPH
        text = FONT.render(f"Generation: {generation_num}", 1, 'black')
        graph_text = SUB_FONT.render(f"Avg Gen Speed: {speed}| Avg Gen Size: {size} | Avg Gen Range: {rng}", 1, 'black')
        WINDOW.blit(text, (SIM_WIDTH-10-text.get_width(), 10))
        WINDOW.blit(graph_text, (SIM_WIDTH-10-graph_text.get_width(), 50))
        graph.draw()

        if org_num == 0:
            simulation_over()
        pygame.display.update()

if __name__ == '__main__':
    main()
