# Organism 
import math
import random
import pygame

pygame.font.init()

class Organism:
    FULL_AMOUNT = 2
    FONT = pygame.font.SysFont('Comic Sans MS', 10)
    MUTATION_RATE = 0.10

    # FONT = pygame.font.SysFont('Comic Sans MS', 20)
    """
    A simple organism with simple traits.
    
    Attributes
    ----------
    name (str): the name of the organism
    r (int): the angle which the organism is looking at
    x (int): the current x position of the organism on env_map
    y (int): the current y position of the organism on env_map
    velocity (int): the maximum velocity of the organism
    strength (int): the maximum strength of the organism
    see_food (bool): determines if the organism sees food in its vision
    vision (int): how far the organism can see in the distance
    peripheral (int): the angle of view the organism can see
    fitness (int): how much food the organism has consumed
    """
    def __init__(self, color, env_map, coords=None, speed=None, rad=None):
        """
        Initializes an organism object in a random.uniform (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        name (str): the name of the organism, default is None
        """
        # Environmental starting traits
        self.color = color
        self.speed = speed if speed != None else random.uniform(1,15)
        self.rad = rad if rad != None else random.uniform(10,30)
        self.num_eaten = 0
        self.r = random.uniform(0, 360)                                       # View
        if coords == None:
            self.x = random.randrange(0, env_map['x_max'])                       # Starting X 
            self.y = random.randrange(0, env_map['y_max'])                       # Starting Y
        else:
            self.x = coords[0]
            self.y = coords[1]
        self.text = self.FONT.render(f'{round(self.speed, 2)} : {round(self.rad, 2)}', 1, 'black')
        # text = FONT.render("{V}, 1, 'black')
        
        # Customizable traits for the user to select in their attributes map
        # if (attributes['v_max'] is not None):                       # Velocity
        #     self.velocity = random.uniform(0, attributes['velo_max'])
        # if (attributes['s_max'] is not None):                       # Strength
        #     self.strength = random.uniform(0, attributes['str_max'])
        
        # # Evolutionary traits
        # self.see_food = False                                       # Can see food
        # self.vision = random.uniform(1, attributes['vis_max'])             # Vision
        # self.peripheral = random.uniform(90, attributes['perp_max'])       # Peripheral Vision
        # self.fitness = 0                                            # Fitness
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad)
        win.blit(self.text, (self.x-self.text.get_width()//2, self.y-self.text.get_height()//2))
        
    def is_full(self):
        if self.num_eaten >=self.FULL_AMOUNT:
            return True
        return False

    def move(self, xmax, ymax):
        self.x += random.uniform(-self.speed, self.speed)
        self.y += random.uniform(-self.speed, self.speed)
        # Set the bounds
        if self.x < 0: self.x = 0
        elif self.x > xmax: self.x = xmax
        if self.y < 0: self.y = 0
        elif self.y > ymax: self.y = ymax

        self.center = (self.x, self.y)

    def mouse_move(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]
    
    def get_distance(self, obj):
        dist = math.hypot(obj.x - self.x, obj.y-self.y)
        return dist
            
    def is_eating(self, obj):
        dist = self.get_distance(obj)
        if dist <= obj.rad + self.rad and self.rad > obj.rad*1.25:
            self.num_eaten+=1
            return True
        return False
    
    def reproduce(self):
        child = Organism(self.color, 
                        {'x_max':1, 'y_max':1}, 
                        (self.x+10, self.y+10),
                         self.speed * random.uniform(1-self.MUTATION_RATE, 1+self.MUTATION_RATE),
                         self.rad * random.uniform(1-self.MUTATION_RATE, 1+self.MUTATION_RATE)
                        )
        return child

    def think(self):
        pass