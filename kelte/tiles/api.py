from dataclasses import dataclass

import colr

from ..colors import Color, get_color


class Registry(type):
    def __new__(cls, class_name, bases, namespace):
        namespace["registry"] = {}
        return type(class_name, bases, namespace)


class Colored:
    @property
    def lit_color(self):
        if not hasattr(self, "_lit_color"):
            color = get_color("grey")
            setattr(self, "_lit_color", color)
        return getattr(self, "_lit_color")

    @lit_color.setter
    def lit_color(self, value):
        if isinstance(value, str):
            color = get_color(value)
            setattr(self, "_lit_color", color)
        elif isinstance(value, Color):
            setattr(self, "_lit_color", value)


@dataclass()
class Tile(Colored, metaclass=Registry):
    name: str = "empty"
    character: str = " "
    lit = False
    visible = False
    walkable = False
    destructable = False
    flyable: bool = False
    opaque: bool = False
    explored: bool = False
    lit_color: Color = get_color("grey")
    unlit_color: Color = get_color("dark_grey")

    @property
    def color(self):
        if self.lit:
            return self.lit_color
        else:
            return self.unlit_color

    @property
    def transparent(self):
        return not self.opaque

    @property
    def rendered(self):
        foreground = self.color.hex
        string = colr.color(self.character, fore=foreground)
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

    def __new__(cls, name: str = "empty", *args, **kwds):
        parent = super()
        if not isinstance(parent, Tile):
            instance = parent.__new__(cls)
        else:
            instance = parent.__new__(cls, name, *args, **kwds)
        cls.registry.setdefault(name, instance)
        return instance

    def __str__(self):
        return self.c


def get_tile(name):
    return Tile.registry.get(name, Tile()).copy()


#
# tiles = Tile.registry
# {
#     "player": Tile(
#         "player",
#         "@",
#         lit_color=get_color("yellow"),
#         unlit_color=get_color("dark_yellow"),
#         explored=True,
#         opaque=True,
#     ),
#     "empty": Tile(),
#     "floor": Tile(
#         "floor",
#         ".",
#         lit_color=get_color("sepia"),
#         unlit_color=get_color("darker_sepia"),
#         walkable=True,
#     ),
#     "wall": Tile(
#         "wall",
#         "#",
#         lit_color=get_color("sepia"),
#         unlit_color=get_color("darker_sepia"),
#         opaque=True,
#     ),
#     "open-door": Tile(
#         "open-door",
#         "-",
#         lit_color=get_color("lighter_sepia"),
#         unlit_color=get_color("sepia"),
#         walkable=True,
#     ),
#     "closed-door": Tile(
#         "closed-door",
#         "+",
#         lit_color=get_color("lighter_sepia"),
#         unlit_color=get_color("sepia"),
#         opaque=True,
#     ),
#     # traditional mob tiles
#     "ant": MobTile("ant", "a"),
#     "bat": MobTile("bat", "b"),
#     "bog monster": MobTile("bog monster", "b"),
#     "gelatinous cube": MobTile("gelatinous cube", "c"),
#     "goblin": MobTile("goblin", "g"),
#     "imp": MobTile("imp", "i"),
#     "jackel": MobTile("jackel", "j"),
#     "hobgoblin": MobTile("hobgoblin", "H"),
#     "kobold": MobTile("kobold", "k"),
#     "orc": MobTile("orc", "o"),
#     "rats": MobTile('rats', 's'),
#     "skeleton": MobTile('skeleton', 's'),
#     "slime": MobTile('slime', 's'),
#     "snake": MobTile('snake', 's'),
#     "spider": MobTile('spider', 's'),
#     "troll": MobTile('troll', 't'),
#     "wolf": MobTile("wolf", "w"),
#     "worm": MobTile('worm', 'w'),
#     # celtic mythological creatures
#     "banshee": MobTile('banshee', 'b'),
#     'badb': MobTile('badb', 'B'),
#     'bean nighe': MobTile('bean nighe', 'b'),
#     "changeling": MobTile('changeling', 'c'),
#     "Morrigan": MobTile('morrigan', 'M'),
#     "macha": MobTile('macha', 'M'),
#     "selkie": MobTile('selkie', 's'),
#
# }
