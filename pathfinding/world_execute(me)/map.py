from obstacle import Obstacle

class Map:

    def __init__(self, obstacles: list[Obstacle], side_length = 200):
        """
        Bottom left corner of map is (0,0), expands right and upwards
        Map modelled as a square
        """
        self.side_length = side_length
        self.obstacles = obstacles

        self.x = 0
        self.y = 0

        self.bound_E = self.x + side_length
        self.bound_W = self.x
        self.bound_N = self.y + side_length
        self.bound_S = self.y
    
    
    def in_bounds(self, obstacle: Obstacle):
        """
        Check if a given obstacle is within the map
        """
        return (
            self.bound_W <= obstacle.x <= self.bound_E and
            self.bound_S <= obstacle.y <= self.bound_N and
            self.bound_W <= obstacle.x + obstacle.side_length <= self.bound_E and
            self.bound_S <= obstacle.y + obstacle.side_length <= self.bound_N
        )
                