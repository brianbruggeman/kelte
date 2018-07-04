from dataclasses import dataclass

from ..tiles import Tile


class Mob:
    name: str = "undefined"
    tile: Tile = None
