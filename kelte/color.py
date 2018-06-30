import typing


class Color(typing.NamedTuple):
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0

    def __get__(self):
        return (self.r, self.g, self.b, self.a)

    @property
    def red(self):
        return int(self.r * 255)

    @property
    def green(self):
        return int(self.g * 255)

    @property
    def blue(self):
        return int(self.b * 255)

    @property
    def alpha(self):
        return int(self.a * 255)

    @property
    def hex(self):
        red = f"{self.red:02x}"
        green = f"{self.green:02x}"
        blue = f"{self.blue:02x}"
        return f"{red}{green}{blue}"

    @property
    def hexa(self):
        alpha = f"{self.alpha:02x}"
        return f"{self.hex}{alpha}"

    def __str__(self):
        return self.hex


def get_color(name):
    return colors.get(name, Color())


colors = {
    "black": Color(),
    "white": Color(1, 1, 1, 1),
    "blue": Color(b=1.0),
    "red": Color(r=1.0),
    "green": Color(g=1.0),
    "yellow": Color(r=1.0, g=1.0),
    "orange": Color(r=1.0, g=0.647),
    "fuchsia": Color(r=1.0, b=1.0),
    "teal": Color(g=1.0, b=1.0),
    "grey": Color(r=0.5, g=0.5, b=0.5),
    "maroon": Color(r=0.5),
    "brown": Color(r=0.647, g=0.1647, b=0.1647),
    "purple": Color(r=0.5, b=0.5),
    "silver": Color(r=192 / 255, g=192 / 255, b=192 / 255),
}
