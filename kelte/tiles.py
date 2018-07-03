from dataclasses import dataclass

import colr

from .colors import Color, get_color


@dataclass()
class Tile:
    name: str = "empty"
    character: str = " "
    lit_color: Color = get_color("grey")
    unlit_color: Color = get_color("grey")
    lit: bool = False
    visible: bool = False
    walkable: bool = False
    destructable: bool = False
    flyable: bool = False
    opaque: bool = False
    explored: bool = False

    @property
    def color(self):
        if self.lit and self.visible:
            return self.lit_color
        else:
            return self.unlit_color

    @property
    def transparent(self):
        return not self.opaque

    @property
    def rendered(self):
        foreground = self.color.hex
        string = colr.color(self.c, fore=foreground)
        return string

    @property
    def c(self):
        if self.explored:
            return self.character
        else:
            return " "

    def copy(self):
        copy_of_self = Tile(
            name=self.name,
            character=self.character,
            lit_color=self.lit_color,
            unlit_color=self.unlit_color,
            lit=self.lit,
            visible=self.visible,
            walkable=self.walkable,
            destructable=self.destructable,
            flyable=self.flyable,
            opaque=self.opaque,
            explored=self.explored,
        )
        return copy_of_self

    def __str__(self):
        return self.c


def get_tile(name):
    return tiles.get(name, Tile()).copy()


tiles = {
    "empty": Tile(),
    "floor": Tile(
        "floor",
        ".",
        lit_color=get_color("sepia"),
        unlit_color=get_color("darker_sepia"),
        walkable=True,
    ),
    "wall": Tile(
        "wall",
        "#",
        lit_color=get_color("sepia"),
        unlit_color=get_color("darker_sepia"),
        opaque=True,
    ),
    "open-door": Tile(
        "open-door",
        "-",
        lit_color=get_color("lighter_sepia"),
        unlit_color=get_color("sepia"),
        walkable=True,
    ),
    "closed-door": Tile(
        "closed-door",
        "+",
        lit_color=get_color("lighter_sepia"),
        unlit_color=get_color("sepia"),
        opaque=True,
    ),
    "player": Tile(
        "player",
        "@",
        lit_color=get_color("yellow"),
        unlit_color=get_color("dark_yellow"),
        explored=True,
        opaque=True,
    ),
}


if __name__ == "__main__":
    for tile_name, tile in tiles.items():
        tile.lit = True
        print(f"{tile_name}: {tile.rendered}")
