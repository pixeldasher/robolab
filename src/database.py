# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
# No imports

class Database:
    def __init__(self):
        """
        Initializes database module
        """

        # After the ready message's been sent, planet name is received
        self.planet_name = None


        # Temporarily saves the received message for further processing
        self.received_message = None


        # One time check at first station, should return as False afterwards
        self.first_time_ready = True


        # Type of the latest received message
        self.message_type = None


        # Boolean for whether or not the last message received an answer
        self.answered = False


        # Saves a specific point in time, then compares it with the current time
        self.time_offset = None


        # Variables for data extracted from mothership messages 
        self.start_x = None
        self.start_y = None
        self.start_dir = None

        self.end_x = None
        self.end_y = None
        self.end_dir = None

        self.path_status = None
        self.path_weight = None

        self.target = None

        self.done_message = None
        self.testplanet_message = None

        # Variables for exploration on planet
        self.next_direction = None
        self.vert = (self.end_x, self.end_y)
        self.directions = None


        # Latest path, put together with the data above
        self.latest_path_start = ((self.start_x, self.start_y), self.start_dir)
        self.latest_path_end = ((self.end_x, self.end_y), self.end_dir)
        self.latest_path_weight = self.path_weight


        # Booleans for whether or not the exploration is completed
        self.exploration_completed = False


    def update_start_coords(self):
        self.start_x = self.end_x
        self.start_y = self.end_y
        self.start_dir = (180 + self.end_dir) % 360
