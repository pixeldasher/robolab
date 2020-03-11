#!/usr/bin/env python3

# Import py modules
import logging
import uuid
import os
import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3
from time import sleep

# Import src modules
from odometry import Odometry
from communication import Communication
from planet import Direction, Planet
from database import Database

client = None  # DO NOT EDIT


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
                        format='%(asctime)s: %(message)s'  # Define default logging format
                        )
    logger = logging.getLogger('RoboLab')


    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.

    # Objects for classes of other modules
    global p, c, d, o
    p = Planet()
    c = Communication(client, logger)
    d = Database()
    o = Odometry()

    # Run system loop for exploration
    system_loop()


# System loop for running through all phases
def system_loop():
    o.start_driving()

    while True:
        # Add all sensor data to database# Movement function
        o.while_driving()

        # If stations has been reached:
        if o.move_smooth():
            # ... send ready message, only works once
            c.send_ready()

            # ... move forward in order to not scan the same station twice
            o.motor_left.speed_sp = 360
            o.motor_right.speed_sp = 360
            sleep(1)

            # ... get data from odometry and save it to database
            o.stop_driving()

            # ... send collected data to mothership
            c.send_path()

            # ... turn around and check all directions for possible paths
            #o.scan_directions()
            o.turn_around(360)

            # ... take all directions and put them int planet data
            p.add_vertex(d.vert, d.directions)
            
            # ... add the corrected path to planet data
            p.add_path(d.latest_path_start, d.latest_path_end, d.latest_path_weight)

            # ... replace old start coordinates and direction with current end coordinates and direction
            d.update_start_coords()

            # ... select the next direction, check if the target has been reached
            if p.select_direction((d.start_x, d.start_y), d.target) == None:
                c.send_target_reached()
            
            if not p.select_direction((d.start_x, d.start_y), d.target) == None:
                d.next_direction = p.select_direction((d.start_x, d.start_y), d.target)
            
            # Check if exploration is completed
            if p.explore_dict == {}:
                c.send_exploration_completed()

            # ... send selected path choice to mothership
            c.send_path_select()

            # ... turn to the selected direction if one was given
            if type(d.next_direction) == int:
                o.turn_around((d.start_dir - d.next_direction) % 360)

            # ... play a happy tune
            ev3.Sound.play_song((('D4', 'e3'),( 'D4', 'e3'), ('D4', 'e3'), ('G4', 'h')))

            # ... continue driving
            o.start_driving()


        # Samplingrate for system loop ### 1/10 of a seconds
        sleep(1/10)


# DO NOT EDIT
if __name__ == '__main__':
    run()
