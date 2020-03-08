# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import main
import time


class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
    
    
path_dict = {}

def touch_check(n):
    if (n == 1):
        path_dict.update({"latest_path" : "blocked t"})
        print(path_dict)
        stop_moving()
        return False
    else:
        return True


def distance_check(d):
    if (d < 25):
        path_dict.update({"latest_path" : "blocked d"})
        print(path_dict)
        turn_around()
        return False
    else:
        return True


def movement_check(boolean):
    if boolean:
        follow_line()
    else:
        stop_moving()


# Define movement functions
def move_straight():
    main.motor_left.speed_sp = 250
    main.motor_right.speed_sp = 250
    main.motor_left.command = "run-forever"
    main.motor_right.command = "run-forever"

    
def move_left():
    main.motor_left.speed_sp = 25
    main.motor_right.speed_sp = 250
    main.motor_left.command = "run-forever"
    main.motor_right.command = "run-forever"

    
def move_right():
    main.motor_left.speed_sp = 250
    main.motor_right.speed_sp = 25
    main.motor_left.command = "run-forever"
    main.motor_right.command = "run-forever"

    
def stop_moving():
    main.motor_left.speed_sp = 0
    main.motor_right.speed_sp = 0
    main.motor_left.command = "run-forever"
    main.motor_right.command = "run-forever"


def luminance():
    current_value_red = (main.cs.bin_data("hhh")[0] / 185)
    current_value_green = (main.cs.bin_data("hhh")[1] / 321)
    current_value_blue = (main.cs.bin_data("hhh")[2] / 157)
    value = (0.2126 * current_value_red + 0.7152 * current_value_green + 0.0722 * current_value_blue)

    return value


def turn_around():
    main.motor_left.speed_sp = 400
    main.motor_right.speed_sp = -400
    main.motor_left.command = "run-forever"
    main.motor_right.command = "run-forever"
    time.sleep(0.25)
    while (float(luminance()) > 0.4):
        main.motor_left.speed_sp = 400
        main.motor_right.speed_sp = -400
        main.motor_left.command = "run-forever"
        main.motor_right.command = "run-forever"
    follow_line()


def follow_line():
    if (float(luminance()) < 0.4):
        move_left()

    if (0.4 >= float(luminance()) >= 0.7):
        move_straight()

    if (float(luminance()) > 0.7):
        move_right()


def check_phase():
    movement_check(touch_check(main.ts.value()) & distance_check(main.us.distance_centimeters))