from curses.textpad import rectangle
import pygame
from simple import organism

#initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolve")

FPS = 60
BG_COLOR = "white"
INITIAL_ORGANISM_COUNT = 10
ORGANISM_COLOR = "red"



def make_organisms(N):
    orgs = []
    for i in range (N):
        org = organism.Organism({'x_max': WIDTH, 'y_max': HEIGHT})
        orgs.append(org)
    return orgs

def draw(orgs):
    WINDOW.fill(BG_COLOR)

    for org in orgs:
        org.draw(WINDOW, ORGANISM_COLOR)
    pygame.display.update()

#create game loop
def main():
    clock = pygame.time.Clock()
    running = True

    orgs = make_organisms(INITIAL_ORGANISM_COUNT)

    while running:
        clock.tick(FPS) #   Caps game frames at 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(orgs)

if __name__ == '__main__':
    main()
