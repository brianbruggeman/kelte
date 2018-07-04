import random
import json

import numpy as np
import tcod as tdl

from .config import settings
from .utils import terminal
from .ecs import Entity
from .colors import get_color
from .procgen import create_dungeon, LevelSize
from .tiles import get_tile
from .rendering import render_tile
from .lighting import handle_lighting
from .fov import handle_view


def initialize(debug=None, verbose=None, seed=None):
    """Initializes game"""
    verbose = True if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    if seed:
        settings.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    typeface_path = settings.package_path / 'assets' / f'{settings.typeface_name}.{settings.typeface_tablename}.{settings.typeface_size}.png'
    typeface_map_path = settings.package_path / 'assets' / f'{settings.typeface_name}.{settings.typeface_tablename}.map'
    with typeface_map_path.open() as stream:
        typeface_map = json.loads(stream.read())
    typeface_shape = len(typeface_map), len(typeface_map[0])
    settings.typeface_mapper = {chr(value): index for index, value in enumerate(np.array(typeface_map).flatten())}

    tdl.console_set_custom_font(str(typeface_path), flags=settings.typeface_flags, nb_char_vertic=typeface_shape[0], nb_char_horiz=typeface_shape[-1])
    terminal.echo(f"Set font to: {typeface_path}", verbose=verbose)

    settings.main_console = tdl.console_init_root(
        settings.width, settings.height, settings.title,
        settings.full_screen, settings.renderer
    )

    tdl.console_set_default_background(settings.main_console, get_color('black').tdl_color)

    # Create a player
    player = Entity(type="physical", name="player")
    player.add_component("tile", get_tile("player"))
    player.tile.lit_color = get_color('yellow')
    player.tile.unlit_color = get_color('dark_yellow')

    settings.entities = []
    settings.entities.append(player)
    settings.player = player
    terminal.echo(f"Created player: {player}", verbose=verbose)

    dungeon = create_dungeon(level_size=LevelSize(settings.width, settings.height))
    settings.dungeon = dungeon
    settings.current_level = dungeon[0]

    random_starting_room = random.choice(settings.current_level.rooms)
    settings.player.add_component("position", random_starting_room.center)

    for position, tile in settings.current_level:
        # setup console
        render_tile(position, tile)

    for entity in settings.entities:
        if entity == settings.player:
            handle_lighting(entity.position, entity.position, settings.current_level)
            handle_view(entity.position, entity.position, settings.current_level)
        render_tile(entity.position, entity.tile)

    return settings

