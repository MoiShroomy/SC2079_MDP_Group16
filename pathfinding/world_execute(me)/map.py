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

        assert all(map(lambda obstacle: self.in_bounds(obstacle), self.obstacles))
    
    
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
    
    def generate_goals(self):
        """
        Go through the obstacle list and generate goal position for robot to stand and take picture
        """
        #TODO Generate goal positions

    def generate_edges(self, V: list[tuple]):
        """
        Given a list of coordinates (representing target vertices in graph)
        generate the possible edges connecting the graph

        Params:
            V: list(tuple)
                list of (x, y, theta) representing vertices
        """

        