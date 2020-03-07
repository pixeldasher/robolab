# !/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import main


class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
    
    
path_dict = {}

def follow_line():
    red = main.cs.color.getRed()
    blue = main.color.getBlue()
    green = main.color.getGreen()


def touch_check(n):
    if (n == 1):
        path_dict.update({"latest_path" : "blocked t"})
        print(path_dict)
        main.stop_moving()
        return False
    else:
        return True


def distance_check(d):
    if (d < 20):
        path_dict.update({"latest_path" : "blocked d"})
        print(path_dict)
        main.turn_around()
        return False
    else:
        return True


def movement_check(boolean):
    if boolean:
        follow_line()
    else:
        main.stop_moving()
