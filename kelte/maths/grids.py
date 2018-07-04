import numpy as np


def create_grid(start, end, offset=None):
    (x1, y1), (x2, y2) = start, end
    grid = np.mgrid[x1:x2 + 1:1, y1:y2 + 1:1].reshape(2, -1).T
    if offset is not None:
        grid = np.add(offset, grid)
    return tuple(sorted(map(tuple, grid)))
