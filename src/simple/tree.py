import math
import random
import pygame
     
class Tree:   
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
    def __init__(self, attributes):
        """
        Initializes a food object in a random (x, y) location on env_map.
        
        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        """
        self.color = "brown"
        self.rad = 20   #   Radius from the center
        self.width = 20  #   Width of the circle outline
        self.x = random.randrange(0, attributes['x_max'])  # Starting X
        self.y = random.randrange(0, attributes['y_max'])  # Starting Y
        self.center = (self.x, self.y)
        
    def draw(self, win):
        pygame.draw.circle(win, self.color, self.center, self.rad, self.width)
        
    
        