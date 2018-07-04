import pytest


@pytest.mark.parametrize(
    "data",
    [
        {
            "a": (0, 0),
            "b": (3, 3),
            "expected": tuple((x, y) for x in range(4) for y in range(4)),
        },
        {
            "a": (0, 0),
            "b": (3, 3),
            "offset": (1, 1),
            "expected": tuple((x + 1, y + 1) for x in range(4) for y in range(4)),
        },
    ],
)
def test_create_grid(data):
    from kelte.maths.grids import create_grid

    a = data.get("a")
    b = data.get("b")
    offset = data.get("offset", None)
    expected = data.get("expected")

    assert expected == create_grid(a, b, offset)
