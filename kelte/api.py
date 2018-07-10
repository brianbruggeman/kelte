import tcod as tdl

from .config import settings
from .ecs import Event
from .maths import vector
from .ui.event import KeyboardEvent, QuitEvent, get_events
from .utils import terminal
from .fov import handle_view
from .lighting import handle_lighting
from .rendering import render_tile, render_entity
from .initialization import initialize


def convert_event(ui_event):
    """Converts ui.event into ecs.event

    This maps keyboard entries into something that the system can handle

    TODO: Add a movement system
    """
    if isinstance(ui_event, KeyboardEvent):
        vim_movement_mapper = {
            # Cardinal
            KeyboardEvent("h"): vector.LEFT,
            KeyboardEvent("j"): vector.DOWN,
            KeyboardEvent("k"): vector.UP,
            KeyboardEvent("l"): vector.RIGHT,
            # Diagonals
            KeyboardEvent("y"): vector.UP_LEFT,
            KeyboardEvent("u"): vector.UP_RIGHT,
            KeyboardEvent("b"): vector.DOWN_LEFT,
            KeyboardEvent("n"): vector.DOWN_RIGHT,
            # No movement
            KeyboardEvent("."): vector.NONE,
        }

        movement = vim_movement_mapper.get(ui_event)
        if movement:
            ecs_event = Event("MOVE", settings.player, movement)
            return ecs_event

        if ui_event == KeyboardEvent('return', 13, meta=True):
            tdl.console_set_fullscreen(not tdl.console_is_fullscreen())
            return None

        if ui_event == KeyboardEvent("escape"):
            exit(0)


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

            if not settings.current_level[new_pos].walkable:
                continue

            if entity == settings.player:
                handle_lighting(entity.position, new_pos, settings.current_level)
                handle_view(entity.position, new_pos, settings.current_level)

            render_tile(entity.position, old_tile)
            render_tile(new_pos, entity.tile)
            entity.position = new_pos

    for entity in settings.entities:
        render_entity(entity)

    tdl.console_flush()
    return done


def main(debug=None, verbose=None, seed=None):
    """Main game loop"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    initialize(verbose=verbose, debug=debug, seed=seed)

    while not tdl.console_is_window_closed():
        if cycle():
            break

    terminal.echo("Finished", verbose=verbose)
