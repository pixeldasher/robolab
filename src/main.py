#!/usr/bin/env python3

# Import py modules
import logging
import uuid
import os
import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3
from time import sleep, time

# Import src modules
from odometry import Odometry
from communication import Communication
from planet import Direction, Planet

client = None  # DO NOT EDIT

#####################################################################################

# Initial function for main


def run():
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client = mqtt.Client(client_id=str(uuid.uuid4()),  # Unique Client-ID to recognize our program
                         clean_session=False,  # We want to be remembered
                         protocol=mqtt.MQTTv31  # Define MQTT protocol version
                         )
    log_file = os.path.realpath(__file__) + '/../../logs/project.log'
    logging.basicConfig(filename=log_file,  # Define log file
                        level=logging.DEBUG,  # Define default mode
                        # Define default logging format
                        format='%(asctime)s: %(message)s'
                        )
    logger = logging.getLogger('RoboLab')

    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.

    # Objects for classes of other modules
    global p, c, o
    p = Planet()
    o = Odometry()
    c = Communication(client, logger, p, o)

    p.explore_dict = {}

    # send test planet message
    #c.send_test_planet()

    # Reset wheels
    o.init_mov()

    # Run beginning loop for start up once
    while True:
        o.while_driving

        # First time movement
        if o.move_to_point():
            # ... move to point
            o.correct_pos()
            break

    # ... scan for possible paths
    o.scan()
    
    print(o.directions)

    # ... send ready message to mothership
    c.send_ready()

    # ... send the best path (chosen inside this function through a function in planet) to mothership
    print("vor pathselect:", p.explore_dict)
    c.send_path_select()

    # ... wait until last message is atleast 3 seconds old
    while (time() - c.time_offset < 3):
        pass

    # ... play a happy tune
    ev3.Sound.play_song(
        (('D4', 'e3'), ('D4', 'e3'), ('D4', 'e3'), ('G4', 'h')))

    # ... turn to the direction the algorithm or mothership has given the robot
    o.correct_dir()

    # ... continue driving
    o.init_mov()

    # Run system loop for exploration
    system_loop()

#####################################################################################

# System loop for map exploration


def system_loop():
    while True:
        # Movement function
        o.while_driving()

        # Follow line; if on station point, break out of oop
        if o.move_to_point():
            # ... move forward to the correct position on the station point
            o.correct_pos()

            # ... get data from odometry and save it
            o.save_data()

            # ... send collected data to mothership
            c.send_path()

            # ... update coords
            o.update_coords()

            # ... check if station point is already registered and if not: turn around and check all directions for possible paths
            #if (o.curr_x, o.curr_y) not in p.explore_dict:
            o.scan()
            #    print(o.directions)

            # ... send the best path (chosen inside this function through a function in planet) to mothership
            print(p.explore_dict)
            c.send_path_select()

            # ... wait until last message is atleast 3 seconds old
            while (time() - c.time_offset < 3):
                pass

            # ... turn to the direction the algorithm or mothership has given the robot
            o.correct_dir()
            
            # ... play a happy tune
            ev3.Sound.play_song(
                (('D4', 'e3'), ('D4', 'e3'), ('D4', 'e3'), ('G4', 'h')))

            # ... continue driving
            o.init_mov()

#####################################################################################


# DO NOT EDIT
if __name__ == '__main__':
    run()
