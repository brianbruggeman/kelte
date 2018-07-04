from dataclasses import dataclass, field

import colr
import tcod as tdl

from ..colors import Color, get_color


class Registry(type):
    def __new__(cls, class_name, bases, namespace):
        namespace["registry"] = {}
        new_cls = type(class_name, bases, namespace)
        return new_cls


@dataclass()
class Tile(metaclass=Registry):
    name: str = "empty"
    character: str = " "
    lit: bool = False
    visible: bool = False
    walkable: bool = False
    destructable: bool = False
    flyable: bool = False
    opaque: bool = False
    explored: bool = False
    lit_color: Color = field(default=get_color("grey"))
    unlit_color: Color = field(default=get_color("darker_grey"))
    background_lit_color: Color = field(default=get_color("black"))
    background_unlit_color: Color = field(default=get_color("black"))
    background_mode: int = tdl.BKGND_NONE

    @property
    def background_color(self):
        if self.lit and self.visible:
            return self.background_lit_color
        else:
            return self.background_unlit_color

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
        background = self.background_color.hex
        string = colr.color(self.c, fore=foreground, back=background)
        return string

    @property
    def c(self):
        if self.explored or self.visible:
            return self.character
        else:
            return " "

    def copy(self):
        copy_of_self = Tile(
            name=self.name,
            character=self.character,
            lit=self.lit,
            visible=self.visible,
            walkable=self.walkable,
            destructable=self.destructable,
            flyable=self.flyable,
            opaque=self.opaque,
            explored=self.explored,
        )
        copy_of_self.lit_color = self.lit_color
        copy_of_self.unlit_color = self.unlit_color
        return copy_of_self

    def __new__(cls, *args, **kwds):
        name = kwds.get("name")
        parent = super()
        if not isinstance(parent, Tile):
            instance = super().__new__(cls)
        else:
            instance = super().__new__(cls, *args, **kwds)
        cls.registry.setdefault(name, instance)
        return instance

    def __str__(self):
        return self.c


def get_tile(name):
    return Tile.registry.get(name, Tile()).copy()
