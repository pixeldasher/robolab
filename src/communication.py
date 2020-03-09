#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
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

        # Changes current channel (topic) to explorer/025
        database.current_channel = "explorer/025"

        # Setup for client/server communication
        self.client.username_pw_set('025', password='4NpQpEEVS7')  # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('{}'.format(database.current_channel), qos=1)  # Subscribe to topic explorer/025

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
        if payload["from"] == "server":
            database.message_type = payload["type"]
            database.received_message = json.loads(message.payload.decode('utf-8'))
            self.message_type_scan()
        

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


    # Define all unique receivable message types for easier usage
    def message_type_scan(self):
        print(database.message_type)
        if database.message_type == "planet":
            database.planet_name = database.received_message["payload"]["planetName"]
            database.current_channel = "planet/{}/025".format(database.planet_name)
            database.first_time_ready = not database.first_time_ready


    # Define all unique sendable message types as functions for easier usage
    def send_planetName_message(self, planetName):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "testplanet", "payload": {"planetName": database.planet_name}})


    def send_ready_message(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "ready"})


    def send_path_message(self, message):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "path", "payload": "{}"})


    def send_pathSelect_message(self, message):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "pathSelect", "payload":{message}})


    def send_targetReached_message(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "explorationCompleted", "payload":{"message": "Target reached!"}})


    def send_explorationCompleted_message(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "done", "payload":{"message": "Exploration completed!"}})

    
    def comm_phase_init(self):
        if database.first_time_ready:
            # Send ready message to mothership
            self.send_ready_message()
        else:
            self.comm_phase_send()
        

    def comm_phase_send(self):
        print("Hello")


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
