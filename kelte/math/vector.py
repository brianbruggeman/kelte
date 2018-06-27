from enum import Enum
from dataclasses import dataclass

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


@dataclass
class Vector:
    direction: Direction = Direction.NORTH
    magnitude: int = 0
