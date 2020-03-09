### Communication variables ###

# After the ready message's been sent, planet name is received
global planet_name
planet_name = None

# Temporarily saves the received message for further processing
global received_message
received_message = None

# Defines the channel the brick is subscribed to and sending to
global current_channel
current_channel = None

# One time check at first station, should return as False afterwards
global first_time_ready
first_time_ready = True

# Type of the latest received message
global message_type
message_type = None