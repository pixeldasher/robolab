# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import main
from time import sleep
from math import sin,cos,pi


class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
    
    
path_dict = {}


def luminance():
    current_value_red = (main.cs.bin_data("hhh")[0]/185)
    current_value_green = (main.cs.bin_data("hhh")[1]/321)
    current_value_blue = (main.cs.bin_data("hhh")[2]/157)

    value = (0.2126 * current_value_red + 0.7152 * current_value_green + 0.0722 * current_value_blue)

    return value


"""
def colorscan():

    max_value_red = 0
    min_value_red = 1020

    max_value_green = 0
    min_value_green = 1020

    max_value_blue = 0
    min_value_blue = 1020

    n = 2000
    i = 1

    while i <= n:
        i += 1
        current_value_red = (main.cs.bin_data("hhh")[0])
        current_value_green = (main.cs.bin_data("hhh")[1])
        current_value_blue = (main.cs.bin_data("hhh")[2])

        if current_value_red > max_value_red:
            max_value_red = current_value_red

        if current_value_red < min_value_red:
            min_value_red = current_value_red

        if current_value_green > max_value_green:
            max_value_green = current_value_green

        if current_value_green < min_value_green:
            min_value_green = current_value_green

        if current_value_blue > max_value_blue:
            max_value_blue = current_value_blue

        if current_value_blue < min_value_blue:
            min_value_blue = current_value_blue

    print(max_value_red, max_value_green, max_value_blue)
    print(min_value_red, min_value_green, min_value_blue)

"""
Kp = 20
Ki = 1
Kd = 100
offset = 45
Tp = 90


def move_smooth():

    integral = 0
    lasterror = 0

    lightvalue = luminance() * 100
    error = lightvalue - offset
    integral = integral + error
    derivative = error - lasterror
    turn = Kp * error + Ki * integral + Kd * derivative
    turn = turn / 40
    power_motor_left = (Tp + turn)
    power_motor_right = (Tp - turn)
    lasterror = error

    main.motor_left.speed_sp = power_motor_left
    main.motor_right.speed_sp = power_motor_right

    current_value_red = (main.cs.bin_data("hhh")[0])
    current_value_green = (main.cs.bin_data("hhh")[1])
    current_value_blue = (main.cs.bin_data("hhh")[2])

    """
    print("red:", current_value_red)
    print("green:", current_value_green)
    print("blue:", current_value_blue)
    """

    if 65 < current_value_red < 100 and 20 < current_value_green < 40 and 5 < current_value_blue < 35:
        main.motor_left.command = "stop"
        main.motor_right.command = "stop"
        sleep(3)
        return True

    elif 15 < current_value_red < 35 and 80 < current_value_green < 105 and 55 < current_value_blue < 79:
        main.motor_left.command = "stop"
        main.motor_right.command = "stop"
        sleep(3)
        return True
    else:
        main.motor_left.command = "run-forever"
        main.motor_right.command = "run-forever"
        return False


def start_driving():
    global wheel_left, wheel_right
    wheel_left = []
    wheel_right = []
    main.motor_right.reset()
    main.motor_left.reset()


def while_driving():
    motor_left_value = (main.motor_left.position / 360)
    motor_right_value = (main.motor_right.position / 360)
    wheel_left.append(motor_left_value)
    wheel_right.append(motor_right_value)
    sleep(0.1)


def stop_driving():
    x = 0
    y = 0
    gamma = 0
    a = 13.2

    for i in range(1, len(wheel_left)):
        distance_left = (wheel_left[i] - wheel_left[i-1]) * 5.6 * pi
        distance_right = (wheel_right[i] - wheel_right[i-1]) * 5.6 * pi

        alpha = (distance_right - distance_left) / a
        beta = alpha / 2
        if alpha == 0:
            s = distance_left
        else:
            s = ((distance_right + distance_left ) / alpha) * sin(beta)
        deltax = - sin(gamma + beta) * s
        deltay = cos(gamma + beta) * s
        gamma = gamma + alpha
        x = deltax + x
        y = deltay + y

    return x, y, gamma

