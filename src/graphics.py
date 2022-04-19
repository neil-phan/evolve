import pygame
from simple import organism, food
import random

#initialize pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1200, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolve")

FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 10
INITIAL_FOOD_COUNT = 20
FONT = pygame.font.SysFont('Comic Sans MS', 30)
SUB_FONT = pygame.font.SysFont('Comic Sans MS', 15)

def make_foods(N):
    foods = []
    for i in range (N):
        f = food.Food({'x_max': WIDTH, 'y_max': HEIGHT})
        foods.append(f)
    return foods

def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r,g,b)

def make_organisms(N):
    orgs = []
    for i in range (N):
        color = random_color()
        org = organism.Organism(color, {'x_max': WIDTH, 'y_max': HEIGHT})
        orgs.append(org)
    return orgs

def generation_done(orgs):
    for org in orgs:
        if org.num_eaten < 1:
            orgs.remove(org)
        else:
            if org.num_eaten >= 2:
                for i in range(org.num_eaten-1):
                    child = org.reproduce()
                    orgs.append(child)
            org.num_eaten = 0

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
        # org.move(WIDTH, HEIGHT)
        org.target_move(foods, WIDTH, HEIGHT)
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

    speed, size, rng = make_graph(orgs)
    text = FONT.render(f"Generation: {generation_num}", 1, 'black')
    graph_text = SUB_FONT.render(f"Avg Gen Speed: {speed}| Avg Gen Size: {size} | Avg Gen Range: {rng}", 1, 'black')
    WINDOW.blit(text, (WIDTH-10-text.get_width(), 10))
    WINDOW.blit(graph_text, (WIDTH-10-graph_text.get_width(), 50))
    pygame.display.update()

#create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    counter = 15
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    orgs = make_organisms(INITIAL_ORGANISM_COUNT)
    foods = make_foods(INITIAL_FOOD_COUNT)
    

    generation_num = 1
    while running:
        clock.tick(FPS) #   Caps game frames at 60fps
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1

                #reset after 15 seconds per generation
                if counter == 0:
                    generation_num+=1
                    generation_done(orgs)
                    foods = make_foods(10)
                    counter = 15

            if event.type == pygame.QUIT:
                running = False

        draw(orgs, foods, generation_num)
        if len(foods) == 0: 
            generation_num+=1
            generation_done(orgs)
            foods = make_foods(10)
            counter = 15

if __name__ == '__main__':
    main()
