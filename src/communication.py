#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from time import time
import database





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
        if json.loads(message.payload.decode('utf-8'))["from"] == "server" or json.loads(message.payload.decode('utf-8'))["from"] == "debug":
            database.message_type = payload["type"]
            database.received_message = dict(json.loads(message.payload.decode("utf-8")))

            #print(database.received_message["from"])

            # Function for differentiating all possible messages
            self.message_type_scan()

            # Prints the message
            print(json.dumps(json.loads(message.payload.decode('utf-8')), indent=2))

            # Checks whether or not an answer has been received
            if database.received_message["from"] == "server" or database.received_message["from"] == "debug":
                database.answered = True
        
            # Writes down the time since the last message has been sent/received
            database.time_offset = int(time())
      

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
        database.time_offset = int(time())

        while True:
            # If last message has received an answer, continue...
            if database.answered:
                database.answered = False
                break
            
            # If last message has been sent/received longer than three seconds ago, continue...
            elif int(time()) - database.time_offset >= 3:
                break
            
            # Wait until either one of the conditions is met
            else:
                pass
            


    # Define all unique receivable message types for easier usage; Takes all data from message and adds them to database
    def message_type_scan(self):
        if database.message_type == "planet":
            database.planet_name = str(database.received_message["payload"]["planetName"])

            database.start_x = int(database.received_message["payload"]["startX"])
            database.start_y = int(database.received_message["payload"]["startY"])
            database.start_dir = int(database.received_message["payload"]["startOrientation"])

            self.client.subscribe("planet/{}/025".format(database.planet_name), qos=1)

        
        elif database.message_type == "path":
            database.start_x = int(database.received_message["payload"]["startX"])
            database.start_y = int(database.received_message["payload"]["startY"])
            database.start_dir = int(database.received_message["payload"]["startDirection"])

            database.end_x = int(database.received_message["payload"]["endX"])
            database.end_y = int(database.received_message["payload"]["endY"])
            database.end_dir = int(database.received_message["payload"]["endDirection"])

            database.path_status = str(database.received_message["payload"]["pathStatus"])
            database.path_weight = database.received_message["payload"]["pathWeight"]
        
        elif database.message_type == "pathSelect":
            database.start_dir = int(database.received_message["payload"]["startDirection"])
        
        elif database.message_type == "pathUnveiled":
            database.start_x = int(database.received_message["payload"]["startX"])
            database.start_y = int(database.received_message["payload"]["startY"])
            database.start_dir = int(database.received_message["payload"]["startDirection"])

            database.end_x = int(database.received_message["payload"]["endX"])
            database.end_y = int(database.received_message["payload"]["endY"])
            database.end_dir = int(database.received_message["payload"]["endDirection"])

            database.path_status = str(database.received_message["payload"]["pathStatus"])
            database.path_weight = int(database.received_message["payload"]["pathWeight"])
        
        elif database.message_type == "target":
            database.target = (int(database.received_message["payload"]["targetX"]), int(database.received_message["payload"]["targetY"]))
        
        elif database.message_type == "done":
            database.done_message = str(database.received_message["payload"]["message"])

        elif database.message_type == "notice":
            database.testplanet_message = str(database.received_message["payload"]["message"])

            

    # Define all unique sendable message types as functions for easier usage; Takes all data from database and adds them to message
    def send_ready(self):
        if database.first_time_ready:
            # Only performs the ready message action once
            self.send_message("explorer/025", {"from": "client", "type": "ready"})
        else:
            pass


    def send_test_planet(self):
        self.send_message("explorer/025", {"from": "client", "type": "testplanet", "payload": {"planetName": database.planet_name}})


    def send_path(self):
        # If no data has been set, don't call it from database
        if not database.first_time_ready:
            self.send_message("planet/{}/025".format(database.planet_name), {"from": "client", "type": "path", "payload": {"startX": database.start_x, "startY": database.start_y, "startDirection": database.start_dir, "endX": database.end_x, "endY": database.end_y, "endDirection": database.end_dir, "pathStatus": database.path_status}})
        else:
            database.first_time_ready = not database.first_time_ready
            pass


    def send_path_select(self):
        # If no data has been set, don't call it from database
        if type(database.next_direction) == int:
            self.send_message("planet/{}/025".format(database.planet_name), {"from": "client", "type": "pathSelect", "payload":{"startX": database.start_x, "startY": database.start_y, "startDirection": database.next_direction}})
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
