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

    background_image = pygame.image.load(r'C:\Users\lenovo\PycharmProjects\MyProjects\gravitation\Star-Field.jpg')

    win.blit(background_image, (0, 0))

    clock = pygame.time.Clock()
    FPS = 100  # желаните кадри в секунда
    clock.tick(FPS)
    win.blit(background_image, (0, 0))
    running = True
    frame = 0
    height = screen_height / 2
    width = screen_width / 2
    while running:
        frame += 1

        # Проверка за събития
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Изпълнение на игрова логика
        # win.fill((0,0,0))

        win.blit(background_image, (0, 0))
        # Изчисляване на новите положения на всички участващи тела
        # [b.signal_start_moments.append(frame) for b in bodies]

        body_access.calc_new_positions(frame, simultaneous_interaction, *bodies)
        # [b.position_history.append([b.x, b.y,len(bodies)-1]) for b in bodies]

        for body in bodies:
            if not simultaneous_interaction:
                body.x, body.y = body.fictional_position
                # body.x += body.velocity[0]
                # body.y +=  body.velocity[1]
                body.position_history.append([body.x, body.y, [], frame])
                if len(body.position_history[0][2]) == interacting_bodies_number:
                    del body.position_history[0]
            else:
                body.x += body.velocity[0]
                body.y += body.velocity[1]
            # Drawing the bodies at their new positions
            x_position = body.x + width

            y_position = height - body.y
            pygame.draw.circle(win, body.color, (x_position, y_position), body.radius)
   

            # Drawing points to trace body traejectories
            if trace_trajectories:
                length = len(body.position_history)
                trace_array = []
                if length > 200:
                    trace_array = body.position_history[length - 200:]
                for x, y, _, _ in trace_array:
                    pygame.draw.circle(win, body.color, (x, y), 1)

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
    
    # Orange body initial position
    orange_body_pos = np.array([900,200])
    
    # blue_body_velocity_vec = np.array([0, 0.3])
    
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
            blue_body_velocity_vec[1] = -0.01 
        
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
