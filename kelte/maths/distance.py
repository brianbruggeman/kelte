import numpy as np
import scipy.spatial.distance as spsd


def euclidean_distance(point01, point02, strict=None):
    """Calculates the euclidean distance between tuples

    Args:
        points: set of points to calculate distances
        strict: only calculates based on

    Returns:
        float: distance value
    """
    point01 = np.array(point01)
    point02 = np.array(point02)
    value = spsd.euclidean(point01, point02)
    return value
