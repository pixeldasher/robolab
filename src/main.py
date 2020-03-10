#!/usr/bin/env python3

import logging
import os
import paho.mqtt.client as mqtt
import uuid
import ev3dev.ev3 as ev3
import time

import odometry
from communication import Communication
#from odometry import Odometry
from planet import Direction, Planet

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

    system_loop()

    """
    comm = Communication(client, logger)
    comm.send_ready_message()
    """
    

# Define sensors
us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()


# Define sensor modes
us.mode = 'US-DIST-CM'
cs.mode = 'RGB-RAW'


# Define motors
motor_left = ev3.LargeMotor("outA")
motor_right = ev3.LargeMotor("outB")


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
            time.sleep(1)
            motor_left.run_to_rel_pos(position_sp=270)
            motor_right.run_to_rel_pos(position_sp=270)
            time.sleep(3)
            odometry.start_driving()
        else:
            pass


# DO NOT EDIT
if __name__ == '__main__':
    run()
