import typing

import munch
import pytest


class Point(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0
    w: int = 0


@pytest.mark.parametrize(
    "data",
    [
        {  # 4d
            "points": [Point(0, 1, 2, 3), Point(4, 5, 6, 7)],
            "strict": False,
            "expected": 8.0,
        },
        {  # 3d
            "points": [Point(3, 0, 0), Point(0, 4, 0)],
            "strict": False,
            "expected": 5.0,
        },
        {"points": [Point(0, 3), Point(0, 4)], "strict": False, "expected": 1.0},  # 2d
        {"points": [Point(0), Point(2)], "strict": False, "expected": 2.0},  # 1d
        {  # Origin
            "points": [Point(), Point(0, 1, 0)],
            "strict": False,
            "expected": 1.0,
        },
    ],
)
def test_euclidean_distance(data):
    from kelte.maths.distance import euclidean_distance

    data = munch.Munch(data)

    assert euclidean_distance(*data.points, strict=data.strict) == data.expected
