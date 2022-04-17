from curses.textpad import rectangle
import pygame
from simple import organism, food

#initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolve")

FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 10
INITIAL_FOOD_COUNT = 50


def make_foods(N):
    foods = []
    for i in range (N):
        f = food.Food({'x_max': WIDTH, 'y_max': HEIGHT})
        foods.append(f)
    return foods

def make_organisms(N):
    orgs = []
    for i in range (N):
        org = organism.Organism({'x_max': WIDTH, 'y_max': HEIGHT})
        orgs.append(org)
    return orgs

def draw(orgs, foods):
    WINDOW.fill(BG_COLOR)

    for org in orgs:
        org.draw(WINDOW)
        org.move(WIDTH, HEIGHT)
        # org.mouse_move()

    for food in foods:
        food.draw(WINDOW)
    
    #   COLLISION DETECTION
    for org in orgs:
        for food in foods:
            if org.is_eating(food):
                foods.remove(food)

                #Eating outcomes here
                org.rad+=2
                org.speed+=2

    pygame.display.update()

#create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    orgs = make_organisms(INITIAL_ORGANISM_COUNT)
    foods = make_foods(INITIAL_FOOD_COUNT)

    while running:
        clock.tick(FPS) #   Caps game frames at 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(orgs, foods)

if __name__ == '__main__':
    main()
