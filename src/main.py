#!/usr/bin/env python3

# Import py modules
import logging
import uuid
import os
import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3
from time import sleep

# Import src modules
import odometry
from communication import Communication
from planet import Direction, Planet
from database import Database

client = None  # DO NOT EDIT

# Define sensors
us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()

# Define sensor modes
us.mode = 'US-DIST-CM'
cs.mode = 'RGB-RAW'

# Define motors
motor_left = ev3.LargeMotor("outA")
motor_right = ev3.LargeMotor("outB")


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
    global p, c, d
    p = Planet()
    c = Communication(client, logger)
    d = Database()

    # Run system loop for exploration
    system_loop()


# Push all the sensor data into the database
def push_sensor_data():
    d.color_sensor_red_raw = cs.bin_data("hhh")[0]
    d.color_sensor_green_raw = cs.bin_data("hhh")[1]
    d.color_sensor_blue_raw = cs.bin_data("hhh")[2]

    d.color_sensor_red_rgb = cs.bin_data("hhh")[0] / 185
    d.color_sensor_green_rgb = cs.bin_data("hhh")[1] / 321
    d.color_sensor_blue_rgb = cs.bin_data("hhh")[2] / 157

    d.ultra_sonic_sensor = us.distance_centimeters


# System loop for running through all phases
def system_loop():
    odometry.start_driving()
    while True:
        # Add all sensor data to database
        push_sensor_data()

        # Movement function
        odometry.while_driving()

        # If stations has been reached:
        if odometry.move_smooth():
            # ... send ready message, only works at the first station
            c.send_ready()

            # ... move forward in order to not scan the same station twice
            motor_left.run_to_rel_pos(position_sp=180)
            motor_right.run_to_rel_pos(position_sp=180)
            sleep(2.5)

            # ... get data from odometry and save it to database
            odometry.stop_driving()

            # ... send collected data to mothership
            c.send_path()
            
            # ... add the corrected path to planet data
            # p.add_path(d.latest_path)

            # ... replace old start coordinates and direction with current end coordinates and direction
            d.update_start_coords()

            # ... turn around to search for possible paths
            # odometry.search_paths()

            # ... send selected path choice to mothership
            c.send_path_select

            # ... make a sound
            ev3.Sound.play_song((('D4', 'e3'),( 'D4', 'e3'), ('D4', 'e3'), ('G4', 'h')))

            # ... continue driving
            odometry.start_driving()


        # Samplingrate for system loop ### 1/10 of a seconds
        sleep(1/10)


# DO NOT EDIT
if __name__ == '__main__':
    run()
