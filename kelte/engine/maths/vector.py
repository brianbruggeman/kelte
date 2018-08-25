from dataclasses import dataclass

from .point import Point


@dataclass
class Direction(Point):
    x: int = 0
    y: int = 0


NONE: Direction = Direction(0, 0)

NORTH: Direction = Direction(0, -1)
SOUTH: Direction = Direction(0, 1)
EAST: Direction = Direction(1, 0)
WEST: Direction = Direction(-1, 0)

NORTH_EAST: Direction = NORTH + EAST
NORTH_WEST: Direction = NORTH + WEST
SOUTH_EAST: Direction = SOUTH + EAST
SOUTH_WEST: Direction = SOUTH + WEST

UP: Direction = Direction(0, -1)
DOWN: Direction = Direction(0, 1)
RIGHT: Direction = Direction(1, 0)
LEFT: Direction = Direction(-1, 0)

UP_RIGHT: Direction = UP + RIGHT
UP_LEFT: Direction = UP + LEFT
DOWN_RIGHT: Direction = DOWN + RIGHT
DOWN_LEFT: Direction = DOWN + LEFT
