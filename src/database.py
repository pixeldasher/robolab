# After the ready message's been sent, planet name is received
planet_name = None


# Temporarily saves the received message for further processing
received_message = None


# One time check at first station, should return as False afterwards
first_time_ready = True


# Type of the latest message
message_type = None


# Boolean for whether or not the last message received an answer
answered = False


# Saves a specific point in time, then compares it with the current time
time_offset = None


# Variables for data extracted from mothership messages 
start_x = None
start_y = None
start_dir = None

end_x = None
end_y = None
end_dir = None

path_status = None
path_weight = None

target = None

done_message = None
testplanet_message = None


# Variables for exploration on planet
next_direction = None
vert = (end_x, end_y)
directions = None


# Latest path, put together with the data above
latest_path_start = ((start_x, start_y), start_dir)
latest_path_end = ((end_x, end_y), end_dir)
latest_path_weight = path_weight


# Boolean for whether or not the exploration is completed
exploration_completed = False


def update_start_coords():
    global end_x
    global start_x
    global start_y
    global start_dir
    global end_dir

    if type(end_x) == int:
        start_x = end_x
        start_y = end_y
        start_dir = (180 + end_dir) % 360
    else:
        pass
