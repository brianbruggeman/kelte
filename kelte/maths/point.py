from dataclasses import dataclass

import numpy as np

from .bresenham import bresenham
from .distance import euclidean_distance
from .grids import create_grid

# Position Requirements
#   Provide a simple data store for a point on a points
#   Provide a distance function
#   Provide a mechanism to add and subtract tuple data (for Direction Enum)

neighbor_grid = create_grid((-1, -1), (1, 1))


class Point:

    @property
    def array(self):
        return np.array(tuple(self))

    def distance(self, other, func=None) -> float:
        if not isinstance(other, tuple):
            other = tuple(other)
        if not func:
            func = euclidean_distance
        my_data = tuple(self)
        value = func(my_data, other)
        return value


    def ray(self, other, maxx=None, maxy=None, minx=None, miny=None):
        Class = self.__class__
        for point in bresenham(tuple(self), tuple(other)):
            point = Class(*point)
            if maxx and point[0] > maxx:
                continue
            elif maxy and point[1] > maxy:
                continue
            elif minx and point[0] < minx:
                continue
            elif miny and point[1] < miny:
                continue
            yield point

    def __add__(self, other):
        cls = self.__class__
        other = tuple(other) if not isinstance(other, tuple) else other
        return cls(*tuple(np.add(other, tuple(self))))

    def __bool__(self):
        return True if any(iter(self)) else False

    def __eq__(self, other):
        other = tuple(other) if not isinstance(other, tuple) else other
        return tuple(self) == other

    def __get__(self, instance, owner):
        value = instance.__dict__[self.name]
        return value

    def __hash__(self):
        return hash(tuple(iter(self)))

    def __iter__(self):
        for key in self.__annotations__.keys():
            val = getattr(self, key)
            if not isinstance(val, str):
                try:
                    yield from val
                except TypeError:
                    yield val
            else:
                yield val

    def __len__(self):
        return len(tuple(self.__annotations__.keys()))

    def __lt__(self, other):
        other = tuple(other) if not isinstance(other, tuple) else other
        return tuple(self) < other

    def __mul__(self, other):
        cls = self.__class__
        other = tuple(other) if not isinstance(other, tuple) else other
        answer = np.multiply(tuple(self), other)
        return cls(*tuple(answer))

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

    def __str__(self):
        return str(tuple(self))

    def __sub__(self, other):
        cls = self.__class__
        other = tuple(other) if not isinstance(other, tuple) else other
        return cls(*tuple(np.subtract(tuple(self), other)))


@dataclass
class Position(Point):
    x: int = 0
    y: int = 0

    def __hash__(self):
        return hash((self.x, self.y))

    def __getitem__(self, item):
        data = tuple(self)
        if isinstance(item, int):
            return data[item]
        elif isinstance(item, str):
            return self.__dict__[item]

    def __iter__(self):
        yield self.x
        yield self.y

    def __set__(self, instance, value):
        super().__set__(instance, value)
        self.x, self.y = value

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        owner.neighbors = self.neighbors
        owner.distance = self.distance

    @property
    def neighbors(self):
        grid = np.add((self.x, self.y), neighbor_grid)
        return grid
