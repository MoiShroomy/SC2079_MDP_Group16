from enum import Enum
from dataclasses import dataclass, replace

"""
I'm using dataclasses solely for the ability to clone using replace()
This will be useful when implmenting Reeds Shepp Paths if I get to that
due to the timeflip and reverse functions mentioned in the paper to easily generate similar looking paths
"""

class Direction(Enum):
    LEFT = -1
    RIGHT = 1
    STRAIGHT = 0

class Gear(Enum):
    FORWARD = 1
    BACKWARD = -1

@dataclass(eq=True)
class PathSegment:
    """
    This class represents a single segment of a path (so either the curve or the straight part)
    A full path would thus be an array of PathSegments
    """
    dist: float
    dir: Direction
    gear: Gear

    @classmethod
    def create(cls, dist: float, dir: Direction, gear: Gear):
        if dist >= 0:
            return cls(dist, dir, gear)
        else:
            return cls(-dist, dir, gear).reverse_gear()

    def __repr__(self):
        s = "{ Direction: " + self.dir.name + "\tGear: " + self.gear.name + "\tdistance: " + str(round(self.dist, 2)) + " }"
        return s

    def reverse_steering(self):
        dir = Direction(-self.dir.value)
        return replace(self, dir=dir)

    def reverse_gear(self):
        gear = Gear(-self.gear.value)
        return replace(self, gear=gear)