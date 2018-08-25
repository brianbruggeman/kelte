import typing
from dataclasses import dataclass, field
from textwrap import wrap

import tcod as tdl

from kelte.engine.maths import Point

colors = {}


def _convert(value: typing.Union[int, float]) -> float:
    ...

@dataclass
class FloatByte:
    value: typing.Union[int, float] = field(default=0.0)
    name: str = "value"

    def __init__(self, value=None, name=None):
        self.value = _convert(value or 0.0)
        self.name = name or 'value'

    def __get__(self, instance, owner):
        value = instance.__dict__[self.name]
        self.value = value
        return value

    def __set__(self, instance, value):
        value = _convert(value if value is not None else self.value)
        instance.__dict__[self.name] = value
        self.value = value

    def __set_name__(self, owner, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, (float, int)):
            other = _convert(other)
        return self.value == other

    def __repr__(self):
        return f"{self.value}"


@dataclass
class Color(Point):
    r: typing.Union[float, int, FloatByte] = field(default=FloatByte(0.0))
    g: typing.Union[float, int, FloatByte] = field(default=FloatByte(0.0))
    b: typing.Union[float, int, FloatByte] = field(default=FloatByte(0.0))
    a: typing.Union[float, int, FloatByte] = field(default=FloatByte(1.0))

    def __init__(self, r=None, g=None, b=None, a=None):
        self.r = FloatByte(r or 0.0)
        self.g = FloatByte(g or 0.0)
        self.b = FloatByte(b or 0.0)
        self.a = FloatByte(a or 1.0)

    @property
    def red(self):
        return int(self.r * 255)

    @red.setter
    def red(self, value):
        assert 0 <= value <= 255
        self.r = value / 255

    @property
    def green(self):
        return int(self.g * 255)

    @green.setter
    def green(self, value):
        assert 0 <= value <= 255
        self.g = value / 255

    @property
    def blue(self):
        return int(self.b * 255)

    @blue.setter
    def blue(self, value):
        assert 0 <= value <= 255
        self.b = value / 255

    @property
    def alpha(self):
        return int(self.a * 255)

    @alpha.setter
    def alpha(self, value):
        assert 0 <= value <= 255
        self.a = value / 255

    @property
    def hex(self):
        red = f"{self.red:02x}"
        green = f"{self.green:02x}"
        blue = f"{self.blue:02x}"
        return f"{red}{green}{blue}"

    @hex.setter
    def hex(self, value):
        expected_length = 6
        if not isinstance(value, str):
            raise TypeError(f"Value, {value}, must be of type `str`")
        elif not len(value) == expected_length:
            raise ValueError(
                f"Value, {value}, must be {expected_length} characters long"
            )
        self.r, self.g, self.b = tuple(map(lambda x: int(x, 16) / 255, wrap(value, 2)))

    @property
    def hexa(self):
        alpha = f"{self.alpha:02x}"
        return f"{self.hex}{alpha}"

    @hexa.setter
    def hexa(self, value):
        expected_length = 8
        if not isinstance(value, str):
            raise TypeError(f"Value, {value}, must be of type `str`")
        elif not len(value) == expected_length:
            raise ValueError(
                f"Value, {value}, must be {expected_length} characters long"
            )
        self.r, self.g, self.b, self.a = tuple(
            map(lambda x: int(x, 16) / 255, wrap(value, 2))
        )

    @property
    def hsl(self):
        max_value = max(self.r, self.g, self.b)
        min_value = min(self.r, self.g, self.b)
        chroma = max_value - min_value
        luminosity = chroma / 2 + max_value
        hue = 0
        if chroma != 0:
            if max_value == self.r:
                segment = (self.g - self.b) / chroma
                shift = 0 // 60 if chroma >= 0 else 360 // 60
                hue = segment + shift
            elif max_value == self.g:
                segment = (self.b - self.r) / chroma
                shift = 120 // 60
                hue = segment + shift
            elif max_value == self.b:
                segment = (self.r - self.g) / chroma
                shift = 240 // 60
                hue = segment + shift
        saturation = 0 if chroma == 0 else chroma / (1 - abs(2 * luminosity - 1))
        return (hue, saturation, luminosity)

    @property
    def tdl_color(self) -> tdl.Color:
        tdl_color = tdl.Color(self.red, self.green, self.blue)
        return tdl_color

    @tdl_color.setter
    def tdl_color(self, value: tdl.Color):
        self.red = value.r
        self.green = value.g
        self.blue = value.b
        self.alpha = 255

    def shade(self, other):
        other = Color(*other)
        ar, ag, ab = -0.0, -0.0, -0.0
        dr, dg, db = abs(ar - self.r), abs(ag - self.g), abs(ab - self.b)
        r = self.r + dr * other.a
        g = self.g + dg * other.a
        b = self.b + dg * other.a
        new_color = Color(r, g, b, other.a)
        return new_color

    def tint(self, other, intensity=0.5):
        other = Color(*other)
        ar, ag, ab = 1.0, 1.0, 1.0
        dr, dg, db = abs(ar - other.r), abs(ag - other.g), abs(ab - other.b)

        r = self.r + dr * other.a * intensity
        g = self.g + dg * other.a * intensity
        b = self.b + dg * other.a * intensity
        new_tint = Color(r, g, b, other.a)
        return new_tint

    def __iter__(self):
        yield self.r
        yield self.b
        yield self.g
        yield self.a

    def __getitem__(self, key):
        key_mapping = {
            "r": self.r,
            "red": self.red,
            0: self.r,
            "g": self.g,
            "green": self.green,
            1: self.g,
            "b": self.b,
            "blue": self.blue,
            2: self.b,
            "a": self.a,
            "alpha": self.alpha,
            3: self.a,
        }
        if key in key_mapping:
            value = key_mapping.get(key)
            return value
        else:
            raise KeyError(f"Could not find {key} in {self}")

    def __eq__(self, other):
        for index, value in enumerate(other):
            if index == 0:
                if self.r != _convert(value):
                    return False
            if index == 1:
                if self.g != _convert(value):
                    return False
            if index == 2:
                if self.b != _convert(value):
                    return False
            if index == 3:
                if self.a != _convert(value):
                    return False
        return True

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))

    def __lt__(self, other):
        other = tuple(other) if not isinstance(other, (tuple, list)) else other
        return tuple(self) < tuple(other)

    def __repr__(self):
        return f"{type(self).__name__}(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __str__(self):
        return self.hex


def get_color(name):
    global colors

    name = name.lower()
    color = colors[name]
    return color


def populate_colors():
    global colors

    for color_name in dir(tdl):
        tdl_color_value = getattr(tdl, color_name)
        if isinstance(tdl_color_value, tdl.Color):
            new_color = Color()
            new_color.tdl_color = tdl_color_value
            color_name = color_name.lower()
            colors[color_name] = new_color

    colors['brown'] = Color(139, 69, 19)
    colors['light_brown'] = Color(160, 82, 45)
    colors['lighter_brown'] = Color(205, 133, 63)
    colors['lightest_brown'] = Color(222, 184, 135)
    colors['none'] = Color(0, 0, 0, 0)

    for color_name, color in colors.items():
        globals()[color_name] = color


def _convert(value: typing.Union[int, float, FloatByte]) -> float:
    if value is None:
        value = 0.0
    elif isinstance(value, int):
        value = value / 255
    elif isinstance(value, str) and len(value) == 2:
        value = int(value, 16) / 255
    elif isinstance(value, FloatByte):
        value = value.value
    if not isinstance(value, float):
        raise TypeError(f"Value, {value}, must be of type `float` not `{type(value)}`")
    if value > 1.0:
        value = 1.0
    if value < 0.0:
        value = 0.0
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"Value, {value}, must be between `0.0` and `1.0`")
    return value


populate_colors()


if __name__ == "__main__":
    import colr
    import subprocess

    height, width = list(
        map(
            int,
            subprocess.run("stty size", shell=True, stdout=subprocess.PIPE)
            .stdout.decode("utf-8")
            .strip()
            .split(),
        )
    )

    line = ""
    for color_name, color in colors.items():
        string = colr.color(color_name, fore=color.hex)
        if len(line) > width:
            print(line)
            line = ""
        if not line:
            line = string
        else:
            line += f", {string}"
