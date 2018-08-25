import pytest


@pytest.mark.parametrize(
    "data",
    [
        {
            "kwds": {"x": 1, "y": 2},
            "expected": {
                "x": 1,
                "y": 2,
                "neighbors": (
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (1, 1),
                    (1, 2),
                    (1, 3),
                    (2, 1),
                    (2, 2),
                    (2, 3),
                ),
            },
        }
    ],
)
def test_position(data):
    from kelte.engine.maths import Position

    args = data.get("args", tuple())
    kwds = data.get("kwds", dict())

    expected = data.get("expected")

    p = Position(*args, **kwds)
    assert len(p) == 2
    for key, value in expected.items():
        assert hasattr(p, key)
        data = getattr(p, key)
        try:
            assert data == value
        except ValueError:
            data = tuple(map(tuple, data))
            assert data == value


@pytest.mark.parametrize(
    "point01, point02, distance", [((0, 1), (0, 0), 1), ((3, 0), (0, 4), 5)]
)
def test_position_distance(point01, point02, distance):
    from kelte.engine.maths import Position

    p = Position(*point01)

    assert p.distance(point02) == distance
    assert p.distance(Position(*point02)) == distance
