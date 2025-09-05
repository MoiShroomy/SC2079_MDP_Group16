from math import pi, cos, sin, atan2, acos, dist
from .path_algo import PathAlgo

#Every coordinate is represented with (x, y, theta), theta follows polar standard, so east is 0 radians/degrees

#TODO convert to using degrees in code

"""
REGARDING FLOATING POINT PRECISION:
Working in radians led to compounding inaccuracies due to floating point representation
being gimped in computers due to limited memory

I HAVE A FEELING THIS IS WHY OTHER GROUPS GOT ROBOTS MOVING IN ELIPSES INSTEAD OF CIRCLES
Also probably due to real world interference

I am unsure how much of an issue this will be, will keep an eye out
"""

"""
REGARDING FORMULAS:
Rotating a vector clockwise or anticlockwise CORRECTLY is very important, as is using the correct x or y coordinate
Throughout debugging there was a lot of time wasted because of an incorrect rotation about an angle
ALWAYS DOUBLE CHECK EACH FUNCTION AGAINST MULTIPLE TEST CASES AND VERIFY SOLUTION BY HAND (or Desmos lol)
Drawing out the diagram helps
"""

"""
REGARDING CCC DUBIN PATH:
I have yet to figure out how to deduce which side of the circles should the third circle be
There's 2 possible positions (opposing corners of rhombus formed by centers)
But one leads to a shorter path
For now I have decided to just calculate both paths and output the shorter one
DO TEST THESE FUNCTIONS CAREFULLY, HIGH CHANCE YO SLEEPY HEAD MADE A MISTAKE
"""


class Dubins(PathAlgo):
    """
    Class implementing methods to calculate Dubins paths
    """

    def __init__(self, radius):
        assert radius > 0
        self.radius = radius

    def find_center(self, pos: tuple):
        """
        Calculates center of left and right circles

        Params:
            pos: tuple
                (x, y, theta) tuple representing the coordinates we want to generate circle centers for
                theta represented in radians
        
        Returns:
            An array of tuples of length 2, 
            with the first element being the left circle center (x,y)
            and the 2nd element being the right circle center (x,y)
        """

        #Calculate polar angle of left and right circle centers relative to given pos
        r_center_dir = pos[2] - pi/2 #Rotate clockwise
        l_center_dir = pos[2] + pi/2 #Rotate anticlockwise

        r_center_pos = (pos[0] + self.radius * cos(r_center_dir), pos[1] + self.radius * sin(r_center_dir))
        l_center_pos = (pos[0] + self.radius * cos(l_center_dir), pos[1] + self.radius * sin(l_center_dir))

        return [l_center_pos, r_center_pos]
    
    def arc_length(self, p: tuple, pt1: tuple, center: tuple, dir: str):
        """
        Calculates arc length given center and 2 points on the circle

        Params:
            p: tuple
                (x, y) tuple, the robot start point on the circle
            pt1: tuple
                (x, y) tuple, the second point on the circle
            center: tuple
                (x, y) tuple, the center of the circle
            dir: str
                L for left, R for right
        
        Returns:
            The length of the arc between p and pt1, with regards to direction chosen
        """

        dir = dir.upper()
        assert dir in "LR"
        
        V1 = (p[0] - center[0], p[1] - center[1])
        V2 = (pt1[0] - center[0], pt1[1] - center[1])

        alpha = atan2(V2[1], V2[0]) - atan2(V1[1], V1[0])

        if alpha < 0 and dir == "L":
            alpha = alpha + 2*pi
        elif alpha > 0 and dir == "R":
            alpha = alpha - 2*pi

        arc_length = abs(self.radius * alpha)

        return arc_length

    def LSL(self, start: tuple, end: tuple):
        """
        Left-Straight-Left Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates

        """
        
        #Find the centers of the 2 left turning circles
        p1 = self.find_center(start)[0] #start point left turning circle
        p2 = self.find_center(end)[0] #end point left turning circle

        l = dist(p1, p2) #length of straight segment

        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p3
        alpha = atan2(p2[1]-p1[1], p2[0]-p1[0]) #Polar angle of vector from p1 to p3 (coincidentally angle for the straight segment too)

        V2 = (V1[1], -V1[0]) #clockwise orthogonal vector to V1

        pt1 = (p1[0] + (self.radius/l)*V2[0] , p1[1] + (self.radius/l)*V2[1]) #tangent point on first circle
        pt2 = (pt1[0] + V1[0] , pt1[1] + V1[1])

        #find total length of path
        arc_1 = self.arc_length(start, pt1, center=p1, dir="L")
        arc_2 = self.arc_length(end, pt2, center=p2, dir="L")

        total_length = arc_1 + l + arc_2

        return (total_length, pt1, pt2)

    def RSR(self, start: tuple, end: tuple):
        """
        Right-Straight-Right Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates

        """
        
        #Find the centers of the 2 right turning circles
        p1 = self.find_center(start)[1] #start point right turning circle
        p2 = self.find_center(end)[1] #end point right turning circle

        l = dist(p1, p2) #length of straight segment

        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p2
        alpha = atan2(p2[1]-p1[1], p2[0]-p1[0]) #Polar angle of vector from p1 to p2 (coincidentally angle for the straight segment too)

        V2 = (-V1[1], V1[0]) #anticlockwise orthogonal vector to V1

        pt1 = (p1[0] + (self.radius/l)*V2[0] , p1[1] + (self.radius/l)*V2[1]) #tangent point on first circle
        pt2 = (pt1[0] + V1[0] , pt1[1] + V1[1])

        #find total length of path
        arc_1 = self.arc_length(start, pt1, center=p1, dir="R")
        arc_2 = self.arc_length(pt2, end, center=p2, dir="R")

        total_length = arc_1 + l + arc_2

        return (total_length, pt1, pt2)
        
    def RSL(self, start: tuple, end: tuple):
        """
        Right-Straight-Left Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates
        """

        #Find the centers of the 2 right turning circles
        p1 = self.find_center(start)[1] #start point right turning circle
        p2 = self.find_center(end)[0] #end point left turning circle

        d = dist(p1, p2) #distance between 2 centers

        l = (d**2 - (2*self.radius)**2)**0.5

        delta = acos((2*self.radius)/d)

        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p2
        V2 = (V1[0]*cos(delta) - V1[1]*sin(delta),
              V1[0]*sin(delta) + V1[1]*cos(delta)) #Counterclockwise V1 
        V3 = (-V2[0], -V2[1]) #Reverse of V2
        
        pt1 = (p1[0] + (self.radius/d)*V2[0], 
               p1[1] + (self.radius/d)*V2[1])
        pt2 = (p2[0] + (self.radius/d)*V3[0], 
               p2[1] + (self.radius/d)*V3[1])
        
        #find total length of path
        arc_1 = self.arc_length(start, pt1, center=p1, dir="R")
        arc_2 = self.arc_length(pt2, end, center=p2, dir="L")

        total_length = arc_1 + l + arc_2

        return (total_length, pt1, pt2)
    
    def LSR(self, start: tuple, end: tuple):
        """
        Right-Straight-Left Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates
        """

        #Find the centers of the 2 right turning circles
        p1 = self.find_center(start)[0] #start point left turning circle
        p2 = self.find_center(end)[1] #end point right turning circle

        d = dist(p1, p2) #distance between 2 centers

        l = (d**2 - (2*self.radius)**2)**0.5

        delta = acos((2*self.radius)/d)

        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p2
        V2 = (V1[0]*cos(delta) + V1[1]*sin(delta),
              -V1[0]*sin(delta) + V1[1]*cos(delta)) #Clockwise V1 
        V3 = (-V2[0], -V2[1]) #Reverse of V2

        pt1 = (p1[0] + (self.radius/d)*V2[0], 
               p1[1] + (self.radius/d)*V2[1])
        pt2 = (p2[0] + (self.radius/d)*V3[0], 
               p2[1] + (self.radius/d)*V3[1])
        
        #find total length of path
        arc_1 = self.arc_length(start, pt1, center=p1, dir="L")
        arc_2 = self.arc_length(pt2, end, center=p2, dir="R")

        total_length = arc_1 + l + arc_2

        return (total_length, pt1, pt2)

    def RLR(self, start: tuple, end: tuple):
        """
        Right-Left-Right Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates
        """
        #Find the centers of the 2 right turning circles
        p1 = self.find_center(start)[1] #start point right turning circle
        p2 = self.find_center(end)[1] #end point right turning circle

        d = dist(p1, p2) #distance between 2 centers
        #CCC Path only useful if d < 4r, else straight go to CSC
        if d > 4*self.radius:
            total_length = float('inf') #Make path length super long so algo ignores this immediately
            return (total_length, {}) #TODO when output format is finalized, don't forget to edit here

        q = ((p1[0] + p2[0])/2 ,(p1[1] + p2[1])/2) #Midpoint between center of 2 circles
        
        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p2
        
        #From here we try both possible Circle 3, and we output the shorter path
        
        clockwise_V2 = (V1[1], -V1[0])
        anticlockwise_V2 = (-V1[1], V1[0])

        d1 = ((2*self.radius)**2 - (d/2)**2)**0.5 #Distance from q to p3

        #||V2|| = d
        p3_c = (q[0] + (d1/d)* clockwise_V2[0], 
                q[1] + (d1/d)* clockwise_V2[1])
        p3_ac = (q[0] + (d1/d)* anticlockwise_V2[0], 
                 q[1] + (d1/d)* anticlockwise_V2[1])
        
        pt1_c = ((p1[0] + p3_c[0])/2, (p1[1] + p3_c[1])/2)
        pt2_c = ((p2[0] + p3_c[0])/2, (p2[1] + p3_c[1])/2)

        pt1_ac = ((p1[0] + p3_ac[0])/2, (p1[1] + p3_ac[1])/2)
        pt2_ac = ((p2[0] + p3_ac[0])/2, (p2[1] + p3_ac[1])/2)


        #Find total length of both paths
        arc_1_c = self.arc_length(start, pt1_c, center=p1, dir="R")
        arc_2_c = self.arc_length(pt1_c, pt2_c, center=p2, dir="L")
        arc_3_c = self.arc_length(pt2_c, end, center=p1, dir="R")

        total_length_c = arc_1_c + arc_2_c + arc_3_c

        arc_1_ac = self.arc_length(start, pt1_ac, center=p1, dir="R")
        arc_2_ac = self.arc_length(pt1_c, pt2_ac, center=p2, dir="L")
        arc_3_ac = self.arc_length(pt2_ac, end, center=p1, dir="R")

        total_length_ac = arc_1_ac + arc_2_ac + arc_3_ac

        #Return the shortest path
        if total_length_c < total_length_ac:
            return (total_length_c, pt1_c, pt2_c)
        else:
            return (total_length_ac, pt1_ac, pt2_ac)
    
    def LRL(self, start: tuple, end: tuple):
        """
        Left-Right_Left Path 

        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates
        """
        #Find the centers of the 2 right turning circles
        p1 = self.find_center(start)[0] #start point left turning circle
        p2 = self.find_center(end)[0] #end point left turning circle

        d = dist(p1, p2) #distance between 2 centers
        #CCC Path only useful if d < 4r, else straight go to CSC
        if d > 4*self.radius:
            total_length = float('inf') #Make path length super long so algo ignores this immediately
            return (total_length, {}) #TODO when output format is finalized, don't forget to edit here

        q = ((p1[0] + p2[0])/2 ,(p1[1] + p2[1])/2) #Midpoint between center of 2 circles
        
        V1 = (p2[0]-p1[0], p2[1]-p1[1]) #Vector from p1 to p2
        
        #From here we try both possible Circle 3, and we output the shorter path
        
        clockwise_V2 = (V1[1], -V1[0])
        anticlockwise_V2 = (-V1[1], V1[0])

        d1 = ((2*self.radius)**2 - (d/2)**2)**0.5 #Distance from q to p3

        #||V2|| = d
        p3_c = (q[0] + (d1/d)* clockwise_V2[0], 
                q[1] + (d1/d)* clockwise_V2[1])
        p3_ac = (q[0] + (d1/d)* anticlockwise_V2[0], 
                 q[1] + (d1/d)* anticlockwise_V2[1])
        
        pt1_c = ((p1[0] + p3_c[0])/2, (p1[1] + p3_c[1])/2)
        pt2_c = ((p2[0] + p3_c[0])/2, (p2[1] + p3_c[1])/2)

        pt1_ac = ((p1[0] + p3_ac[0])/2, (p1[1] + p3_ac[1])/2)
        pt2_ac = ((p2[0] + p3_ac[0])/2, (p2[1] + p3_ac[1])/2)


        #Find total length of both paths
        arc_1_c = self.arc_length(start, pt1_c, center=p1, dir="L")
        arc_2_c = self.arc_length(pt1_c, pt2_c, center=p2, dir="R")
        arc_3_c = self.arc_length(pt2_c, end, center=p1, dir="L")

        total_length_c = arc_1_c + arc_2_c + arc_3_c

        arc_1_ac = self.arc_length(start, pt1_ac, center=p1, dir="L")
        arc_2_ac = self.arc_length(pt1_c, pt2_ac, center=p2, dir="R")
        arc_3_ac = self.arc_length(pt2_ac, end, center=p1, dir="L")

        total_length_ac = arc_1_ac + arc_2_ac + arc_3_ac

        #Return the shortest path
        if total_length_c < total_length_ac:
            return (total_length_c, pt1_c, pt2_c)
        else:
            return (total_length_ac, pt1_ac, pt2_ac)
        
    def get_shortest_path(self, start: tuple, end: tuple):
        """
        Calculates all dubins paths between start and end points
        and returns shortest one
        Params:
            start: tuple
                (x, y, theta) start coordinates
            end: tuple
                (x, y, theta) end coordinates
        """
        paths = []

        funcs = [self.LSL, self.RSR, self.RSL, self.LSR, self.RLR, self.LRL]

        for f in funcs:
            paths.append(f(start, end))

        return min(paths, key = lambda t: t[0])
