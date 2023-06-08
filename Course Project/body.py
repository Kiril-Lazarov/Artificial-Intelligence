import numpy as np
import math


class Body:
    # `Gravitational` constant.Can be the real value or free choice
    G = 0.004

    signal_speed = 5

    def __init__(self, x, y, mass, radius=0.2, color=(250, 250, 250)):
        self.x = x
        self.y = y

        # Virtual position of the object, which will be used solely for
        # calculations and will be entered as a new actual position after the calculations are completed
        self.fictional_position = np.array([x, y])
        
        self.mass = mass
        self.radius = radius
        self.color = color
        self.velocity = np.array([0, 0])        
        self.position_history = [[x, y, [], 0]]


    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    # This method integrates the gravitational acceleration to find the instantaneous velocity.
    @staticmethod
    def integrate_acceleration(M, r):
        return Body.G * M / r 

    # This method calculates the distance between the two objects,
    # based on which it computes the gravitational acceleration generated by the gravitational field of the body at that point,
    # finds the instantaneous velocity created by that acceleration (calculating the first derivative),
    # and adds the vector of the instantaneous velocity to the current velocity vector of the body that consumes the gravitational signal.   
    @staticmethod
    def vectors_calculations(body, other_object_x, other_object_y, other_object_mass, simultaneous_interaction):
        if simultaneous_interaction:
            dist = body.distance([body.x, body.y], [other_object_x, other_object_y])
            
            dist_vector = np.array([other_object_x - body.x, other_object_y - body.y])
        else:
            dist = body.distance([body.fictional_position[0], body.fictional_position[1]],
                                 [other_object_x, other_object_y])
    
            dist_vector = np.array([other_object_x - body.fictional_position[0], other_object_y - body.fictional_position[1]])
        
        first_deriv = body.integrate_acceleration(other_object_mass, dist)
        velocity_vector = np.array(dist_vector * first_deriv)

        body.velocity = body.velocity + velocity_vector

    @staticmethod
    def find_signal_coordinates(body, other_body, body_x_position, body_y_position, frame, index):
       
        x_diff = body_x_position - other_body.position_history[index][0]
        y_diff = body_y_position - other_body.position_history[index][1]
        
        # The slope between curr position of the body and the point where signal is emmited
        slope = body.slope(x_diff, y_diff)
        
        time_interval = frame - other_body.position_history[index][3]
        
        distance_traveled_by_signal = body.signal_speed * time_interval
        
        # A slope to be `None` means that the velocity of the body is zero.
        if slope is None:
            return body_x_position, body_y_position
        
        if slope == 'inf':
            signal_x = other_body.position_history[index][0]
            if other_body.position_history[index][1] > body_y_position:
                distance_traveled_by_signal *= -1
            signal_y = other_body.position_history[index][1] + distance_traveled_by_signal
            
        elif slope == 0:
            if other_body.position_history[index][0] > body_x_position:
                distance_traveled_by_signal *= -1
            signal_x = other_body.position_history[index][0] + distance_traveled_by_signal
            signal_y = other_body.position_history[index][1]
            
        else:
            if slope > 0:
                if other_body.position_history[index][0] > body_x_position:
                    distance_traveled_by_signal *= -1
            if slope < 0:
                if other_body.position_history[index][0] < body_x_position:
                    distance_traveled_by_signal *= -1
                    
            # Angle between curr body position and the position of the signal`s origin in radians      
            angle_rad = math.atan(slope)
            
            if angle_rad < 0:
                distance_traveled_by_signal *= -1
                
            signal_x = other_body.position_history[index][0] + math.cos(angle_rad) * distance_traveled_by_signal
            signal_y = other_body.position_history[index][1] + math.sin(angle_rad) * distance_traveled_by_signal

        return signal_x, signal_y

    @staticmethod
    def slope(x_length, y_length):
        if x_length == 0 and y_length == 0:
            return None
        if x_length == 0:
            return 'inf'
        elif y_length == 0:
            return 0
        return y_length / x_length

    @staticmethod
    def find_const(slope, point):
        x, y = point
        if slope == 'inf' or slope is None:
            return None
        return y - x * slope

    # Calculates point of intersection between the signal and the path of the body
    @staticmethod
    def find_point_of_intersection(body, body_curr_coords, body_next_coords,
                                   signal_next_coords, signal_curr_coords):
        # If the body is not move the point of intersection is the position of the body
        if body_curr_coords == body_next_coords:
            return body_curr_coords

        body_slope = body.slope(body_next_coords[0] - body_curr_coords[0],
                                body_next_coords[1] - body_curr_coords[1])
        signal_slope = body.slope(signal_next_coords[0] - signal_curr_coords[0],
                                  signal_next_coords[1] - signal_curr_coords[1])
        
        
        # Different formulas for calculating the point of intersection in all combinations 
        # between the slopes of the body and the signal.
        if body_slope == 'inf' and signal_slope == 'inf':
            x_intersect = body_curr_coords[0]
            y_intersect = (body_curr_coords[1] * body.signal_speed -
                           signal_curr_coords[1] * body.velocity[1])/ (body.signal_speed - body.velocity[1])
            return x_intersect, y_intersect

        if body_slope == 'inf':
            x_intersect = body_curr_coords[0]
            signal_const = body.find_const(signal_slope, [signal_next_coords[0], signal_next_coords[1]])
            y_intersect = signal_slope * x_intersect + signal_const
            return x_intersect, y_intersect

        if body_slope == 0:            
            y_intersect = body_curr_coords[1]
            if signal_slope == 0:
                x_intersect = body_curr_coords[0]
            elif signal_slope == 'inf':
                x_intersect = signal_curr_coords[0]
            else:
                signal_const = body.find_const(signal_slope, [signal_curr_coords[0], signal_curr_coords[1]])
                x_intersect = (y_intersect - signal_const) / signal_slope
            return x_intersect, y_intersect
        
        if signal_slope == 'inf':
            x_intersect = signal_curr_coords[0]
            body_const = body.find_const(body_slope, [body_curr_coords[0], body_curr_coords[1]])
            y_intersect = body_slope * x_intersect + body_const
            return x_intersect, y_intersect
        
        if signal_slope == 0:
            y_intersect = signal_curr_coords[1]
            body_const = body.find_const(body_slope, [body_curr_coords[0], body_curr_coords[1]])
            x_intersect = (y_intersect - body_const) / body_slope
            return x_intersect, y_intersect
        
        body_const = body.find_const(body_slope, [body_curr_coords[0], body_curr_coords[1]])
        signal_const = body.find_const(signal_slope, [signal_curr_coords[0], signal_curr_coords[1]])

        x_intersect = (signal_const - body_const) / (body_slope - signal_slope)
        y_intersect = body_slope * x_intersect + body_const

        return x_intersect, y_intersect

    @staticmethod
    def calc_new_positions(frame, simultaneous_interaction, *bodies):
        for body in bodies:
            for other_body in bodies:
                if body != other_body:
                    if simultaneous_interaction:
                        body.vectors_calculations(body, other_body.x, other_body.y,
                                                  other_body.mass, simultaneous_interaction)
                    else:
                        for index in range(len(other_body.position_history)):
                            
                            # Checks if the object has interacted with this signal, and if not,
                            # initiates a procedure to determine if it could.
                            if body not in other_body.position_history[index][2]:                            

                                # Distance between next position of the body and position
                                # where gravitational signal was emmited
                                body_next_position_x, body_next_position_y = body.fictional_position + body.velocity

                                next_dist = body.distance([body_next_position_x, body_next_position_y],
                                                          [other_body.position_history[index][0],
                                                           other_body.position_history[index][1]])

                                # The time interval between the moment of emission of the gravitational signal and
                                # the next moment measured using corresponding frame numbers.
                                next_time_interval = frame + 1 - other_body.position_history[index][3]

                                # The distance between the current position of the body and the next position
                                # of the gravitational signal.
                                signal_to_body_distance = next_dist - body.signal_speed * next_time_interval

                                # If the distance is less than zero (which means that the gravitational
                                # signal has reached the body).
                                if signal_to_body_distance <= 0:
                                    
                                    # Calculate current frame coordinates of the signal
                                    signal_curr_coords = body.find_signal_coordinates(body, other_body, body.x,
                                                                                      body.y, frame, index)
                                    
                                    # Checks if the current signal has passed the body, and if it has passed,
                                    # it calculates the coordinates of the current and previous signal.
                                    if abs(signal_to_body_distance) >= body.signal_speed:
                                        
                                        # Calculates coordinates of the signal for previous frame
                                        signal_previous_coords = body.find_signal_coordinates(body, other_body,
                                                                                              body.x, body.y,
                                                                                              frame - 1, index)
                                        # Calculates point of intersection between curr and previous signals and the
                                        # body path
                                        body.fictional_position = np.array(
                                            body.find_point_of_intersection(body, (body.x, body.y),
                                                                            (body_next_position_x, body_next_position_y),
                                                                            signal_curr_coords, signal_previous_coords))
                                                                            
                                
                                    else:
                                        # Calculate coordinates of the signal for next frame
                                        signal_next_coords = body.find_signal_coordinates(body, other_body,
                                                                                          body_next_position_x,
                                                                                          body_next_position_y,
                                                                                          frame + 1, index)

                                        body.fictional_position = np.array(
                                            body.find_point_of_intersection(body, (body.x, body.y),
                                                                            (body_next_position_x, body_next_position_y),
                                                                            signal_next_coords, signal_curr_coords))
                                        
                                    # These are coordinates of the position where signal was emmited
                                    signal_origin_x = other_body.position_history[index][0]
                                    signal_origin_y = other_body.position_history[index][1]

                                    body.vectors_calculations(body, signal_origin_x, signal_origin_y,
                                                              other_body.mass, simultaneous_interaction)

                                    other_body.position_history[index][2].append(body)
                               
                                    break
                                
                                else:
                                    break
            body.fictional_position = body.fictional_position + body.velocity