import random

from ..maths import Position
from ..tiles import get_tile
from .rooms import Room


class Cooridor:
    @property
    def points(self):
        if not hasattr(self, "_points"):
            self._build()
        return self._points

    @property
    def start(self):
        return self.start_room.center

    @property
    def end(self):
        return self.end_room.center

    def __init__(self, start: Room, end: Room):
        self.start_room = start
        self.end_room = end
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
            in_room = True
            last_position = Position()
            for x in range(xmin, xmax):
                position = Position(x, self.start.y)
                if position not in self.start_room:
                    if in_room is True:
                        self.start_room.doors.append(last_position)
                        in_room = False
                self._points.append((position, default_tile.copy()))
                last_position = position

            last_position = Position()
            for y in range(ymin, ymax):
                position = Position(self.end.x, y)
                if position in self.end_room:
                    if in_room is False:
                        self.end_room.doors.append(last_position)
                        in_room = True
                self._points.append((position, default_tile.copy()))
                last_position = position

        else:
            in_room = True
            last_position = Position()
            for y in range(ymin, ymax):
                position = Position(self.start.x, y)
                if position not in self.start_room:
                    if in_room is True:
                        self.start_room.doors.append(last_position)
                        in_room = False
                self._points.append((position, default_tile.copy()))
                last_position = position

            last_position = Position()
            for x in range(xmin, xmax):
                position = Position(x, self.end.y)
                if position in self.end_room:
                    if in_room is False:
                        self.end_room.doors.append(last_position)
                        in_room = True
                self._points.append((position, default_tile.copy()))
                last_position = position
