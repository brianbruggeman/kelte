from dataclasses import dataclass, field

import colr
import tcod as tdl

from ..colors import Color, get_color


def populate_tile_data(file_data):
    for data_type, file_items in file_data.items():
        if not file_items:
            continue
        for item in file_items:
            item['type'] = data_type

            # ----------------------------------------------------------
            # colors
            # ----------------------------------------------------------
            lit_color = item.get("lit_color")
            if isinstance(lit_color, str):
                item["lit_color"] = get_color(lit_color)
            unlit_color = item.get("unlit_color")
            if isinstance(unlit_color, str):
                item["unlit_color"] = get_color(unlit_color)

            # ----------------------------------------------------------
            code = item.pop("code", None)
            if code:
                character = chr(code)
                item["character"] = character
            if not item.get("character"):
                name = item.get('name')
                item["character"] = name[0]

            item = {k: v for k, v in item.items() if k in Tile.__annotations__}
            Tile(**item)

    return Tile.registry


class Registry(type):

    def __new__(meta, class_name, bases, namespace):
        namespace["registry"] = {}
        new_cls = type(class_name, bases, namespace)
        return new_cls


@dataclass
class Tile(metaclass=Registry):
    name: str = "undefined"
    character: str = "?"
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
    type: str = ''

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
        string = colr.color(self.character, fore=foreground, back=background)
        return string

    @property
    def c(self):
        if self.explored or self.visible:
            return self.character
        else:
            return " "

    def copy(self):
        data = {k: getattr(self, k) for k in self.__annotations__}
        copy_of_self = Tile(**data)
        return copy_of_self

    def __hash__(self):
        hashed = hash((k, getattr(self, k)) for k in self.__annotations__)
        return hashed

    def __new__(cls, *args, **kwds):
        name = kwds.get("name")
        parent = super()
        if not isinstance(parent, Tile):
            instance = super().__new__(cls)
        else:
            instance = super().__new__(cls, *args, **kwds)
        Tile.registry.setdefault(name, instance)
        new_id = len(Tile.registry.keys())
        instance.id = new_id
        return instance

    def __str__(self):
        return self.character


def get_tile(name: str, copy: bool = True, **kwds) -> Tile:
    if name not in Tile.registry:
        Tile(name=name, **kwds)
    tile = Tile.registry[name]
    return tile.copy() if copy is True else tile
