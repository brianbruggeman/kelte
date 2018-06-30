from dataclasses import dataclass

from ..math import Position


@dataclass()
class BoundingBox:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def __contains__(self, other):
        contained = False
        if isinstance(other, Position):
            if self.x <= other.x < self.x + self.width:
                if self.y <= other.y < self.y + self.height:
                    contained = True
        return contained


@dataclass()
class Room:
    position: Position = Position()
    bounding_box: BoundingBox = BoundingBox()

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def grid(self):
        if not hasattr(self, '_grid'):
            self._grid = []
            for y in range(self.bounding_box.height):
                row = []
                for x in range(self.bounding_box.width):
                    edge = False
                    if y in [0, self.bounding_box.height - 1]:
                        edge = True
                    elif x in [0, self.bounding_box.width - 1]:
                        edge = True
                    if edge:
                        row.append('#')
                    else:
                        row.append('.')
                self._grid.append(row)
        return self._grid

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                yield Position(x + self.x, y + self.y), col

    def __contains__(self, other):
        contained = False
        if isinstance(other, Position):
            if other in self.bounding_box:
                return True

        elif isinstance(other, Room):
            for point, tile in self:
                if point in other:
                    contained = True
                    break

        else:
            contained = True
            for point, tile in self:
                if point not in other:
                    contained = False
                    break

        return contained

    def __str__(self):
        data = []
        for y, row in enumerate(self.grid):
            row = ''.join(map(str, row))
            data.append(row)
        return '\n'.join(data)
