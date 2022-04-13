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
    x (int): the current x position of the organism on env_map
    y (int): the current y position of the organism on env_map
    velocity (int): the maximum velocity of the organism
    vision (int): how far the organism can see in the distance
    fitness (int): how much food the organism has consumed
    energy (int): the amount of energy the organism can utilize
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
        self.x = uniform(0, env_map['x_max'])                       # Starting X 
        self.y = uniform(0, env_map['y_max'])                       # Starting Y
        
        # Customizable traits for the user to select in their attributes map                
        self.velocity = uniform(0, attributes['velo_max'])  # Velocity
        
        # Evolutionary traits
        self.vision = uniform(1, attributes['vis_max'])             # Vision
        self.energy = uniform(20, 100)                              # Energy
        self.fitness = 0                                            # Fitness
        
    def think(self):
        """
        Runs the neural network to determine the organism's next output.
        """
        return
    