from dataclasses import dataclass

from ..math import Position


@dataclass()
class RoomSize:
    width: int = 0
    height: int = 0


@dataclass()
class BoundingBox:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    def __contains__(self, other):
        contained = False
        if isinstance(other, Position):
            if self.x <= other.x < self.x2:
                if self.y <= other.y < self.y2:
                    contained = True
        return contained


@dataclass()
class Room:
    position: Position = Position()
    bounding_box: BoundingBox = BoundingBox()

    @property
    def center(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return Position(center_x, center_y)

    @property
    def width(self):
        return self.bounding_box.width

    @property
    def height(self):
        return self.bounding_box.height

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def x2(self):
        return self.bounding_box.x2

    @property
    def y2(self):
        return self.bounding_box.y2

    @property
    def grid(self):
        if not hasattr(self, '_grid'):
            self._grid = []
            for y in range(self.y, self.y2):
                row = []
                for x in range(self.x, self.x2):
                    row.append('.')
                self._grid.append(row)
        return self._grid

    def copy(self):
        return Room(position=self.position, bounding_box=self.bounding_box)

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



