### Variable database ###

# After the ready message's been sent, planet name is received
planet_name = None

# Temporarily saves the received message for further processing
received_message = None

# Defines the channel the brick is subscribed to and sending to
current_channel = None

# One time check at first station, should return as False afterwards
first_time_ready = True

# Type of the latest received message
message_type = None

# Variables for data extracted from mothership messages 
start_x = None
start_y = None
start_dir = None
end_x = None
end_y = None
end_dir = None
path_status = None
path_weight = None
target_x = None
target_y = None
done_message = None