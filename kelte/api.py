import random

import tcod as tdl

from .config import settings
from .ecs import Entity, Event
from .maths import Direction
from .procgen import LevelSize, create_dungeon
from .ui.event import KeyboardEvent, QuitEvent, get_events
from .utils import terminal
from .tiles import get_tile


def initialize(debug=None, verbose=None):
    """Initializes game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    tdl.console_set_custom_font(settings.font_path)
    terminal.echo(f"Set font to: {settings.font_path}", verbose=verbose)

    settings.main_console = tdl.console_init_root(
        settings.width, settings.height, settings.title, settings.full_screen
    )

    # Create a player
    player = Entity(name="player")
    player.add_component("tile", get_tile("player"))

    settings.entities = []
    settings.entities.append(player)
    settings.player = player
    terminal.echo(f"Created player: {player}", verbose=verbose)

    settings.game_map = tdl.map_new(settings.width, settings.height)
    settings.fov_map = tdl.map_new(settings.width, settings.height)
    return settings


def convert_event(event):
    """Converts ui.event into ecs.event

    This maps keyboard entries into something that the system can handle

    TODO: Add a movement system
    """
    if isinstance(event, KeyboardEvent):
        vim_movement_mapper = {
            # Cardinal
            KeyboardEvent("h"): Direction.LEFT,
            KeyboardEvent("j"): Direction.DOWN,
            KeyboardEvent("k"): Direction.UP,
            KeyboardEvent("l"): Direction.RIGHT,
            # Diagonals
            KeyboardEvent("y"): Direction.UP_LEFT,
            KeyboardEvent("u"): Direction.UP_RIGHT,
            KeyboardEvent("b"): Direction.DOWN_LEFT,
            KeyboardEvent("n"): Direction.DOWN_RIGHT,
        }

        movement = vim_movement_mapper.get(event)
        if movement:
            event = Event("MOVE", settings.player, movement)
            return event

        if event == KeyboardEvent("escape"):
            exit(0)


def render_all():
    pass


def cycle():
    done = False

    for event in get_events(released=False, mouse_motion=False):

        if isinstance(event, QuitEvent):
            done = True
            break

        event = convert_event(event)
        if event and event.type == "MOVE":
            entity = event.target

            new_pos = entity.position + event.data
            old_tile = settings.current_level[entity.position]

            if entity == settings.player:

                for neighbor in list(settings.player.position.neighbors) + [
                    settings.player.position
                ]:
                    tile = settings.current_level[neighbor]
                    if not tile.explored:
                        tile.explored = True
                        tdl.console_set_default_foreground(
                            settings.main_console, tile.color.tdl_color
                        )
                        tdl.console_put_char(
                            settings.main_console,
                            neighbor.x,
                            neighbor.y,
                            str(tile),
                            tdl.BKGND_NONE,
                        )

            if not settings.current_level[new_pos].walkable:
                continue

            tdl.console_set_default_foreground(
                settings.main_console, old_tile.color.tdl_color
            )
            tdl.console_put_char(
                settings.main_console,
                entity.position.x,
                entity.position.y,
                str(old_tile),
                tdl.BKGND_NONE,
            )

            tdl.console_set_default_foreground(
                settings.main_console, entity.tile.color.tdl_color
            )
            entity.position = new_pos
            tdl.console_put_char(
                settings.main_console,
                entity.position.x,
                entity.position.y,
                str(entity.tile),
                tdl.BKGND_NONE,
            )

            if entity == settings.player:

                tdl.map_compute_fov(
                    settings.fov_map,
                    new_pos.x,
                    new_pos.y,
                    0,
                    True,
                    tdl.FOV_PERMISSIVE_2,
                )

    tdl.console_flush()
    return done


def main(debug=None, verbose=None):
    """Main game loop"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    initialize(verbose=verbose, debug=debug)

    dungeon = create_dungeon(level_size=LevelSize(settings.width, settings.height))
    settings.dungeon = dungeon
    settings.current_level = dungeon[0]

    random_starting_room = random.choice(settings.current_level.rooms)
    settings.player.add_component("position", random_starting_room.center)

    neighbors = list(settings.player.position.neighbors) + [settings.player.position]
    for neighbor in neighbors:
        tile = settings.current_level[neighbor]
        if not tile.explored:
            tile.explored = True
            tdl.console_set_default_foreground(
                settings.main_console, tile.color.tdl_color
            )
            tdl.console_put_char(
                settings.main_console, neighbor.x, neighbor.y, str(tile), tdl.BKGND_NONE
            )

    for position, tile in settings.current_level:
        # initialize fov map
        tdl.map_set_properties(
            m=settings.fov_map,
            x=position.x,
            y=position.y,
            isTrans=tile.transparent,
            isWalk=tile.walkable,
        )
        # setup console
        tdl.console_set_default_foreground(settings.main_console, tile.color.tdl_color)
        tdl.console_put_char(
            settings.main_console, position.x, position.y, str(tile), tdl.BKGND_NONE
        )

    for entity in settings.entities:
        tile = entity.tile
        pos = entity.position

        tdl.console_set_default_foreground(settings.main_console, tile.color.tdl_color)
        tdl.console_put_char(
            settings.main_console, pos.x, pos.y, str(tile), tdl.BKGND_NONE
        )

    while not tdl.console_is_window_closed():
        if cycle():
            break

    terminal.echo("Finished", verbose=verbose)
