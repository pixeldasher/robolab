# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import ev3dev.ev3 as ev3
from time import sleep
from math import sin, cos, pi, degrees, radians
from planet import Direction


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

        self.a = 8
        self.d = 5.6
        self.k_p = 112.5
        self.k_i = 425
        self.k_d = 36.25
        self.offset = 50
        self.t_p = 112.5
        self.integral = 0
        self.derivative = 0
        self.lasterror = 0
        self.wheel_left = None
        self.wheel_right = None

        self.directions = set()
        self.path_status = "free"
        self.path_weight = 0

        self.curr_x = 0
        self.curr_y = 0
        self.dest_x = 0
        self.dest_y = 0

        self.curr_d = 0
        self.dest_d = 0

        self.next_d = 0

    def update_coords(self):
        # Use the destination coords of the last path as the current coords
        self.curr_x = self.dest_x
        self.curr_y = self.dest_y

        # Reset destination coords
        self.dest_x = 0
        self.dest_y = 0

        # sets the path status to free as default after it has been set to "blocked" at collision with an object
        self.path_status = "free"

    def correct_dir(self):
        turn_to = ((-(self.dest_d + 180) % 360) + self.next_d) % 360
        print(self.dest_d, self.next_d, turn_to)
        self.turn_around(turn_to)
        self.curr_d = self.next_d

    def correct_pos(self):
        self.motor_left.run_to_rel_pos(position_sp=135, speed_sp=90)
        self.motor_right.run_to_rel_pos(position_sp=135, speed_sp=90)
        sleep(0.01)
        self.motor_left.wait_until_not_moving()

    def luminance(self):
        current_value = (self.cs.bin_data("hhh"))
        current_value_red = (current_value[0] / 185)
        current_value_green = (current_value[1] / 321)
        current_value_blue = (current_value[2] / 157)

        value = (0.2126 * current_value_red + 0.7152 *
                 current_value_green + 0.0722 * current_value_blue)
        return value

    def move_to_point(self):
        lightvalue = self.luminance() * 100
        error = lightvalue - self.offset
        self.integral = self.integral + error
        self.derivative = error - self.lasterror
        turn = (self.k_p * error) + (self.k_i/100 * self.integral) + (self.k_d * self.derivative)
        turn = turn / 97.5
        power_motor_left = (self.t_p + turn)
        power_motor_right = (self.t_p - turn)
        self.lasterror = error

        self.motor_left.speed_sp = power_motor_left
        self.motor_right.speed_sp = power_motor_right

        current_value = (self.cs.bin_data("hhh"))
        current_value_red = (current_value[0])
        current_value_green = (current_value[1])
        current_value_blue = (current_value[2])

        if self.us.distance_centimeters <= 5:
            self.turn_around(170)
            self.path_status = "blocked"
            ev3.Sound.play_song((('G4', 'e3'), ('D4', 'e3')))

        if 110 < current_value_red < 140 and 35 < current_value_green < 60 and 10 < current_value_blue < 30:
            self.motor_left.command = "stop"
            self.motor_right.command = "stop"
            sleep(1)
            return True

        elif 20 < current_value_red < 40 and 110 < current_value_green < 140 and 70 < current_value_blue < 90:
            self.motor_left.command = "stop"
            self.motor_right.command = "stop"
            sleep(1)
            return True
        else:
            self.motor_left.command = "run-forever"
            self.motor_right.command = "run-forever"
            return False

    # Turn around by the given angle
    def turn_around(self, direct: int):
        self.derivative = 0
        self.integral = 0
        self.error = 0
        self.motor_left.run_to_rel_pos(
            position_sp=(direct-22.5) * self.a / self.d, speed_sp=150, stop_action="hold")
        self.motor_right.run_to_rel_pos(
            position_sp=-(direct-22.5) * self.a / self.d, speed_sp=-150, stop_action="hold")

        while 'running' in (self.motor_left.state + self.motor_right.state):
            sleep(0.1)

        while True:
            self.motor_left.run_to_rel_pos(
                position_sp=(60) * self.a / self.d, speed_sp=50, stop_action="hold")
            self.motor_right.run_to_rel_pos(
                position_sp=-(60) * self.a / self.d, speed_sp=-50, stop_action="hold")
            if self.luminance() <= 0.33:
                self.motor_left.speed_sp = 0
                self.motor_right.speed_sp = 0
                self.motor_left.stop()
                self.motor_right.stop()
                break

    # Scans the robots surroundings for possible paths

    def scan(self):

        self.directions = set()
        self.motor_left.reset()
        self.motor_right.reset()
        self.motor_left.run_to_rel_pos(
            position_sp=360 * self.a / self.d, speed_sp=150, stop_action="hold")
        self.motor_right.run_to_rel_pos(
            position_sp=-360 * self.a / self.d, speed_sp=-150, stop_action="hold")

        while 'running' in (self.motor_left.state + self.motor_right.state):
            if self.luminance() <= 0.33:
                self.directions.add(Direction(
                    (self.dest_d + 180 + round((self.d / self.a * self.motor_left.position)/90)*90) % 360))
        self.motor_left.run_to_abs_pos(position_sp=0,speed_sp=150,stop_action="hold")
        self.motor_right.run_to_abs_pos(position_sp=0,speed_sp=150,stop_action="hold")
        sleep(0.01)
        self.motor_left.wait_until_not_moving()
        self.motor_right.wait_until_not_moving()


    def init_mov(self):
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

    def save_data(self):
        x = 0
        y = 0
        gamma = -radians(self.curr_d)

        for i in range(1, len(self.wheel_left)):
            distance_left = (
                self.wheel_left[i] - self.wheel_left[i - 1]) * self.d * pi
            distance_right = (
                self.wheel_right[i] - self.wheel_right[i - 1]) * self.d * pi

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

        self.dest_x = self.curr_x + round(x / 50)
        self.dest_y = self.curr_y + round(y / 50)
        self.dest_d = (180 - (round(degrees(gamma)/90) % 4)*90) % 360
