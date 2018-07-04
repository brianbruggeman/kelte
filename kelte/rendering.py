import tcod as tdl

from .config import settings
from .maths import Position
from .tiles import Tile
from .colors import Color


def render_tile(position: Position, tile: Tile, foreground_color: Color = None, background_color: Color = None, background_mode: int = None):
    foreground_color = foreground_color or tile.color
    background_color = background_color or tile.background_color
    background_mode = background_mode or tile.background_mode

    # capture tile "picture"
    character = settings.typeface_mapper.get(tile.c)

    # setup colors
    tdl.console_set_default_foreground(settings.main_console, foreground_color.tdl_color)
    tdl.console_set_default_background(settings.main_console, background_color.tdl_color)

    # write to buffer
    tdl.console_put_char(
        con=settings.main_console,
        x=position.x,
        y=position.y,
        c=character,
        flag=background_mode)
