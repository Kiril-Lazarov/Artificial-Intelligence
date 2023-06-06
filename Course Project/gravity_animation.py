import numpy as np 
import pygame 
from body import Body
import time
import math

def animation(interacting_bodies_number, *bodies, simultaneous_interaction=False, trace_trajectories=False,
              screen_width=1500, screen_height=800):
    
    # Variable for accessing the Body class.
    body_access = bodies[0]
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height))

    prefix = 'Non-simultaneous' if not simultaneous_interaction else 'Simultaneous'
    
    pygame.display.set_caption(f'{prefix} gravitational interaction')
    
    background_image = pygame.image.load(r'C:\Users\lenovo\PycharmProjects\MyProjects\gravitation\Star-Field.jpg')

    win.blit(background_image, (0, 0))

    clock = pygame.time.Clock()
    
    # Frames per second
    FPS = 100  
    clock.tick(FPS)
    win.blit(background_image, (0, 0))
    running = True
    
    frame = 0
    height = screen_height / 2
    width = screen_width / 2
    
    while running:
        frame += 1

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not trace_trajectories:
            win.blit(background_image, (0, 0))
        
        # Calculate the new postions of all bodies
        body_access.calc_new_positions(frame, simultaneous_interaction, *bodies)

        for body in bodies:
            if not simultaneous_interaction:
                
                body.x, body.y = body.fictional_position
                body.position_history.append([body.x, body.y, [], frame])
                
                if len(body.position_history[0][2]) == interacting_bodies_number:
                    del body.position_history[0]
            else:
                body.x += body.velocity[0]
                body.y += body.velocity[1]
                
            # Transforming the Cartesian coordinates of positions into the Pygame coordinate system.
            x_position = body.x + width
            y_position = height - body.y
            pygame.draw.circle(win, body.color, (x_position, y_position), body.radius)
            
        # Refreshing the screen
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()

    # Exit
    pygame.quit()
    
def еxplanatory_animation1(screen_width=1500, screen_height=800, moving_bodies=False):
    center = (screen_width/2, screen_height/2)
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height)) 
    bg_color = (255, 255, 255)
    
    pygame.display.set_caption('Expanding gravitational signal')
    
    # Orange body initial position
    orange_body_pos = np.array([900,200])
    
    # The slope of the line connecting the orange and blue bodies.
    slope = (center[1]-orange_body_pos[1])/(orange_body_pos[0] - center[0])
   
    # slope =(200/150)
 
    angle_rad = math.atan(slope)
    
    # The velocity vector with which the orange body will start moving 
    # towards the blue body when the gravitational signal from the blue body reaches it.
    velocity_vec = np.array([-math.cos(angle_rad),math.sin(angle_rad)]) * 0.5
 
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    FPS = 100 # frames per second
    clock.tick(FPS)
 
    running = True
    frame = 0

    while running:
        frame += 1
        
        # Check for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        win.fill(bg_color)
       
        pygame.draw.circle(win, (0,0,250), center, frame)
        pygame.draw.circle(win, (250,250,250), center, frame-2)
        pygame.draw.circle(win, (0,0,250), center, radius = 10)
        
        if frame < 250:
            pygame.draw.circle(win, (255, 165, 0), (900,200), radius = 7)
        else:
            orange_body_pos = orange_body_pos + velocity_vec
            pygame.draw.circle(win, (255, 165, 0), orange_body_pos, radius = 7)
            
        text = font.render(f'Frame number {frame}', True, (0,0,0))
        
        # Refreshing the screen
        win.blit(text, (10, 10))
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
        
        # End of test animation
        if  frame == 780:
            running = False
    # Exit
    pygame.quit()
    
def еxplanatory_animation2(screen_width=1500, screen_height=800):
    
    center = (screen_width/2, screen_height/2)
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height)) 
    bg_color = (255, 255, 255)    
    
    pygame.display.set_caption('Dinamicaly interacting bodies')
    
    # Blue body initial position
    blue_body_pos = np.array([700,350])
    blue_body_velocity_vec = np.array([0.25, 0.25])
    
   
    # Orange body initial position
    orange_body_pos = np.array([900,200])
    
    # The slope of the line connecting the orange body to the point from which 
    # the blue body emits a gravitational signal.
    slope = (center[1]-orange_body_pos[1])/(orange_body_pos[0] - center[0])   
     
    angle_rad = math.atan(slope)
    
    # The velocity vector with which the orange body will start moving 
    # towards the blue body when the gravitational signal from the blue body reaches it.
    orange_body_velocity_vec = np.array([-math.cos(angle_rad),math.sin(angle_rad)]) * 0.5  
    
 
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    FPS = 100 # frames per second
    clock.tick(FPS)
 
    running = True
    frame = 0

    while running:
        frame += 1
        
        # Check for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        win.fill(bg_color)
      
            
        if frame >= 200:
          
            pygame.draw.circle(win, (0,0,250), center, frame-200)
            pygame.draw.circle(win, (250,250,250), center, frame-202)
            if frame < 550:
                pygame.draw.circle(win, (0,0,250), center, radius = 1)
        
        if frame >= 550:
            
            pygame.draw.circle(win, (255, 165, 0), (870,240), frame-550)
            pygame.draw.circle(win, (250,250,250), (870,240), frame-552)
            pygame.draw.circle(win, (255, 165, 0), (870,240), radius = 1)
            pygame.draw.circle(win, (0,0,250), center, radius = 1)
            
        if frame < 450:
            pygame.draw.circle(win, (255, 165, 0), orange_body_pos, radius = 7)
        else:
            # Updating the position of the orange object after it is reached by 
            # the gravitational signal emitted by the blue object.
            orange_body_pos = orange_body_pos + orange_body_velocity_vec
            pygame.draw.circle(win, (255, 165, 0), orange_body_pos, radius = 7)
        
        # Change in the velocity vector of the blue body after it is influenced
        # by the gravitational signal from the orange body.
        if frame == 888:
            blue_body_velocity_vec[1] = -0.5 
        
        # Update blue body position
        blue_body_pos = blue_body_pos + blue_body_velocity_vec   
        pygame.draw.circle(win, (0,0,250), blue_body_pos, 10)      
            
        text = font.render(f'Frame number {frame}', True, (0,0,0))
    
        #Refreshing the screen
        win.blit(text, (10, 10))
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
        
        # End of test animation
        if  frame == 1700:
            running = False
    # Exit
    pygame.quit()

    
def signal_trajectory_animation(screen_width = 1500,screen_height = 800):  
    
    center = (screen_width / 2, screen_height / 2)
    
    signal_positions_history = []
    
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height))
    bg_color = (255, 255, 255)

    pygame.display.set_caption('Signal trajectory')
    
    # Blue body position
    blue_body_pos = np.array([center[0] - 200, center[1] + 100])

    # Orange body initial position
    orange_body_pos = np.array([950, center[1] + 100])

    orange_body_velocity_vec = np.array([0, -0.5])

    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    
    # frames per second
    FPS = 100  
    clock.tick(FPS)

    running = True
    frame = 0

    while running:
        frame += 1

        # Check for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(bg_color)

        # Update the spreading gravitational signal circle
        pygame.draw.circle(win, (0, 0, 250), (blue_body_pos[0], blue_body_pos[1]), frame)
        pygame.draw.circle(win, (250, 250, 250), (blue_body_pos[0], blue_body_pos[1]), frame - 2)

        # Update orange body position
        orange_body_pos = orange_body_pos + orange_body_velocity_vec

        # The slope of the line between blue and orange bodies
        slope = (blue_body_pos[1] - orange_body_pos[1]) / (blue_body_pos[0] - orange_body_pos[0])

        angle_rad = math.atan(slope)

        signal_x = blue_body_pos[0] + frame * math.cos(angle_rad)
        signal_y = blue_body_pos[1] + frame * math.sin(angle_rad)

        signal_position = np.array([signal_x, signal_y])

        signal_positions_history.append(signal_position)

        for position in signal_positions_history:
            pygame.draw.circle(win, (125, 125, 125), (position[0], position[1]), 1)

        # Draw signal point 
        pygame.draw.circle(win, (125, 125, 125), signal_position, 5)

        if frame < 462:
            # Draw connecting line between blue and orange bodies
            pygame.draw.line(win, (0, 0, 250), blue_body_pos, orange_body_pos, 1)
        else:
            # Draw connecting line between blue body and gravitational signal
            pygame.draw.line(win, (0, 0, 250), blue_body_pos, signal_position, 1)

        pygame.draw.circle(win, (255, 165, 0), orange_body_pos, 7)

        # Draw blue body
        pygame.draw.circle(win, (0, 0, 250), blue_body_pos, 10)

        text = font.render(f'Frame number {frame}', True, (0, 0, 0))

        # Refreshing the screen
        win.blit(text, (10, 10))
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()

        # End of test animation
        if frame == 1000:
            running = False
    # Exit
    pygame.quit()
    
    
def expanding_spiral_animation(screen_width = 1500,screen_height = 800):   
    
    
    # Signal speed in pixels by frame
    signal_speed = 80   
  

    center = (screen_width / 2, screen_height / 2)
    
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height))
    bg_color = (255, 255, 255)

    pygame.display.set_caption('Expanding spiral')
    
    # Blue body position
    blue_body_pos = np.array([center[0] - 200, center[1] + 100])

    # Orange body position 0
    orange_body_pos_0 = np.array([950, center[1] + 100])
    
    # Orange body position 1
    orange_body_pos_1 = np.array([950, center[1]])
    
    # Orange body position 2
    orange_body_pos_2 = np.array([950, center[1] - 100])
    
    # Orange body position 3
    orange_body_pos_3 = np.array([950, center[1] - 200])

    orange_body_position_list = [orange_body_pos_0, orange_body_pos_1, orange_body_pos_2, orange_body_pos_3]
    
    orange_body_velocity_vec = np.array([0, -0.5])

    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    FPS = 100  # frames per second
    clock.tick(FPS)

    running = True
    frame = 0

    while running:
        frame += 1
   
        # Check for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(bg_color)
        
        moment_position = 0
        signal_x = 0
        signal_y = 0
        signal_speed += frame * 0.001        
        
        # Draw descreet postions of signal and orange body
        for position in orange_body_position_list:
            moment_position += 1
           
            # Draw orange body frames positions
            pygame.draw.circle(win, (255, 165, 0), position, 7)
            
            # The slope of the line between blue and orange body
            slope = (blue_body_pos[1] - position[1]) / (blue_body_pos[0] - position[0])

            angle_rad = math.atan(slope)
            if moment_position > 1:
                coefficient = (moment_position -1)*signal_speed
                signal_x = blue_body_pos[0] + coefficient * math.cos(angle_rad)
                signal_y = blue_body_pos[1] + coefficient * math.sin(angle_rad)
            
            pygame.draw.circle(win, (125, 125, 125), (signal_x, signal_y), 5)           
            pygame.draw.line(win, (125, 125, 125), blue_body_pos, position, 1)
    
        # Settings for signal and body to track the signal trajectory.
        orange_fictional_init_position = orange_body_pos_0
        curr_orange_body_velocity_vec = orange_body_velocity_vec
        curr_signal_speed = signal_speed * 0.005     
        
        
        # Tracing the signal`s trajectory for this value of the signal speed
        for fict_frame in range(700):            
           
            # Update orange body position
            orange_fictional_init_position = orange_fictional_init_position + curr_orange_body_velocity_vec
            
            slope = (blue_body_pos[1] - orange_fictional_init_position[1]) / (blue_body_pos[0] - orange_fictional_init_position[0])
            
            angle_rad = math.atan(slope)
            
            coefficient = fict_frame * curr_signal_speed
            
            x = blue_body_pos[0] + coefficient * math.cos(angle_rad)
            y = blue_body_pos[1] + coefficient *  math.sin(angle_rad) 
            
            pygame.draw.circle(win, (125, 125, 125), (x,y), 1)
        
        # Draw blue body
        pygame.draw.circle(win, (0, 0, 250), blue_body_pos, 10)

        pygame.draw.line(win, (255, 165, 0), orange_body_pos_0, orange_body_pos_3, 1)
        
        text = font.render(f'Frame number {frame}', True, (0, 0, 0))

        # Show frame number for position of the orange body
        for index in range(4):
            info = font.render(f'Frame {index}', True, (0, 0, 0))
            x, y = orange_body_position_list[index]
            
            win.blit(info, (x + 20, y))
            
        # Refreshing the screen
        win.blit(text, (10, 10))
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
        
        if frame == 1500:
            running = False
       
    # Exit
    pygame.quit()