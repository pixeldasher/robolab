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


# Define movement functions
def move_straight():
    motor_left.speed_sp = 250
    motor_right.speed_sp = 250
    motor_left.command = "run-forever"
    motor_right.command = "run-forever"

    
def move_left():
    motor_left.speed_sp = 125
    motor_right.speed_sp = 250
    motor_left.command = "run-forever"
    motor_right.command = "run-forever"

    
def move_right():
    motor_left.speed_sp = 250
    motor_right.speed_sp = 125
    motor_left.command = "run-forever"
    motor_right.command = "run-forever"

    
def stop_moving():
    motor_left.speed_sp = 0
    motor_right.speed_sp = 0
    motor_left.command = "run-forever"
    motor_right.command = "run-forever"


def turn_around():
    motor_left.speed_sp = 400
    motor_right.speed_sp = -400
    motor_left.command = "run-forever"
    motor_right.command = "run-forever"
    time.sleep(1.075)
        


# Define phases
def check_phase():
    odometry.movement_check(odometry.touch_check(ts.value()) & odometry.distance_check(us.distance_centimeters))


# System loop for running through all phases
def system_loop():
    while True:
        check_phase()


# DO NOT EDIT
if __name__ == '__main__':
    run()
