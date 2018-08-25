import random

import tcod as tdl

from .config import settings
from .engine import Event, KeyboardEvent, QuitEvent, get_ui_events, vector
from .initialization import initialize
from .lighting import handle_lighting
from .rendering import render_log, render_tile
from .tiles import get_tile
from .utils import terminal


def convert_event(ui_event, movement_mapper):
    """Converts ui.event into ecs.event

    This maps keyboard entries into something that the system can handle

    TODO: Add a movement system
    """
    if isinstance(ui_event, KeyboardEvent):
        movement = movement_mapper.get(ui_event)
        if movement:
            ecs_event = Event("MOVE", settings.player, movement)
            return ecs_event

        if ui_event == KeyboardEvent('return', 13, meta=True):
            tdl.console_set_fullscreen(not tdl.console_is_fullscreen())
            ecs_event = Event('FULLSCREEN', None, None)
            return ecs_event

        if ui_event == KeyboardEvent("escape") or isinstance(ui_event, QuitEvent):
            exit(0)


def cycle(movement_mapper):
    door_tiles = [get_tile(t) for t in ['closed door', 'hidden door']]

    events = [convert_event(e, movement_mapper) for e in get_ui_events(released=False, mouse_motion=False)]
    for event in events:
        if not event:
            continue

        if event and event.type == 'OPEN':
            position = event.data
            level_tile = settings.current_level[position]
            if level_tile.name == 'hidden door':
                new_tile = get_tile('closed door')
                new_tile.position = position
                new_tile.lit = level_tile.lit
                new_tile.visible = level_tile.visible
                settings.current_level[position] = new_tile
                render_tile(position=position, tile=new_tile)
            elif level_tile.name == 'closed door':
                new_tile = get_tile('open door')
                new_tile.position = position
                new_tile.lit = level_tile.lit
                new_tile.visible = level_tile.visible
                settings.current_level[position] = new_tile
                render_tile(position=position, tile=new_tile)

        elif event and event.type == 'ATTACK':
            target_entity = event.data
            aggressor_entity = event.target
            settings.main_log.append(f'{aggressor_entity.name} attacks {target_entity.name}')

        elif event and event.type == "MOVE":
            entity = event.target
            new_pos = entity.position + event.data

            another_entity = settings.entities.get(new_pos)
            if another_entity:
                if not another_entity.tile.walkable:
                    new_event = Event('ATTACK', entity, another_entity)
                    events.append(new_event)
                    continue

            level_tile = settings.current_level[new_pos]
            if not level_tile.walkable:
                if level_tile.name in [dt.name for dt in door_tiles]:
                    new_event = Event('OPEN', entity, new_pos)
                    events.append(new_event)
                else:
                    msg = random.choice(settings.expletives)
                    settings.main_log.append(msg)
                    terminal.echo(msg)
                continue

            if entity == settings.player:
                handle_lighting(settings.current_level)
                # handle_view(entity.position, new_pos, settings.current_level)

            old_tile = settings.current_level[entity.position]
            render_tile(entity.position, old_tile)
            render_tile(new_pos, entity.tile)
            entity.position = new_pos

    render_log(settings.main_log)
    tdl.console_flush()


def old_main(debug=None, verbose=None, seed=None):
    """Main game loop"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    initialize(verbose=verbose, debug=debug, seed=seed)

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

    while not tdl.console_is_window_closed():
        if cycle(vim_movement_mapper):
            break

    terminal.echo("Finished", verbose=verbose)

