#!/usr/bin/env python3

# Module imports
import logging
import os
import paho.mqtt.client as mqtt
import uuid
import ev3dev.ev3 as ev3
import time

# File imports
import communication
import odometry
import planet
import database

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
    p = planet.Planet()
    c = communication.Communication(client, logger)

    # Run system loop for exploration
    system_loop()


# Define sensor variables
us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()

# Set sensor modes
us.mode = 'US-DIST-CM'
cs.mode = 'RGB-RAW'

# Assign motors to corresponding port on device
motor_left = ev3.LargeMotor("outA")
motor_right = ev3.LargeMotor("outB")

# Default moving speed value
database.motor_speed = 250


# Function to push all the sensor data into the database
def push_sensor_data():
    database.color_sensor_red_raw = cs.bin_data("hhh")[0]
    database.color_sensor_green_raw = cs.bin_data("hhh")[1]
    database.color_sensor_blue_raw = cs.bin_data("hhh")[2]

    database.color_sensor_red_rgb = cs.bin_data("hhh")[0] / 185
    database.color_sensor_green_rgb = cs.bin_data("hhh")[1] / 321
    database.color_sensor_blue_rgb = cs.bin_data("hhh")[2] / 157

    database.ultra_sonic_sensor = us.distance_centimeters


# System loop for exploration
def system_loop():
    while True:
        # Add sensor data to database
        push_sensor_data()

        # Send ready message to mothership, only works once
        c.send_ready()

        c.send_exploration_completed()

        c.send_target_reached()

        """
        # Planet test code
        # -----
        # takes existing values from database and puts them in dicts, then adds them as new path as a whole
        start_dict = ((database.start_x, database.start_y), planet.Direction(database.start_dir))
        end_dict = ((database.end_x, database.end_y), planet.Direction(database.end_dir))
        this_path_weight = database.path_weight

        # Combine all data
        p.add_path(start_dict, end_dict, this_path_weight)
        """

        # Samplingrate for system loop ### 1/10 of a second
        time.sleep(1/10)


# DO NOT EDIT
if __name__ == '__main__':
    run()
