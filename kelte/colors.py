from dataclasses import dataclass

import tcod as tdl


@dataclass
class Color:
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0

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

    @property
    def hexa(self):
        alpha = f"{self.alpha:02x}"
        return f"{self.hex}{alpha}"

    @property
    def tdl_color(self) -> tdl.Color:
        return tdl.Color(self.red, self.green, self.blue)

    @tdl_color.setter
    def tdl_color(self, value: tdl.Color):
        self.red = value.r
        self.green = value.g
        self.blue = value.b

    def __str__(self):
        return self.hex


def get_color(name):
    return colors.get(name, Color())


colors = {}
for color_name in dir(tdl):
    tdl_color_value = getattr(tdl, color_name)
    if isinstance(tdl_color_value, tdl.Color):
        new_color = Color()
        new_color.tdl_color = tdl_color_value
        colors[color_name] = new_color


for color_name, color in colors.items():
    globals()[color_name] = color


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
