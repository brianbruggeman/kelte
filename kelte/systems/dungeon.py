import typing


class BoundingBox(typing.NamedTuple):
    x: int = 0
    y: int = 0


class Dungeon:

    def __init__(self):
        self.levels = []


class Level:

    def __init__(self):
        self.rooms = []


class Room:

    @property
    def bounding_box(self):
        x = len(self.grid[0])
        y = len(self.grid)
        return BoundingBox(x, y)

    def __init__(self):
        self.grid = []

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(self.grid):
                yield y, x, col




def build_dungeon():
