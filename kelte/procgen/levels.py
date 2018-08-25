import typing
from dataclasses import dataclass, field

from kelte.engine.ecs import Entity
from kelte.engine.maths import Position

from ..tiles import Tile, get_tile
from .cooridors import Cooridor
from .rooms import Room


@dataclass
class LevelSize:
    width: int = 0
    height: int = 0


@dataclass
class TileStack:
    tiles: typing.List[Tile] = field(default_factory=list)

    @property
    def tile(self):
        if len(self.tiles):
            return self.tiles[-1]


@dataclass
class Level:
    width: int = 0
    height: int = 0
    rooms: typing.List[Room] = field(default_factory=list)
    cooridors: typing.List[Cooridor] = field(default_factory=list)
    entities: typing.List[Entity] = field(default_factory=list)

    @property
    def items(self):
        data_type = 'item'
        data = []
        for entity in self.entities:
            if entity.type == data_type:
                data.append(entity)
        return data

    @property
    def light_sources(self):
        data_type = 'light'
        data = []
        for entity in self.entities:
            if entity.type == data_type:
                data.append(entity)
        return data

    @property
    def mobs(self):
        data_type = 'mob'
        data = []
        for entity in self.entities:
            if entity.type == data_type:
                data.append(entity)
        return data

    @property
    def grid(self):
        if not hasattr(self, "_grid"):
            self._populate()
        return self._grid

    @property
    def edges(self):
        if not hasattr(self, '_edges'):
            edges = []
            for x in range(0, self.width):
                edges.append(Position(x, 0))
                edges.append(Position(x, self.height))
            for y in range(0, self.height):
                edges.append(Position(0, y))
                edges.append(Position(self.height, y))
            self._edges = edges
        yield from self._edges

    def __getitem__(self, key):
        x, y = tuple(key)
        value = self.grid[y][x]
        return value

    def __setitem__(self, key, value):
        x, y = key
        self.grid[y][x] = value

    def __contains__(self, other):
        contained = False
        if isinstance(other, Position):
            if 1 <= other.x <= self.width - 1:
                if 1 <= other.y <= self.height - 1:
                    contained = True
        elif isinstance(other, Room):
            if other.x2 < self.width and other.y2 < self.height:
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

        # blit entities onto levels
        for entity in self.entities:
            data[entity.position] = entity.tile

        self._grid = data

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                yield Position(x, y), tile

    def __repr__(self):
        return f"{type(self).__name__}(width={self.width}, height={self.height}, room_count={len(self.rooms)})"

    def __str__(self):
        string = "\n".join("".join(tile.rendered for tile in row) for row in self.grid)
        return string
