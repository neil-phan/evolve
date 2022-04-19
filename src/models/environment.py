# Organism 
import torch
import math

from math import uniform

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
    def __init__(self, attributes, env_map, name=None):
        """
        Initializes an organism object in a random (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        name (str): the name of the organism, default is None
        """
        # Environmental starting traits
        self.name = name                                            # Name
        self.r = uniform(360)                                       # View
        self.x = uniform(0, env_map['x_max'])                       # Starting X 
        self.y = uniform(0, env_map['y_max'])                       # Starting Y
        
        # Customizable traits for the user to select in their attributes map
        if (attributes['v_max'] is not None):                       # Velocity
            self.velocity = uniform(0, attributes['velo_max'])
        if (attributes['s_max'] is not None):                       # Strength
            self.strength = uniform(0, attributes['str_max'])
        
        # Evolutionary traits
        self.see_food = False                                       # Can see food
        self.vision = uniform(1, attributes['vis_max'])             # Vision
        self.peripheral = uniform(90, attributes['perp_max'])       # Peripheral Vision
        self.fitness = 0                                            # Fitness
        
class Food:
    """
    Generated food in the environment for the organisms to feed on.
    Is able to respawn after a certain amount of time.
    
    Attributes
    ----------
    x (int): the current x position of the food
    y (int): the current y position of the food
    energy (int): the amount of fitness the food gives to the organism
    can_eat (bool): determines if the food is visible to the organism
    
    """
    def __init__(self, attributes, env_map):
        """
        Initializes a food object in a random (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        """
        self.x = uniform(attributes['x_min'], attributes['x_max'])  # Starting X
        self.y = uniform(attributes['y_min'], attributes['y_max'])  # Starting Y
        self.energy = uniform(1, attributes['food_max'])
        self.can_eat = 1


    def respawn(self, attributes):
        """
        Respawn the food object in a random (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        """
        self.x = uniform(attributes['x_min'], attributes['x_max'])
        self.y = uniform(attributes['y_min'], attributes['y_max'])
        self.energy = uniform(1, attributes['food_max'])
        self.can_eat = 1
    