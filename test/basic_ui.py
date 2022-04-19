import pygame
import pygame_gui

# Initialize pygame
pygame.init()

# Create an 800x600 display with a caption called 'Quick Start'
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

# Add a black background to the whole window
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

# Create a manager that will update the UI for each tick
manager = pygame_gui.UIManager((800, 600))

# Button!
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

# Clock that will update with each tick
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             s_running = False
             
        # Check if the button is pressed
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button: # Check the specific button!
                print('Hello World!')
             
        # Process all events and update them for the user to see
        manager.process_events(event)
        manager.update(time_delta)
        
    # Draw out the UI
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    
    # Update the display for the user
    pygame.display.update()