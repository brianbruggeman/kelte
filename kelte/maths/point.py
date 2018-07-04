import typing

from .distance import euclidean_distance

# Position Requirements
#   Provide a simple data store for a point on a grid
#   Provide a distance function
#   Provide a mechanism to add and subtract tuple data (for Direction Enum)


class Position(typing.NamedTuple):
    x: int = 0
    y: int = 0

    @property
    def neighbors(self):
        for x in [self.x - 1, self.x, self.x + 1]:
            for y in [self.y - 1, self.y, self.y + 1]:
                if x == self.x and y == self.y:
                    continue
                yield Position(x, y)

    def __len__(self):
        return 2

    def __bool__(self):
        return True if self.x or self.y else False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Position):
            value = Position(other.x + self.x, other.y + self.y)
        else:
            value = Position(other[0] + self.x, other[1] + self.y)
        return value

    def __sub__(self, other):
        if isinstance(other, Position):
            value = Position(self.x - other.x, self.y - other.y)
        else:
            value = Position(other[0] - self.x, other[1] - self.y)
        return value

    def __eq__(self, other):
        for mine, theirs in zip(self, other):
            if mine != theirs:
                return False
        return True

    def __hash__(self):
        return (self.x, self.y)

    def distance(self, other, func=None) -> float:
        if not isinstance(other, tuple):
            raise ValueError(f"{other} must be of type tuple.")
        if not func:
            func = euclidean_distance
        value = func(self, other)
        return value