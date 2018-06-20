import typing

from .distance import euclidean_distance


# Position Requirements
#   Provide a simple data store for a point on a grid
#   Provide a distance function
#   Provide a mechanism to add and subtract tuple data (for Direction Enum)


class Position(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other):
        value = self
        if isinstance(other, Position):
            value = Position(other.x + self.x, other.y + self.y)
        return value

    def __sub__(self, other):
        value = Position(0, 0)
        if isinstance(other, Position):
            value = Position(self.x - other.x, self.y - other.y)
        return value

    def distance(self, other, func=None) -> float:
        if not isinstance(other, tuple):
           raise ValueError(f'{other} must be of type tuple.')
        if not func:
            func = euclidean_distance
        value = func(self, other)
        return value
