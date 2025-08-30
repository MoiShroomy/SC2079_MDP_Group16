from abc import ABC, abstractmethod

class PathAlgo(ABC):

    """
    An abstract class for all pathfinding algorithm classes to implement
    (Dubins, Reed-Shepp etc.)
    """

    @abstractmethod
    def get_shortest_path(self, start: tuple, end: tuple):
        """
        Returns the shortest path between start and end coordinates
        """
        pass