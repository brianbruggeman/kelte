import tcod as tdl

from .config import settings
from .ecs import Entity, Event
from .math import Direction, Position
from .ui.event import KeyboardEvent, KeyboardModifiers, QuitEvent, get_events
from .utils import terminal


def initialize(debug=None, verbose=None):
    """Initializes game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    tdl.console_set_custom_font(settings.font_path)
    terminal.echo(f"Set font to: {settings.font_path}", verbose=verbose)

    settings.main_console = tdl.console_init_root(
        settings.width, settings.height, settings.title, settings.full_screen
    )

    # Create a player
    settings.player = Entity(name='player')
    position = Position(settings.width // 2, settings.height // 2)
    settings.player.add_component("position", position)
    settings.player.add_component("tile", "@")
    terminal.echo(f"Created player: {settings.player}", verbose=verbose)

    return settings


def convert_event(event):
    """Converts ui.event into ecs.event

    This maps keyboard entries into something that the system can handle

    TODO: Add a movement system
    """
    if isinstance(event, KeyboardEvent):
        # wasd_movement_mapper = {
        #     # Cardinal
        #     KeyboardEvent('a'): Direction.LEFT,
        #     KeyboardEvent('x'): Direction.DOWN,
        #     KeyboardEvent('w'): Direction.UP,
        #     KeyboardEvent('d'): Direction.RIGHT,
        #
        #     # Diagonals
        #     KeyboardEvent('q'): Direction.UP_LEFT,
        #     KeyboardEvent('e'): Direction.UP_RIGHT,
        #     KeyboardEvent('z'): Direction.DOWN_LEFT,
        #     KeyboardEvent('c'): Direction.DOWN_RIGHT,
        #     }

        vim_movement_mapper = {
            # Cardinal
            KeyboardEvent('h'): Direction.LEFT,
            KeyboardEvent('j'): Direction.DOWN,
            KeyboardEvent('k'): Direction.UP,
            KeyboardEvent('l'): Direction.RIGHT,

            # Diagonals
            KeyboardEvent('y'): Direction.UP_LEFT,
            KeyboardEvent('u'): Direction.UP_RIGHT,
            KeyboardEvent('b'): Direction.DOWN_LEFT,
            KeyboardEvent('n'): Direction.DOWN_RIGHT,
            }

        movement = vim_movement_mapper.get(event)  # or wasd_movement_mapper.get(event)
        if movement:
            event = Event('MOVE', settings.player, movement)
            return event

        if event == KeyboardEvent('escape'):
            exit(0)


def cycle():
    done = False

    for event in get_events(released=False, mouse_motion=False):

        if isinstance(event, QuitEvent):
            done = True
            break

        event = convert_event(event)
        if event and event.type == 'MOVE':
            entity = event.target
            tile = settings.player.tile.data
            old_pos = entity.position
            new_pos = old_pos + event.data

            tdl.console_set_default_foreground(settings.main_console, tdl.darker_sepia)
            tdl.console_put_char(settings.main_console, old_pos.x, old_pos.y, '.', tdl.BKGND_NONE)
            tdl.console_set_default_foreground(settings.main_console, tdl.yellow)
            tdl.console_put_char(settings.main_console, new_pos.x, new_pos.y, tile, tdl.BKGND_NONE)

    tdl.console_flush()
    return done


def main(debug=None, verbose=None):
    """Main game loop"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    # fill map
    tdl.console_set_default_foreground(settings.main_console, tdl.darker_sepia)
    for y in range(settings.height):
        for x in range(settings.width):
            tdl.console_put_char(settings.main_console, x, y, '.', tdl.BKGND_NONE)

    pos = settings.player.position
    tdl.console_set_default_foreground(settings.main_console, tdl.yellow)
    tdl.console_put_char(settings.main_console, pos.x, pos.y, '@', tdl.BKGND_NONE)
    while not tdl.console_is_window_closed():
        if cycle():
            break

    terminal.echo("Finished", verbose=verbose)


def run(debug=None, verbose=None):
    """Runs game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    if debug:
        print(settings)
    initialize(verbose=verbose, debug=debug)
    main(verbose=verbose, debug=debug)
