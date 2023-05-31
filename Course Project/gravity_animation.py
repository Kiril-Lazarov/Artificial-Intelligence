import numpy as np 
import pygame 
from body import Body


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