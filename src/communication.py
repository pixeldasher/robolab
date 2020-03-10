#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from time import time
import database


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
        # Add your client setup here
        #
        # Setup for client/server communication
        self.client.username_pw_set('025', password='4NpQpEEVS7')  # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe("explorer/025", qos=1)  # Subscribe to topic explorer/025
        self.client.loop_start()

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

        print("\n-----\n")
        database.message_type = str(payload["type"])
        database.received_message = dict(json.loads(message.payload.decode('utf-8')))
        self.message_type_scan()

        print(json.dumps(json.loads(message.payload.decode('utf-8')), indent=2))

        if (database.received_message["from"] == "server") or (database.received_message["from"] == "debug"):
            database.answered = True
      

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

        database.time_offset = int(time())
        while True:
            if database.answered:
                database.answered = False
                break

            elif (int(time()) - database.time_offset) >= 3:
                # Stop communication after 3 seconds of no answer
                break

            else:
                pass
            


    # Define all unique receivable message types for easier usage
    def message_type_scan(self):
        if database.message_type == "planet":
            database.planet_name = database.received_message["payload"]["planetName"]

            database.start_x = database.received_message["payload"]["startX"]
            database.start_y = database.received_message["payload"]["startY"]
            database.start_dir = database.received_message["payload"]["startOrientation"]

            self.client.subscribe("planet/{}/025".format(database.planet_name), qos=1)  # Subscribe to topic planet

        
        elif database.message_type == "path":
            database.start_x = database.received_message["payload"]["startX"]
            database.start_y = database.received_message["payload"]["startY"]
            database.start_dir = database.received_message["payload"]["startDirection"]

            database.end_x = database.received_message["payload"]["endX"]
            database.end_y = database.received_message["payload"]["endY"]
            database.end_dir = database.received_message["payload"]["endDirection"]

            database.path_status = database.received_message["payload"]["pathStatus"]
            database.path_weight = database.received_message["payload"]["pathWeight"]
        
        elif database.message_type == "pathSelect":
            database.start_dir = database.received_message["payload"]["startDirection"]
        
        elif database.message_type == "pathUnveiled":
            database.start_x = database.received_message["payload"]["startX"]
            database.start_y = database.received_message["payload"]["startY"]
            database.start_dir = database.received_message["payload"]["startDirection"]

            database.end_x = database.received_message["payload"]["endX"]
            database.end_y = database.received_message["payload"]["endY"]
            database.end_dir = database.received_message["payload"]["endDirection"]

            database.path_status = database.received_message["payload"]["pathStatus"]
            database.path_weight = database.received_message["payload"]["pathWeight"]
        
        elif database.message_type == "target":
            database.target_x = database.received_message["payload"]["targetX"]
            database.target_y = database.received_message["payload"]["targetY"]
        
        elif database.message_type == "done":
            database.done_message = database.received_message["payload"]["message"]

        elif database.message_type == "notice":
            database.testplanet_message = database.received_message["payload"]["message"]

            

    # Define all unique sendable message types as functions for easier usage
    def send_ready(self):
        if database.first_time_ready:
            # Only performs the ready message action once
            self.send_message("explorer/025", {"from": "client", "type": "ready"})
            database.first_time_ready = not database.first_time_ready
        else:
            pass


    def send_test_planet(self, planet_name):
        self.send_message("explorer/025", {"from": "client", "type": "testplanet", "payload": {"planetName": planet_name}})


    def send_path(self, start_x, start_y, start_dir, end_x, end_y, end_dir, path_status):
        self.send_message("planet/{}/025".format(database.planet_name), {"from": "client", "type": "path", "payload": {"startX": start_x, "startY": start_y, "startDirection": start_dir, "endX": end_x, "endY": end_y, "endDirection": end_dir, "pathStatus": path_status}})


    def send_path_select(self, start_x, start_y, start_dir):
        self.send_message("planet/{}/025".format(database.planet_name), {"from": "client", "type": "pathSelect", "payload":{"startX": start_x, "startY": start_y, "startDirection": start_dir}})


    def send_target_reached(self):
        self.send_message("explorer/025", {"from": "client", "type": "targetReached", "payload":{"message": "Target reached!"}})


    def send_exploration_completed(self):
        self.send_message("explorer/025", {"from": "client", "type": "explorationCompleted", "payload":{"message": "Exploration completed!"}})


    def communication_phase(self):
        self.send_ready()
        
        self.send_test_planet(database.planet_name)

        self.send_exploration_completed()

        self.send_target_reached()

        self.send_path_select(1, 1, 0)


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
