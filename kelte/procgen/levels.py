import typing
from dataclasses import dataclass, field

from ..math import Position
from ..tiles import get_tile
from .cooridors import Cooridor
from .rooms import Room


@dataclass()
class LevelSize:
    width: int = 0
    height: int = 0


@dataclass()
class Level:
    width: int = 0
    height: int = 0
    rooms: typing.List[Room] = field(default_factory=list)
    cooridors: typing.List[Cooridor] = field(default_factory=list)

    @property
    def grid(self):
        if not hasattr(self, "_grid"):
            self._populate()
        return self._grid

    def __getitem__(self, key):
        return self.grid[key.y][key.x]

    def __setitem__(self, key, value):
        self.grid[key.y][key.x] = value

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

    def _populate(self):
        data = []

        default_tile = get_tile("wall")

        # fill the entire level with walls
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(default_tile.copy())
            data.append(row)

        # blit rooms onto level
        for room in self.rooms:
            for position, tile in room:
                data[position.y][position.x] = tile

        # blit cooridors onto level
        for cooridor in self.cooridors:
            for position, tile in cooridor:
                data[position.y][position.x] = tile

        self._grid = data

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                yield Position(x, y), tile

    def __repr__(self):
        return f"{type(self).__name__}(width={self.width}, height={self.height}, room_count={len(self.rooms)})"

    def __str__(self):
        if not hasattr(self, "_grid"):
            self._populate()
        string = "\n".join("".join(str(c) for c in r) for r in self._grid)
        return string
