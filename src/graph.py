from re import I
import pygame

class Graph():
    FONT = pygame.font.SysFont('Comic Sans MS', 15)
    SUB_FONT = pygame.font.SysFont('Comic Sans MS', 11)

    def __init__(self, win, bounds):
        self.win = win
        self.x_bounds = bounds[0]
        self.y_bounds = bounds[1]
        self.width = self.x_bounds[1] - self.x_bounds[0]
        self.height = self.y_bounds[1] - self.y_bounds[0] 
        self.speed_vals = []
        self.size_vals = []
        self.num_vals = 0
        self.step_size = 0
    
    def find_max_y(self):
        max_y = -1
        for val in self.values:
            if val > max_y: max_y = val
        return max_y   
    
    def draw(self):
        start_x = self.x_bounds[0]
        end_x = self.x_bounds[1]
        start_y = self.y_bounds[0]
        end_y = self.y_bounds[1]

        # AXES
        xaxis_text = self.SUB_FONT.render('Generation', False, 'black')
        yaxis_text = self.SUB_FONT.render('Relative Amount', False, 'black')
        yaxis_text_rect = yaxis_text.get_rect(bottomleft=(self.x_bounds[0]+15, self.y_bounds[1]+20))
        xaxis_text_rect = xaxis_text.get_rect(midbottom=(self.x_bounds[0]+self.width//2 + 10, self.y_bounds[0]+3))
        self.win.blit(xaxis_text, xaxis_text_rect)
        self.win.blit(yaxis_text, yaxis_text_rect)
        pygame.draw.line(self.win, 'black', (start_x+10, start_y-10), (end_x-10, start_y-10), 2)
        pygame.draw.line(self.win, 'black', (start_x+10, start_y-10), (start_x+10, end_y+10), 2)

        # LEGEND
        speed_text = self.FONT.render('Speed', False, 'green')
        size_text = self.FONT.render('Size', False, 'red')
        speed_text_rect = speed_text.get_rect(topright=(self.x_bounds[1]-10, self.y_bounds[1]+10))
        size_text_rect = size_text.get_rect(topright=(self.x_bounds[1]-10, self.y_bounds[1]+25))
        self.win.blit(speed_text, speed_text_rect)
        self.win.blit(size_text, size_text_rect)

        # DRAW POINTS
        self.plot_vals()
    
    def plot_vals(self):
        if self.num_vals > 0:
            # try and except was put in place because there was a bug where generating a new simulation,
            # while the graph was trying to plot caused an out of bounds error, as generation simulation
            # cleared the values in the graph
            try:
                for i in range(self.num_vals):
                    x = i * self.step_size + self.x_bounds[0] + 10
                    speed_y = self.y_bounds[0] - self.speed_vals[i] - 10
                    size_y = self.y_bounds[0] - self.size_vals[i] - 10
                    speed_point = (x, speed_y)
                    size_point = (x, size_y)
                    pygame.draw.circle(self.win, 'green', speed_point, 2)
                    pygame.draw.circle(self.win, 'red', size_point, 2)
            except:
                return
    
    def add_point(self, speed, size):
        self.speed_vals.append(speed)
        self.size_vals.append(size)
        self.num_vals+=1
        self.step_size = self.find_step_size()
    
    def find_step_size(self):
        return self.width // self.num_vals



