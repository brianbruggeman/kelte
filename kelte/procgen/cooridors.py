import random

from ..math import Position
from ..tiles import get_tile
from .rooms import Room


class Cooridor:
    @property
    def points(self):
        if not hasattr(self, "_points"):
            self._build()
        return self._points

    def __init__(self, start: Room, end: Room):
        self.start = start.center
        self.end = end.center
        self._build()

    def __iter__(self):
        yield from self.points

    def _build(self):
        self._points = []
        xmin = min((self.start.x, self.end.x))
        xmax = max((self.start.x, self.end.x)) + 1
        ymin = min((self.start.y, self.end.y))
        ymax = max((self.start.y, self.end.y)) + 1

        default_tile = get_tile("floor")

        build_horizontal_first = random.randint(0, 1)
        if build_horizontal_first:
            for x in range(xmin, xmax):
                position = Position(x, self.start.y)
                self._points.append((position, default_tile.copy()))
            for y in range(ymin, ymax):
                position = Position(self.end.x, y)
                self._points.append((position, default_tile.copy()))

        else:
            for y in range(ymin, ymax):
                position = Position(self.start.x, y)
                self._points.append((position, default_tile.copy()))
            for x in range(xmin, xmax):
                position = Position(x, self.end.y)
                self._points.append((position, default_tile.copy()))
