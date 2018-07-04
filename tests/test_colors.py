import pytest


@pytest.mark.parametrize(
    "data",
    [
        {  # default
            "kwds": {},
            "expected": {
                "red": 0,
                "green": 0,
                "blue": 0,
                "alpha": 255,
                "hex": "00" * 3,
                "hexa": "00" * 3 + "ff",
            },
        },
        {  # black
            "attrs": {"hexa": "000000ff"},
            "expected": {
                "red": 0,
                "green": 0,
                "blue": 0,
                "alpha": 255,
                "hex": "00" * 3,
                "hexa": "00" * 3 + "ff",
            },
        },
        {  # white
            "kwds": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0},
            "expected": {
                "red": 255,
                "green": 255,
                "blue": 255,
                "alpha": 255,
                "hex": "ff" * 3,
                "hexa": "ff" * 4,
            },
        },
    ],
)
def test_color_data_class(data):
    from kelte.colors import Color

    kwds = data.get("kwds")
    attrs = data.get("attrs")
    expected = data["expected"]

    if kwds:
        c = Color(**kwds)
    else:
        c = Color()
    if attrs:
        for attr_name, attr_value in attrs.items():
            try:
                setattr(c, attr_name, attr_value)
            except AttributeError:
                c.__dict__[attr_name].__setattr__("value", attr_value)
    for key, value in expected.items():
        assert getattr(c, key) == value

    assert c == tuple(c)


@pytest.mark.parametrize(
    "data",
    [
        {  # default
            "name": "red",
            "args": (255, 0, "00", 1.0),
            "named_tdl_color": "red",
            "named_args": (255, 0, 0, 255),
        }
    ],
)
def test_tdl_color_integration(data):
    import tcod as tdl
    from kelte.colors import Color

    # Get
    name = data["name"]
    args = data["args"]

    tdl_color = getattr(tdl, name)

    c = Color(*args)
    assert tdl_color == c.tdl_color

    # Set
    named_tdl_color = data["named_tdl_color"]
    named_args = data["named_args"]

    named_tdl_color = getattr(tdl, named_tdl_color)
    c.tdl_color = named_tdl_color
    assert c == Color(*named_args)
    assert c == named_tdl_color


@pytest.mark.parametrize(
    "data",
    [
        {"args": [None], "raises": TypeError, "expected": None},  # None
        {"kwds": {"value": 1.0}, "raises": None, "expected": 1.0},  # float
        {"kwds": {"value": 255}, "raises": None, "expected": 1.0},  # integer
        {"args": ["ff"], "raises": None, "expected": 1.0},  # string
        {  # out of range integer
            "kwds": {"value": 256},
            "raises": ValueError,
            "expected": None,
        },
        {  # out of range float
            "kwds": {"value": 1.1},
            "raises": ValueError,
            "expected": None,
        },
    ],
)
def test_convert(data):
    from kelte.colors import _convert

    args = data.get("args", [])
    kwds = data.get("kwds", {})
    raises = data.get("raises")
    expected = data.get("expected")

    def run(*args, **kwds):
        if args and kwds:
            result = _convert(*args, **kwds)
        elif args:
            result = _convert(*args)
        elif kwds:
            result = _convert(**kwds)
        else:
            raise RuntimeError("No data")

        assert result == expected

    if not raises:
        run(*args, **kwds)
    else:
        with pytest.raises(raises):
            run(*args, **kwds)


def test_get_color():
    import tcod as tdl
    from kelte.colors import get_color

    tdl_colors = {
        d: getattr(tdl, d) for d in dir(tdl) if isinstance(getattr(tdl, d), tdl.Color)
    }
    for tdl_color_name, tdl_color in tdl_colors.items():
        kelte_color = get_color(tdl_color_name)
        assert kelte_color == tdl_color


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
