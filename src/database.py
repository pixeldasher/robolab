###############################
### Communication variables ###
###############################

# After the ready message's been sent, planet name is received
planet_name = None

# Temporarily saves the received message for further processing
received_message = None

# One time check at first station, should return as False afterwards
first_time_ready = True

# Type of the latest received message
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
target_x = None
target_y = None
done_message = None
testplanet_message = None
#######
targed_reached = False
target_unreachable = False

"""
###
"""

### Odometry variables ###

# Color sensor values
color_sensor_red_raw = None
color_sensor_green_raw = None
color_sensor_blue_raw = None

color_sensor_red_rgb = None
color_sensor_green_rgb = None
color_sensor_blue_rgb = None

# Ultra sonic sensor value
ultra_sonic_sensor = None

# Current speed value
motor_left_speed = None
motor_right_speed = None

# Motor commands
motor_command = None
