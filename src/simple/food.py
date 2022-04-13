import torch
import math

from math import uniform
        
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
    