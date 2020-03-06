#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import logging
import os
import paho.mqtt.client as mqtt
import uuid
import time

import odometry
from communication import Communication
from odometry import Odometry
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

ts = ev3.TouchSensor()
ts.value()
us = ev3.UltrasonicSensor()
us.mode = 'US-DIST-CM'
distance = us.value()
cs = ev3.ColorSensor()
ev3.Sound.beep()
cs.mode = 'COL-COLOR'
m = ev3.LargeMotor("outA")
m2 = ev3.LargeMotor("outB")

while True:
     odometry.colorcheck(cs.value())
     odometry.distancecheck(us.distance_centimeters)
     odometry.touchcheck(ts.value())


# DO NOT EDIT
if __name__ == '__main__':
    run()

