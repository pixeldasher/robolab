#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from time import time
from database import Database


# Class for communication
class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    def __init__(self, mqtt_client, logger):
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

        # Setup database
        global d
        d = Database()


    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(payload, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        # Add the message's content to the database
        d.message_type = str(payload["type"])
        d.received_message = dict(json.loads(message.payload.decode('utf-8')))

        # Function for differentiating all possible messages
        self.message_type_scan()

        # Prints the message
        print(json.dumps(json.loads(message.payload.decode('utf-8')), indent=2))

        # Checks whether or not an answer has been received
        if d.received_message["from"] == "server" or "debug":
            d.answered = True
        
        # Writes down the time since the last message has been sent/received
        d.time_offset = int(time())
      

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
        d.time_offset = int(time())

        while True:
            # If last message has received an answer, continue...
            if d.answered:
                d.answered = False
                break
            
            # If last message has been sent/received longer than three seconds ago, continue...
            elif int(time()) - d.time_offset >= 3:
                break
            
            # Wait until either one of the conditions is met
            else:
                pass
            


    # Define all unique receivable message types for easier usage; Takes all data from message and adds them to database
    def message_type_scan(self):
        if d.message_type == "planet":
            d.planet_name = str(d.received_message["payload"]["planetName"])

            d.start_x = int(d.received_message["payload"]["startX"])
            d.start_y = int(d.received_message["payload"]["startY"])
            d.start_dir = int(d.received_message["payload"]["startOrientation"])

            """
            # Possible Override for testing
            d.planet_name = "examinator-p-33r"
            d.start_x = 1
            d.start_y = 1
            d.start_dir = 0
            #"""

            self.client.subscribe(f"planet/{d.planet_name}/025", qos=1)

        
        elif d.message_type == "path":
            d.start_x = int(d.received_message["payload"]["startX"])
            d.start_y = int(d.received_message["payload"]["startY"])
            d.start_dir = int(d.received_message["payload"]["startDirection"])

            d.end_x = int(d.received_message["payload"]["endX"])
            d.end_y = int(d.received_message["payload"]["endY"])
            d.end_dir = int(d.received_message["payload"]["endDirection"])

            d.path_status = str(d.received_message["payload"]["pathStatus"])
            d.path_weight = int(d.received_message["payload"]["pathWeight"])
        
        elif d.message_type == "pathSelect":
            d.start_dir = int(d.received_message["payload"]["startDirection"])
        
        elif d.message_type == "pathUnveiled":
            d.start_x = int(d.received_message["payload"]["startX"])
            d.start_y = int(d.received_message["payload"]["startY"])
            d.start_dir = int(d.received_message["payload"]["startDirection"])

            d.end_x = int(d.received_message["payload"]["endX"])
            d.end_y = int(d.received_message["payload"]["endY"])
            d.end_dir = int(d.received_message["payload"]["endDirection"])

            d.path_status = str(d.received_message["payload"]["pathStatus"])
            d.path_weight = int(d.received_message["payload"]["pathWeight"])
        
        elif d.message_type == "target":
            d.target = (int(d.received_message["payload"]["targetX"]), int(d.received_message["payload"]["targetY"]))
        
        elif d.message_type == "done":
            d.done_message = str(d.received_message["payload"]["message"])

        elif d.message_type == "notice":
            d.testplanet_message = str(d.received_message["payload"]["message"])

            

    # Define all unique sendable message types as functions for easier usage; Takes all data from database and adds them to message
    def send_ready(self):
        if d.first_time_ready:
            # Only performs the ready message action once
            self.send_message("explorer/025", {"from": "client", "type": "ready"})
            d.first_time_ready = not d.first_time_ready
        else:
            pass


    def send_test_planet(self):
        self.send_message("explorer/025", {"from": "client", "type": "testplanet", "payload": {"planetName": d.planet_name}})


    def send_path(self):
        # If no data has been set, don't call it from database
        if type(d.start_x) == int:
            self.send_message(f"planet/{d.planet_name}/025", {"from": "client", "type": "path", "payload": {"startX": d.start_x, "startY": d.start_y, "startDirection": d.start_dir, "endX": d.end_x, "endY": d.end_y, "endDirection": d.end_dir, "pathStatus": d.path_status}})
        else:
            pass


    def send_path_select(self):
        # If no data has been set, don't call it from database
        if type(d.next_direction) == int:
            self.send_message(f"planet/{d.planet_name}/025", {"from": "client", "type": "pathSelect", "payload":{"startX": d.start_x, "startY": d.start_y, "startDirection": d.next_direction}})
        else:
            pass


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
