from math import pi, sqrt, atan2

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

def M(theta):
        """
        Return the angle phi = theta mod (2 pi) such that -pi <= theta < pi.
        """
        theta = theta % (2*pi)
        if theta < -pi: return theta + 2*pi
        if theta >= pi: return theta - 2*pi
        return theta

def R(x, y):
    """
    Return the polar coordinates (r, theta) of the point (x, y).
    """
    r = sqrt(x*x + y*y)
    theta = atan2(y, x)
    return r, theta