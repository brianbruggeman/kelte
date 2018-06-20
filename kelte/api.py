import tcod as tdl

from .config import settings
from .ecs import Entity
from .utils import terminal

from .math import Position


def initialize(debug=None, verbose=None):
    """Initializes game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    tdl.console_set_custom_font(settings.font_path)
    terminal.echo(f'Set font to: {settings.font_path}', verbose=verbose)

    settings.main_console = tdl.console_init_root(settings.width, settings.height, settings.title, settings.full_screen)

    # Create a player
    settings.player = Entity()
    position = Position(settings.width // 2, settings.height // 2)
    settings.player.add_component('position', position)
    settings.player.add_component('tile', '@')
    terminal.echo(f'Created player: {settings.player}', verbose=verbose)

    return settings


def main(debug=None, verbose=None):
    """Main game loop"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    key = tdl.Key()
    mouse = tdl.Mouse()

    while not tdl.console_is_window_closed():
        tdl.sys_check_for_event(tdl.EVENT_KEY_PRESS, key, mouse)

        if key.vk == tdl.KEY_ESCAPE:
            return True

        tdl.console_set_default_foreground(settings.main_console, tdl.white)

        pos = settings.player.position
        tile = settings.player.tile.data
        tdl.console_put_char(settings.main_console, pos.x, pos.y, tile, tdl.BKGND_NONE)
        tdl.console_flush()

    terminal.echo('Finished', verbose=verbose)


def run(debug=None, verbose=None):
    """Runs game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    initialize(verbose=verbose, debug=debug)
    main(verbose=verbose, debug=debug)
