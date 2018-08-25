import pytest


@pytest.mark.parametrize('data', [
    {  # no change
        'start': (0, 0),
        'end': (0, 0),
        'expected': [
            (0, 0)
            ]
        },
    {  # horizontal
        'start': (0, 0),
        'end': (1, 0),
        'expected': [
            (0, 0),
            (1, 0)
            ]
        },
    {  # vertical
        'start': (0, 0),
        'end': (0, 1),
        'expected': [
            (0, 0),
            (0, 1)
            ]
        },
    {  # top-right coordinate
        'start': (0, 0),
        'end': (1, 1),
        'expected': [
            (0, 0),
            (1, 1)
            ]
        },
    {  # top-left coordinate
        'start': (0, 0),
        'end': (-1, 1),
        'expected': [
            (0, 0),
            (-1, 1)
            ]
        },
    {  # bottom-left coordinate
        'start': (0, 0),
        'end': (-1, -1),
        'expected': [
            (0, 0),
            (-1, -1)
            ]
        },
    {  # bottom-right coordinate
        'start': (0, 0),
        'end': (1, -1),
        'expected': [
            (0, 0),
            (1, -1)
            ]
        },

    ])
def test_bresenham(data):
    from kelte.engine.maths import bresenham

    start = data.get('start')
    end = data.get('end')
    expected = data.get('expected')

    assert list(bresenham(start, end)) == expected
