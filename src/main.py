#!/usr/bin/env python3


import logging
import os
import paho.mqtt.client as mqtt
import uuid
import ev3dev.ev3 as ev3
import time
import database

import communication
import odometry
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

    # Setup communication variable in order to use it after import
    global comm
    comm = communication.Communication(client, logger)

    # Run the system loop for exploration
    system_loop()


### 

"""
# Define sensors
ts = ev3.TouchSensor()
us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()


# Define sensor modes
us.mode = 'US-DIST-CM'
cs.mode = 'RGB-RAW'

# Define motors
motor_left = ev3.LargeMotor("outA")
motor_right = ev3.LargeMotor("outB")
"""


# System loop for exploration
def system_loop():
    while True:
        #odometry.check_phase()
        #odometry.station_fider()

        # Start communication phase
        comm.comm_phase_init()

        # Samplingrate for system loop ### 1/10 of a second
        time.sleep(1/10)


# DO NOT EDIT
if __name__ == '__main__':
    run()
