#!/usr/bin/env python3

import logging
import os
import paho.mqtt.client as mqtt
import uuid
import ev3dev.ev3 as ev3
import time
from communication import Communication
from odometry import Odometry
from planet import Direction, Planet
import database
odometry = Odometry()

client = None  # DO NOT EDIT


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
    # Run the system loop for exploration

    # Setup objects for classes inside modules
    global p
    global c
    p = Planet()
    c = Communication(client, logger)

    # Run system loop for exploration
    system_loop()

"""
# Function to push all the sensor data into the database
def push_sensor_data():
    database.color_sensor_red_raw = cs.bin_data("hhh")[0]
    database.color_sensor_green_raw = cs.bin_data("hhh")[1]
    database.color_sensor_blue_raw = cs.bin_data("hhh")[2]

    database.color_sensor_red_rgb = cs.bin_data("hhh")[0] / 185
    database.color_sensor_green_rgb = cs.bin_data("hhh")[1] / 321
    database.color_sensor_blue_rgb = cs.bin_data("hhh")[2] / 157

    database.ultra_sonic_sensor = us.distance_centimeters
"""  


# System loop for running through all phases
def system_loop():
    odometry.start_driving()
    while True:

        """
        odometry.colorscan()
        """
        odometry.while_driving()
        if odometry.move_smooth():
            print("hallo")
            print(odometry.stop_driving())
            c.communication_phase()
            odometry.motor_left.run_to_rel_pos(position_sp=270)
            odometry.motor_right.run_to_rel_pos(position_sp=270)
            time.sleep(2)
            odometry.turn_around(350)
            odometry.start_driving()
        else:
            pass

        # Samplingrate for system loop ### 1/10 of a second


# DO NOT EDIT
if __name__ == '__main__':
    run()
