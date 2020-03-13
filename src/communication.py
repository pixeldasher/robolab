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

        # Create variables
        self.payload = None
        self.answered = False
        self.time_offset = None
        self.first_time_ready = True


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

            # Checks whether or not an answer has been received
            if self.payload["from"] == "server" or self.payload["from"] == "debug":
                self.answered = True
        
            # Writes down the time since the last message has been sent/received
            self.time_offset = int(time())

        # Prints the message
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
            


    # Define all unique receivable message types for easier usage;
    def message_type_scan(self):
        if self.payload["type"] == "planet":
            self.planet_name = self.payload["payload"]["planetName"]

            self.odometry.start_x = self.payload["payload"]["startX"]
            self.odometry.start_y = self.payload["payload"]["startY"]
            self.odometry.start_dir = self.payload["payload"]["startOrientation"]

            self.client.subscribe("planet/{}/025".format(self.planet_name), qos=1)

        
        elif self.payload["type"] == "path" and self.payload["payload"]["pathStatus"] == "free":
            self.odometry.start_x = self.payload["payload"]["startX"]
            self.odometry.start_y = self.payload["payload"]["startY"]
            self.odometry.start_dir = self.payload["payload"]["startDirection"]

            self.odometry.end_x = self.payload["payload"]["endX"]
            self.odometry.end_y = self.payload["payload"]["endY"]
            self.odometry.end_dir = self.payload["payload"]["endDirection"]

            self.planet.add_vertex((self.payload["payload"]["endX"], self.payload["payload"]["endY"]), self.odometry.directions)
            self.planet.add_path((self.odometry.start_x, self.odometry.start_y), (self.odometry.end_x, self.odometry.end_y), self.payload["payload"]["pathWeight"])

        elif self.payload["type"] == "path" and self.payload["payload"]["pathStatus"] == "blocked":
            self.odometry.start_x = self.payload["payload"]["startX"]
            self.odometry.start_y = self.payload["payload"]["startY"]
            self.odometry.start_dir = self.payload["payload"]["startDirection"]

            self.odometry.end_x = self.payload["payload"]["endX"]
            self.odometry.end_y = self.payload["payload"]["endY"]
            self.odometry.end_dir = self.payload["payload"]["endDirection"]

            self.planet.vertex_explored(((self.payload["payload"]["startX"], self.payload["payload"]["startY"]), self.payload["payload"]["startDirection"]), (self.planet.target, self.payload["payload"]["endDirection"]))
            self.planet.add_vertex((self.payload["payload"]["endX"], self.payload["payload"]["endY"]), self.odometry.directions)
            self.planet.add_path((self.odometry.start_x, self.odometry.start_y), (self.odometry.end_x, self.odometry.end_y), -1)
            self.planet.vertex_explored(((self.payload["payload"]["startX"], self.payload["payload"]["startY"]), self.payload["payload"]["startDirection"]), (self.planet.target, self.payload["payload"]["endDirection"]))
            self.odometry.path_status="free"
        
        elif self.payload["type"] == "pathSelect":
            self.odometry.turn_around((self.odometry.start_dir + 180 + self.payload["payload"]["startDirection"]) % 360)
        
        elif self.payload["type"] == "pathUnveiled":
            self.odometry.start_x = self.payload["payload"]["startX"]
            self.odometry.start_y = self.payload["payload"]["startY"]
            self.odometry.start_dir = self.payload["payload"]["startDirection"]

            self.odometry.end_x = self.payload["payload"]["endX"]
            self.odometry.end_y = self.payload["payload"]["endY"]
            self.odometry.end_dir = self.payload["payload"]["endDirection"]

            self.planet.add_vertex((self.payload["payload"]["endX"], self.payload["payload"]["endY"]), self.odometry.directions)
            self.planet.add_path((self.odometry.start_x, self.odometry.start_y), (self.odometry.end_x, self.odometry.end_y), self.payload["payload"]["pathWeight"])
        
        elif self.payload["type"] == "target":
            self.planet.target = (self.payload["payload"]["targetX"], self.payload["payload"]["targetY"])
        
        elif self.payload["type"] == "done":
            print("Done")

        elif self.payload["type"] == "notice":
            print(self.payload["payload"]["message"])


    # Define all unique sendable message types as functions for easier usage;
    def send_ready(self):
        if self.first_time_ready:
            # Only performs the ready message action once
            self.send_message("explorer/025", {"from": "client", "type": "ready"})
        else:
            pass


    def send_test_planet(self):
        # If no data has been set, don't call function
        if not self.first_time_ready:
            self.send_message("explorer/025", {"from": "client", "type": "testplanet", "payload": {"planetName": "Examinator-A-1337r"}})
        else:
            pass


    def send_path(self):
        # If no data has been set, don't call function
        if not self.first_time_ready:
            self.send_message("planet/{}/025".format(self.planet_name), {"from": "client", "type": "path", "payload": {"startX": self.odometry.start_x, "startY": self.odometry.start_y, "startDirection": self.odometry.start_dir, "endX": self.odometry.end_x, "endY": self.odometry.end_y, "endDirection": self.odometry.end_dir, "pathStatus": self.odometry.path_status}})
        else:
            self.first_time_ready = not self.first_time_ready
            pass


    def send_path_select(self):
        self.send_message("planet/{}/025".format(self.planet_name), {"from": "client", "type": "pathSelect", "payload":{"startX": self.odometry.start_x, "startY": self.odometry.start_y, "startDirection": self.planet.select_direction((self.odometry.start_x, self.odometry.start_y), self.planet.target)}})
        


    def send_target_reached(self):
        self.send_message("explorer/025", {"from": "client", "type": "targetReached", "payload":{"message": "Target reached!"}})


    def send_exploration_completed(self):
        self.send_message("explorer/025", {"from": "client", "type": "explorationCompleted", "payload":{"message": "Exploration completed!"}})


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
