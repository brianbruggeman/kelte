import numpy as np
import scipy.spatial.distance as spsd


def euclidean_distance(*points, strict=None):
    """Calculates the euclidean distance between tuples

    Args:
        points: set of points to calculate distances
        strict: only calculates based on

    Returns:
        float: distance value
    """
    points = np.array(points)
    return spsd.euclidean(*points)
