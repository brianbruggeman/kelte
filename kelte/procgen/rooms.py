from dataclasses import dataclass, field

import numpy as np
import scipy.optimize as spo

from ..maths import Position
from ..tiles import get_tile


def in_hull(points, point):
    # Adapted from: https://stackoverflow.com/a/43564754/631199
    number_of_points = len(points)
    c = np.zeros(number_of_points)
    A = np.r_[points.T, np.ones((1, number_of_points))]
    b = np.r_[point, np.ones(1)]
    lp = spo.linprog(c, A_eq=A, b_eq=b)
    return lp.success


@dataclass()
class Room:
    width: int = 0
    height: int = 0
    doors: list = field(default_factory=list)
    position: Position = field(default_factory=Position)

    @property
    def lit(self):
        if not hasattr(self, '_lit'):
            self._lit = False
        return self._lit

    @lit.setter
    def lit(self, value):
        self._lit = value
        for position, tile in self:
            tile.lit = value

    @property
    def center(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return Position(center_x, center_y)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    @property
    def points(self):
        default_tile = get_tile("floor")
        if not hasattr(self, "_grid"):
            self._grid = []
            for y in range(self.y, self.y2):
                row = []
                for x in range(self.x, self.x2):
                    row.append(default_tile.copy())
                self._grid.append(row)
        return np.array(self._grid)

    def copy(self):
        return Room(width=self.width, height=self.height, position=self.position)

    def __contains__(self, other):
        contained = False
        try:
            x, y = other
            if self.x <= x <= self.x2 and self.y <= y <= self.y2:
                return True
        except ValueError:
            for point, tile in self:
                if point in other:
                    contained = True
                    break

        return contained

    def __iter__(self):
        for y, row in enumerate(self.points):
            for x, tile in enumerate(row):
                yield Position(x + self.x, y + self.y), tile

    def __getitem__(self, item):
        y, x = item
        return self.points[y][x]

    def __setitem__(self, item, value):
        y, x = item
        self.points[y][x] = value

    def __len__(self):
        return len(self.points)

    def __str__(self):
        data = []
        for y, row in enumerate(self.points):
            row = "".join(map(str, row))
            data.append(row)
        return "\n".join(data)
