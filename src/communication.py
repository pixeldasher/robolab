#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from time import time
from planet import Direction


# Class for communication
class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    def __init__(self, mqtt_client, logger, planet, odometry):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        # DO NOT CHANGE THE SETUP HERE
        self.client = mqtt_client
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler

        # Setup for client/server communication; Uses given username, password and channel data
        self.client.username_pw_set('025', password='4NpQpEEVS7')
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe("explorer/025", qos=1)

        # Starts the listener
        self.client.loop_start()

        # logger var from function input
        self.logger = logger

        # Create module objects
        self.planet = planet
        self.odometry = odometry

        # Create variables for functions
        self.planet_name = None
        self.payload = None
        self.answered = False
        self.time_offset = None

    # DO NOT EDIT THE METHOD SIGNATURE

    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        self.payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(self.payload, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        if self.payload["from"] == "server" or self.payload["from"] == "debug":
            # Function for differentiating all possible messages
            self.message_type_scan()

            # Prints the message
            #print(json.dumps(self.payload, indent=2))

            # Checks whether or not an answer has been received
            if self.payload["from"] == "server":
                self.answered = True

            # Writes down the time since the last message has been sent/received
            self.time_offset = int(time())

        print(json.dumps(self.payload, indent=2))

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.

    def send_message(self, topic, message):
        """
        Sends given message to specified channel
        :param topic: String
        :param message: Object
        :return: void
        """
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        self.client.publish(topic, json.dumps(message))

        # Write down time value in order to compare it later
        self.time_offset = int(time())

        while True:
            # If last message has received an answer, continue...
            if self.answered:
                self.answered = False
                break

            # If last message has been sent/received longer than three seconds ago, continue...
            elif int(time()) - self.time_offset >= 3:
                break

            # Wait until either one of the conditions is met
            else:
                pass

#####################################################################################

    # Define all unique receivable message types for easier usage;
    def message_type_scan(self):
        if self.payload["type"] == "planet":
            # Get planet name from ready message and save it to variable for further usage
            self.planet_name = self.payload["payload"]["planetName"]

            # changes start coords and direction
            self.odometry.dest_x = self.payload["payload"]["startX"]
            self.odometry.dest_y = self.payload["payload"]["startY"]
            self.odometry.dest_d = (
                self.payload["payload"]["startOrientation"] - 180) % 360

            # Subscribe to the planets channel in order to receive the messages sent on it
            self.client.subscribe(
                "planet/{}/025".format(self.planet_name), qos=1)

        # If received message is of type "path", update all saved coords with the received counterparts
        elif self.payload["type"] == "path":
            # changes start coords and direction
            self.odometry.curr_x = self.payload["payload"]["startX"]
            self.odometry.curr_y = self.payload["payload"]["startY"]
            self.odometry.curr_d = self.payload["payload"]["startDirection"]

            # changes end coords and direction
            self.odometry.dest_x = self.payload["payload"]["endX"]
            self.odometry.dest_y = self.payload["payload"]["endY"]
            self.odometry.dest_d = self.payload["payload"]["endDirection"]

            self.odometry.path_status = self.payload["payload"]["pathStatus"]
            self.odometry.path_weight = self.payload["payload"]["pathWeight"]

        # If message is of type path select, use the given direction as the next direction to move to
        elif self.payload["type"] == "pathSelect":
            self.odometry.next_d = self.payload["payload"]["startDirection"]

        # If message is of type path unveiled, add the now given path to the planet's database
        elif self.payload["type"] == "pathUnveiled":
            # take the given data and use them in add path function
            print("pathUnveiled/n/n/n/n/n/n/n/n/n/n/n/n/n")
            self.planet.add_path(
                ((self.payload["payload"]["startX"], self.payload["payload"]["startY"]),
                    self.payload["payload"]["startDirection"]),
                ((self.payload["payload"]["endX"], self.payload["payload"]["endY"]),
                    self.payload["payload"]["endDirection"]),
                    self.payload["payload"]["pathWeight"])

            """
            self.planet.vertex_explored(
                ((self.payload["payload"]["startX"], self.payload["payload"]["startY"]), 
                    self.payload["payload"]["startDirection"]), 
                ((self.payload["payload"]["endX"], self.payload["payload"]["endY"]), 
                    self.payload["payload"]["endDirection"]))
            """

        # If message is of type target, save the given target as a tuple in the planet's database
        elif self.payload["type"] == "target":
            # create tuple with x and y coordinate
            self.planet.target = (
                self.payload["payload"]["targetX"], self.payload["payload"]["targetY"])

        # If message is of type done, end all exploration
        elif self.payload["type"] == "done":
            print("Done")

        # This message is a debug message; only available outside of the exam
        elif self.payload["type"] == "notice":
            print(self.payload["payload"]["message"])

#####################################################################################

    # Send a message to mothership that the brick is ready for exploration
    def send_ready(self):
        self.send_message("explorer/025", {"from": "client", "type": "ready"})

    # Send test planet message; determines the current planet that should be used for testing.
    def send_test_planet(self):
        self.send_message(
            "explorer/025", {"from": "client", "type": "testplanet", "payload": {"planetName": "Examinator-X-42b"}})

    # Send the last followed path line to server; Start = prev. point, End = curr. point
    def send_path(self):
        self.send_message("planet/{}/025".format(self.planet_name), {"from": "client", "type": "path", "payload": {"startX": self.odometry.curr_x, "startY": self.odometry.curr_y,
                                                                                                                   "startDirection": self.odometry.curr_d, "endX": self.odometry.dest_x, "endY": self.odometry.dest_y, "endDirection": self.odometry.dest_d, "pathStatus": self.odometry.path_status}})

    # Send the algorithm's selected path to mothership; Could be overwritten by server selection.
    def send_path_select(self):
        direction = int(self.planet.select_direction(
            (self.odometry.curr_x, self.odometry.curr_y), self.planet.target))
        self.send_message("planet/{}/025".format(self.planet_name), {"from": "client", "type": "pathSelect",
                                                                     "payload": {"startX": self.odometry.curr_x, "startY": self.odometry.curr_y, "startDirection": direction}})
        self.odometry.next_d = direction

        if self.planet.target is not None:
            if self.odometry.curr_x == self.planet.target[0] and self.odometry.curr_y == self.planet.target[1]:
                self.send_target_reached()

    # Send message to mothership that the given target has been reached; should be initiated by planet module
    def send_target_reached(self):
        self.send_message(
            "explorer/025", {"from": "client", "type": "targetReached", "payload": {"message": "Target reached!"}})

    # Send message to mothership that the exploration has been completed; Target still has to be reached though.
    def send_exploration_completed(self):
        self.send_message("explorer/025", {"from": "client", "type": "explorationCompleted",
                                           "payload": {"message": "Exploration completed!"}})

#####################################################################################

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"
    def safe_on_message_handler(self, client, data, message):
        """
        Handle exceptions thrown by the paho library
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise
