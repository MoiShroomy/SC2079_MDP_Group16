
#I did not use an enum for the facing because I got annoyed constantly having to import a global enum
#Plus using an angle allows for diagonal facing obstacles (a feature that will never be needed :D)

class Obstacle:

    def __init__(self, x: float, y: float, facing: float, side_length = 10, collision_mask = 40):
        """
        x, y is measured from the bottom left corner of the obstacle
        Obstacle modeled as a square
        """
        self.x = x
        self.y = y
        self.facing = facing #Angle of vector where picture is, so if picture is on right facing = 0 for example
        self.side_length = side_length #Length of one side of obstacle
        self.collision_mask = collision_mask #Size of collision mask with obstacle at center

        self.bound_E, self.bound_W, self.bound_N, self.bound_S = self.domain_expansion()

    def domain_expansion(self):
        """
        Calculates the bounds for the collision mask with obstacle at center
        Assumes x, y is measured from bottom left corner of obstacle
        """
        bound_E = self.x + self.side_length + (self.collision_mask - self.side_length)/2
        bound_W = self.x - (self.collision_mask - self.side_length)/2
        bound_N = self.y + self.side_length + (self.collision_mask - self.side_length)/2
        bound_S = self.y - (self.collision_mask - self.side_length)/2

        return (bound_E, bound_W, bound_N, bound_S)
        
    def collided(self, coord: tuple):
        """
        Check if a given coordinate (x, y, theta) is in the collision map
        """
        return (
            self.bound_W <= coord[0] <= self.bound_E and
            self.bound_S <= coord[1] <= self.bound_N
        )