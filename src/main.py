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
    global p, c, o
    p = Planet()
    o = Odometry()
    c = Communication(client, logger, p, o)

    # Run system loop for exploration
    system_loop()


# System loop for running through all phases
def system_loop():
    o.start_driving()
    
    while True:
        # Movement function
        o.while_driving()
        

        if o.move_smooth():
            o.motor_left.run_to_rel_pos(position_sp=160, speed_sp = 90)
            o.motor_right.run_to_rel_pos(position_sp=160, speed_sp = 90)
            sleep(0.01)
            o.motor_left.wait_until_not_moving()

            o.turn_around(170)
            """
            # ... send ready message, only works once
            c.send_ready()

            # ... move forward in order to not scan the same station twice
            o.motor_left.run_to_rel_pos(position_sp=160, speed_sp = 90)
            o.motor_right.run_to_rel_pos(position_sp=160, speed_sp = 90)
            sleep(0.01)
            o.motor_left.wait_until_not_moving()

            # ... get data from odometry and save it
            o.stop_driving()

            # ... send collected data to mothership
            c.send_path()

            # ... turn around and check all directions for possible paths
            o.scan()

            # ... send the best path (chosen inside this function through a function in planet) to mothership
            c.send_path_select()
            
            # ... play a happy tune
            ev3.Sound.play_song((('D4', 'e3'),( 'D4', 'e3'), ('D4', 'e3'), ('G4', 'h')))

            # ... continue driving
            o.start_driving()
            """


# DO NOT EDIT
if __name__ == '__main__':
    run()
