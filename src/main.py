#!/usr/bin/env python3


import logging
import os
import paho.mqtt.client as mqtt
import uuid
import ev3dev.ev3 as ev3

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

    comm = Communication(client, logger)

    while True:
        user_input = input("Send message...")
        if user_input == "ready":
            comm.send_ready_message()
            print("sent ready message")
        if user_input == "target":
            comm.send_targetReached_message()
            print("sent ready message")
        if user_input == "easy":
            comm.send_explorationCompleted_message()
        else:
            print("try again.")


# DO NOT EDIT
if __name__ == '__main__':
    run()
