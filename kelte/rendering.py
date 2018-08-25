import tcod as tdl

from kelte.engine.ecs import Entity
from kelte.engine.maths import Position
from kelte.engine.ui import Bar, Panel

from .colors import Color
from .config import settings
from .procgen.levels import Level
from .tiles import Tile


def render_bar(bar: Bar):
    position = bar.position


def render_entity(entity: Entity):
    position = entity.position
    tile = entity.tile
    render_tile(position, tile)


def render_level(level: Level):
    pass


def render_log(log: list = None):
    log = log or settings.main_log
    panel = settings.log_pane
    tdl.console_set_default_background(panel, tdl.black)
    tdl.console_clear(panel)
    tdl.console_set_default_foreground(panel, tdl.white)

    for row_id, msg in enumerate(log[-7:]):
        # msg = ''.join(chr(settings.typeface_mapper.get(c) or space) for c in msg)
        tdl.console_print(panel, 0, row_id, fmt=msg)

    tdl.console_blit(panel, 0, 0, settings.screen_width, settings.log_height, 0, 0, settings.screen_height - settings.log_height)


def render_level(level: Level, pane: Panel):
    pass


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
