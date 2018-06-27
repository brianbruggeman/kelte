from dataclasses import dataclass

import colr
from .color import Color, get_color


@dataclass()
class Tile:
    name: str = 'empty'
    character: str = ' '
    color: Color = get_color('grey')
    visible: bool = False
    walkable: bool = False
    destructable: bool = False
    flyable: bool = False
    opaque: bool = False

    @property
    def rendered(self):
        string = colr.color(self.character, fore=self.color.hex)
        return string

    def __str__(self):
        return self.character


def get_tile(name):
    return tiles.get(name, Tile())


tiles = {
    'empty': Tile(),
    'floor': Tile('floor', '.'),
    'wall': Tile('wall', '#', color=get_color('blue')),
    'open-door': Tile('open-door', '-', color=get_color('brown')),
    'closed-door': Tile('closed-door', '+', color=get_color('brown')),
    }
