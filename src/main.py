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
ts = ev3.TouchSensor()
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
    wheel_left = []
    wheel_right = []

    while True:
        odometry.check_phase()
        motor_left_value = (motor_left.position / 360)
        motor_right_value = (motor_right.position / 360)
        wheel_left.append(format(motor_left_value, ".2f"))
        wheel_right.append(format(motor_right_value, ".2f"))
        #print(wheel_left)
        #print(wheel_right)
        time.sleep(0.05)




# DO NOT EDIT
if __name__ == '__main__':
    run()
