# Organism 
import random
import pygame


class Organism:
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
    def __init__(self, env_map, name=None):
        """
        Initializes an organism object in a random.randrange (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        name (str): the name of the organism, default is None
        """
        # Environmental starting traits
        self.color = "red"
        self.rad = 15
        self.width = 20
        self.name = name                                            # Name
        self.r = random.randrange(0, 360)                                       # View
        self.x = random.randrange(0, env_map['x_max'])                       # Starting X 
        self.y = random.randrange(0, env_map['y_max'])                       # Starting Y
        
        # Customizable traits for the user to select in their attributes map
        # if (attributes['v_max'] is not None):                       # Velocity
        #     self.velocity = random.randrange(0, attributes['velo_max'])
        # if (attributes['s_max'] is not None):                       # Strength
        #     self.strength = random.randrange(0, attributes['str_max'])
        
        # # Evolutionary traits
        # self.see_food = False                                       # Can see food
        # self.vision = random.randrange(1, attributes['vis_max'])             # Vision
        # self.peripheral = random.randrange(90, attributes['perp_max'])       # Peripheral Vision
        # self.fitness = 0                                            # Fitness
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad, self.width)
        
    def move(self, xmax, ymax):
        self.x += random.randrange(-5, 6)
        self.y += random.randrange(-5, 6)
        # Set the bounds
        if self.x < 0: self.x = 0
        elif self.x > xmax: self.x = xmax
        if self.y < 0: self.y = 0
        elif self.y > ymax: self.y = ymax


    def think(self):
        pass