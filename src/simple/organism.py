# Organism
import math
import numpy as np
import random
import pygame

pygame.font.init()

SPEED = random.uniform(1, 3)

class Organism:
    FONT = pygame.font.SysFont('Comic Sans MS', 10)

    # FONT = pygame.font.SysFont('Comic Sans MS', 20)
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

    def __init__(self, color, env_map, mutation_rate, coords=None, range=None, speed=None, rad=None, settings=None, wih=None, who=None):
        """
        Initializes an organism object in a random.uniform (x, y) location on env_map.

        Parameters
        ----------
        attributes (dict): a dictionary of attributes to set the food with
        env_map (object): the environment with dimensions (x, y)
        name (str): the name of the organism, default is None
        """
        # Environmental starting traits
        self.mutation_rate = mutation_rate
        self.range = range if range != None else random.randrange(100, 800)
        self.paused = False
        self.color = color
        self.speed = speed if speed != None else SPEED
        self.speeds = [SPEED, 0.9 * SPEED, 0.8 * SPEED, 0.7 * SPEED,
                       0.6 * SPEED, 0.5 * SPEED, 0.4 * SPEED, 0.3 * SPEED,
                       0.2 * SPEED, 0.1 * SPEED, ]
        self.rad = rad if rad != None else random.uniform(10, 30)
        self.fitness = 0
        # View
        self.r = random.uniform(0, 360)
        # self.energy = 100000
        # self.energy_cost = self.get_energy_cost()

        if coords == None:
            self.x = random.randrange(
                0, env_map['x_max'])                       # Starting X
            self.y = random.randrange(
                0, env_map['y_max'])                       # Starting Y
        else:
            self.x = coords[0]
            self.y = coords[1]

        self.r_food = 0

        # Inner layer
        if wih is None:
            self.wih = np.random.uniform(-1, 1,
                                         (settings['hidden'], settings['input']))
        else:
            self.wih = wih

        # Outer layer
        if who is None:
            self.who = np.random.uniform(-1, 1,
                                         (settings['output'], settings['hidden']))
        else:
            self.who = who

        self.nn_direction = -1
        self.nn_velocity = 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad)
        #pygame.draw.circle(win, 'black', (self.x, self.y), self.range, 1)
        text = self.FONT.render(
            f'{round(self.speed, 2)} : {round(self.rad, 2)} : {round(self.fitness, 1)}', 1, 'black')
        win.blit(text, (self.x - text.get_width() //
                 2, self.y - text.get_height() // 2))

    def change_speed(self, new_speed):
        self.speed = new_speed

    ########################## NEURAL NETWORK  ##########################
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def relu(x):
        x = np.maximum(x, 0)
        x = x * (x > 0)
        x = (abs(x) + x) / 2
        return x

    # Update the organism's orientation and speed given its current vision
    def think(self):
        h1 = np.tanh(np.dot(self.wih, self.r_food))  # hidden layers
        out = np.tanh(np.dot(self.who, h1))          # output layer
       # print(out)
        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_direction = float(out[0])   # [-1, 1]  (left=1, right=-1)
        # print(self.nn_direction)

    # Move the organism in its current orientation
    def move(self, xmax, ymax):
        if not self.paused:
            # Update rotation
            self.r += self.nn_direction
            self.r = self.r % 360

            self.x += self.speed * math.cos(math.radians(self.r))
            self.y += self.speed * math.sin(math.radians(self.r))

            # Set the bounds
            if self.x < 0:
                self.x = 0
            elif self.x > xmax:
                self.x = xmax
            if self.y < 0:
                self.y = 0
            elif self.y > ymax:
                self.y = ymax

            self.center = (self.x, self.y)
   #######################################################################

    def length(self, x, y):
        return (x**2 + y**2) ** 0.5

    def norm(self, x, y):
        _len = self.length(x, y)
        return x / _len, y / _len

    def nearest_food(self, foods):
        pos = pygame.math.Vector2(self.x, self.y)
        if len(foods) > 0:
            closest_food = min([food for food in foods], key=lambda food: pos.distance_to(
                pygame.math.Vector2(food.x, food.y)))
            fx, fy = closest_food.x, closest_food.y
            dx, dy = self.x - fx, self.y - fy
            self.r_food = math.degrees(math.atan2(dy, dx))

    # def target_move(self, foods, xmax, ymax):
    #     if not self.paused and self.energy > 0:
    #         self.energy -= self.energy_cost
    #         pos = pygame.math.Vector2(self.x, self.y)
    #         closest_food = min([food for food in foods], key=lambda food: pos.distance_to(pygame.math.Vector2(food.x, food.y)))
    #         fx, fy = closest_food.x, closest_food.y
    #         dx, dy = fx - self.x, fy - self.y
    #         _len = self.length(dx, dy)
    #         direction = self.norm(dx, dy)
    #         if _len <= self.range:
    #             self.x += direction[0] * self.speed
    #             self.y += direction[1] * self.speed
    #         else:
    #             self.move(xmax, ymax)

    # def mouse_move(self):
    #     pos = pygame.mouse.get_pos()
    #     self.x = pos[0]
    #     self.y = pos[1]

    def get_distance(self, obj):
        dist = math.hypot(obj.x - self.x, obj.y - self.y)
        return dist

    def is_eating(self, obj):
        dist = self.get_distance(obj)
        if dist <= obj.rad + self.rad and self.rad > obj.rad * 1.25:
            self.fitness += obj.energy
            # self.energy+=100000
            return True
        return False

    def reproduce(self):
        # Update neural network weights
        wih_new = self.wih
        who_new = self.who

        # Mutate random row
        row = random.randrange(0, len(wih_new))
        wih_new[row] = wih_new[row] * \
            random.uniform(1 - self.mutation_rate, 1 + self.mutation_rate)
        row = random.randrange(0, len(who_new))
        who_new[row] = who_new[row] * \
            random.uniform(1 - self.mutation_rate, 1 + self.mutation_rate)

        # Create the child
        child = Organism(self.color,
                         {'x_max': 1, 'y_max': 1},
                         self.mutation_rate,
                         (self.x + 10, self.y + 10),
                         self.range *
                         random.uniform(1 - self.mutation_rate,
                                        1 + self.mutation_rate),
                         self.speed *
                         random.uniform(1 - self.mutation_rate,
                                        1 + self.mutation_rate),
                         self.rad *
                         random.uniform(1 - self.mutation_rate,
                                        1 + self.mutation_rate),
                         wih=wih_new, who=who_new
                         )
        return child

    # def get_energy_cost(self):
    #     energy_cost = 0.5 * self.rad * (self.speed**2)
    #     return energy_cost

    # def reset_energy(self):
    #     self.energy = 100000
