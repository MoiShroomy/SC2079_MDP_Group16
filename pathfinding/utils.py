from math import pi

def rad2deg(rad):
    """
    Converts radians to degrees
    """
    return 180 * rad / pi

def deg2rad(deg):
    """
    Converts degrees to radians
    """
    return pi * deg / 180