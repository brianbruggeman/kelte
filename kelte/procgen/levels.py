import typing
from dataclasses import dataclass, field

from ..math import Position
from .rooms import Room
from .cooridors import Cooridor


@dataclass()
class Level:
    width: int = 0
    height: int = 0
    rooms: typing.List[Room] = field(default_factory=list)
    cooridors: typing.List[Cooridor] = field(default_factory=list)

    def __contains__(self, other):
        contained = False
        if isinstance(other, Position):
            if 1 <= other.x <= self.width - 1:
                if 1 <= other.y <= self.height - 1:
                    contained = True
        elif isinstance(other, Room):
            if other.bounding_box.width + other.position.x < self.width:
                if other.bounding_box.height + other.position.y < self.height:
                    contained = True
        return contained

    def __repr__(self):
        return f'{type(self).__name__}(width={self.width}, height={self.height}, room_count={len(self.rooms)})'

    def __str__(self):
        data = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(' ')
            data.append(row)

        for room in self.rooms:
            for position, tile in room:
                data[position.y][position.x] = tile

        for cooridor in self.cooridors:
            for position, tile in cooridor:
                data[position.y][position.x] = tile

        string = '\n'.join(''.join(str(c) for c in r) for r in data)
        return string
