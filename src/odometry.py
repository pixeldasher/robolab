# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import ev3dev.ev3 as ev3
from time import sleep
from math import sin,cos,pi, degrees
import planet


class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """
        # Define sensors
        self.us = ev3.UltrasonicSensor()
        self.cs = ev3.ColorSensor()

        # Define sensor modes
        self.us.mode = 'US-DIST-CM'
        self.cs.mode = 'RGB-RAW'

        # Define motors
        self.motor_left = ev3.LargeMotor("outA")
        self.motor_right = ev3.LargeMotor("outB")

        self.a = 9.3
        self.d = 5.6
        self.Kp = 10
        self.Ki = 1
        self.Kd = 100
        self.offset = 50
        self.Tp = 65
        self.wheel_left = None
        self.wheel_right = None

        self.directions = set()
        self.path_status = None
        
    def luminance(self):

        current_value = (self.cs.bin_data("hhh"))
        current_value_red = (current_value[0] / 185)
        current_value_green = (current_value[1] / 321)
        current_value_blue = (current_value[2] / 157)

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
            current_value_red = (self.cs.bin_data("hhh")[0])
            current_value_green = (self.cs.bin_data("hhh")[1])
            current_value_blue = (self.cs.bin_data("hhh")[2])

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

    def move_smooth(self):

        integral = 0
        lasterror = 0

        lightvalue = self.luminance() * 100
        error = lightvalue - self.offset
        integral = integral + error
        derivative = error - lasterror
        turn = self.Kp * error + self.Ki * integral + self.Kd * derivative
        turn = turn / 100
        power_motor_left = (self.Tp + turn)
        power_motor_right = (self.Tp - turn)
        lasterror = error

        self.motor_left.speed_sp = power_motor_left
        self.motor_right.speed_sp = power_motor_right

        current_value = (self.cs.bin_data("hhh"))
        current_value_red = (current_value[0])
        current_value_green = (current_value[1])
        current_value_blue = (current_value[2])

        # print("red:", current_value_red)
        # print("green:", current_value_green)
        # print("blue:", current_value_blue)

        if self.us.distance_centimeters < 30:
            self.motor_right.speed_sp = self.motor_right.speed_sp * (-1)
            sleep(3)

        if 110 < current_value_red < 140 and 35 < current_value_green < 60 and 10 < current_value_blue < 30:
            self.motor_left.command = "stop"
            self.motor_right.command = "stop"
            sleep(3)
            return True

        elif 20 < current_value_red < 40 and 110 < current_value_green < 140 and 70 < current_value_blue < 90:
            self.motor_left.command = "stop"
            self.motor_right.command = "stop"
            sleep(3)
            return True

        else:
            self.motor_left.command = "run-forever"
            self.motor_right.command = "run-forever"
            return False

    def turn_around(self, direct: int):
        self.motor_left.run_to_rel_pos(position_sp=direct * self.a / self.d, speed_sp=200, stop_action="hold")
        self.motor_right.run_to_rel_pos(position_sp=-direct * self.a / self.d, speed_sp=-200, stop_action="hold")
        sleep(0.001)
        self.motor_left.wait_until_not_moving()
        self.motor_right.wait_until_not_moving()

    def scan(self):
        counter = 0
        while counter < 360:
            counter += 45
            self.turn_around(45)
            while True:
                counter += 5
                self.turn_around(5)
                if self.luminance() < 0.5:
                    self.directions.add(planet.Direction(round(counter/90)*90 % 360))
                    break

    def start_driving(self):
        self.wheel_left = []
        self.wheel_right = []
        self.motor_right.reset()
        self.motor_left.reset()

    def while_driving(self):
        motor_left_value = (self.motor_left.position / 360)
        motor_right_value = (self.motor_right.position / 360)
        self.wheel_left.append(motor_left_value)
        self.wheel_right.append(motor_right_value)
        sleep(0.1)

    def stop_driving(self):
        x = 0
        y = 0
        gamma = 0

        for i in range(1, len(self.wheel_left)):
            distance_left = (self.wheel_left[i] - self.wheel_left[i - 1]) * self.d * pi
            distance_right = (self.wheel_right[i] - self.wheel_right[i - 1]) * self.d * pi

            alpha = (distance_right - distance_left) / self.a
            beta = alpha / 2
            if alpha == 0:
                s = distance_left
            else:
                s = ((distance_right + distance_left) / alpha) * sin(beta)
            deltax = - sin(gamma + beta) * s
            deltay = cos(gamma + beta) * s
            gamma = gamma + alpha 
            x = deltax + x
            y = deltay + y

        self.path_status = "Free"
        x = x + round(x / 90)
        y = y + round(x / 90)
        dir = (dir + 180 - (round(degrees(gamma)/90) % 4)*90) % 360
        return x, y, gamma
