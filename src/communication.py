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
            database.message_type = str(payload["type"])
            database.received_message = dict(json.loads(message.payload.decode('utf-8')))
            self.message_type_scan()
        """
        if payload["from"] == "server":
            database.message_type = str(payload["type"])
            database.received_message = dict(json.loads(message.payload.decode('utf-8')))
            print(json.dumps(payload, indent=2))
        """

        

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
            database.planet_name = str(database.received_message["payload"]["planetName"])
            database.current_channel = str("planet/{}/025".format(database.planet_name))
            database.first_time_ready = not database.first_time_ready

            database.start_x = int(database.received_message["payload"]["startX"])
            database.start_y = int(database.received_message["payload"]["startY"])
            database.start_dir = int(database.received_message["payload"]["startOrientation"])
        
        elif database.message_type == "path":
            database.start_x = int(database.received_message["payload"]["startX"])
            database.start_y = int(database.received_message["payload"]["startY"])
            database.start_dir = int(database.received_message["payload"]["startDirection"])

            database.end_x = int(database.received_message["payload"]["endX"])
            database.end_y = int(database.received_message["payload"]["endY"])
            database.end_dir = int(database.received_message["payload"]["endDirection"])

            database.path_status = str(database.received_message["payload"]["pathStatus"])
            database.path_weight = str(database.received_message["payload"]["pathWeight"])
        
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
            database.target_x = int(database.received_message["payload"]["targetX"])
            database.target_y = int(database.received_message["payload"]["targetY"])
        
        elif database.message_type == "done":
            database.done_message = str(database.received_message["payload"]["message"])
            

    # Define all unique sendable message types as functions for easier usage
    def send_test_planet(self, planet_name):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "testplanet", "payload": {"planetName": database.planet_name}})


    def send_ready(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "ready"})


    def send_path(self, startX, startY, startDirection, endX, endY, pathStatus):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "path", "payload": "{}"})


    def send_path_select(self, message):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "pathSelect", "payload":{message}})


    def send_target_reached(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "explorationCompleted", "payload":{"message": "Target reached!"}})


    def send_exploration_completed(self):
        self.send_message("{}".format(database.current_channel), {"from": "client", "type": "done", "payload":{"message": "Exploration completed!"}})

    
    def comm_phase_init(self):
        if database.first_time_ready:
            # Only performs the ready message action once
            self.send_ready()
            database.first_time_ready = not database.first_time_ready

        else:
            #Continue to sending phase
            self.comm_phase_send()
        

    def comm_phase_send(self):
        print("Hello")

        # Continue to receiving phase
        self.comm_phase_receive()


    def comm_phase_receive(self):
        pass


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
