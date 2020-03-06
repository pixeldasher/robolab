# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import main


class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)


def colorcheck(color):
    if color == 5 or color == 2 or color == 0:
        print("Stop")
        main.m.speed_sp = 0
        main.m2.speed_sp = 0
        main.m.command = "run-forever"
        main.m2.command = "run-forever"
    elif color == 1:
        main.m.speed_sp = 200
        main.m2.speed_sp = 200
        main.m.command = "run-forever"
        main.m2.command = "run-forever"


def distancecheck(centimeters):
    print(centimeters)
