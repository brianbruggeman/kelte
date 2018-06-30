from dataclasses import dataclass
from enum import Enum

from .point import Position


class Direction(Enum):
    NONE: Position = Position(0, 0)

    # Cardinal directions
    NORTH: Position = Position(0, -1)
    SOUTH: Position = Position(0, 1)
    EAST: Position = Position(1, 0)
    WEST: Position = Position(-1, 0)

    NORTH_EAST: Position = NORTH + EAST
    NORTH_WEST: Position = NORTH + WEST
    SOUTH_EAST: Position = SOUTH + EAST
    SOUTH_WEST: Position = SOUTH + WEST

    UP: Position = Position(0, -1)
    DOWN: Position = Position(0, 1)
    RIGHT: Position = Position(1, 0)
    LEFT: Position = Position(-1, 0)

    UP_RIGHT = UP + RIGHT
    UP_LEFT = UP + LEFT
    DOWN_RIGHT = DOWN + RIGHT
    DOWN_LEFT = DOWN + LEFT

    @classmethod
    def get(cls, other):
        for name, value in cls.__members__.items():
            if value == other:
                return getattr(cls, name)

    def __get__(self, obj, type=None):
        return self.value

    def __set__(self, obj, value):
        self.value = value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __iter__(self):
        yield from self.value

    def __str__(self):
        return self.name


@dataclass
class Vector:
    direction: Direction = Direction.NORTH
    magnitude: int = 0
