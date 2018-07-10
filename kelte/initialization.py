import json
import random
import typing
from pathlib import Path

import numpy as np
import tcod as tdl
import yaml

from .colors import get_color
from .config import settings
from .ecs import Entity
from .fov import handle_view
from .lighting import handle_lighting
from .procgen import create_dungeon
from kelte.items import populate_item_data
from kelte.mobs import populate_mob_data
from .rendering import render_entity, render_tile
from .tiles import get_tile, populate_tile_data
from .utils import terminal


def find_data(path: typing.Union[str, Path] = None):
    data_path = path or settings.data_path
    data = {}
    for data_file in data_path.glob('**/*.yml'):
        rel_data_file = data_file.relative_to(data_path)
        file_items = yaml.load(data_file.read_text(encoding='utf-8'))
        data_type = '.'.join([s.split('.')[0] for s in rel_data_file.parts])
        data[data_type] = file_items
    return data


def initialize(debug=None, verbose=None, seed=None):
    """Initializes game"""
    verbose = 1 if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    tdl.sys_set_fps(20)
    initialize_random_seed(seed=seed, debug=debug, verbose=verbose)
    initialize_typeface(debug=debug, verbose=verbose)
    initialize_console(debug=debug, verbose=verbose)
    initialize_game_data(debug=debug, verbose=verbose)
    initialize_expletives()

    return settings


def initialize_console(title=None, width=None, height=None, fullscreen=None, renderer=None, debug=None, verbose=None):
    global settings

    verbose = 1 if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    title = title or settings.title
    screen_width = width or settings.screen_width
    screen_height = height or settings.screen_height
    log_panel_height = settings.log_height

    fullscreen = fullscreen or settings.full_screen
    renderer = renderer or settings.renderer

    settings.main_console = tdl.console_init_root(screen_width, screen_height, title, fullscreen, renderer)
    tdl.console_set_default_foreground(settings.main_console, get_color('grey').tdl_color)
    tdl.console_set_default_background(settings.main_console, get_color('black').tdl_color)

    settings.log_pane = tdl.console_new(screen_width, log_panel_height)
    terminal.echo(f'Created console [{screen_width}x{screen_height}]: {title}', verbose=verbose)


def initialize_expletives():
    global settings

    expletives_filepath = settings.data_path / 'expletives.txt'
    with expletives_filepath.open() as stream:
        for line in stream.readlines():
            line = line.strip()
            if not line:
                continue
            settings.expletives.append(line)


def initialize_game_data(debug=None, verbose=None):
    global settings
    verbose = 1 if debug else max(int(verbose or 0), 0)  # cap minimum at 0

    data = find_data()
    populate_tile_data(data)
    populate_mob_data(data)
    populate_item_data(data)

    # Create a player
    player = Entity(name="player", type='player')
    player.add_component("tile", get_tile("player"))
    player.tile.lit_color = get_color('yellow')
    player.tile.unlit_color = get_color('dark_yellow')

    settings.entities = {}

    settings.player = player
    terminal.echo(f"Created player: {player}", verbose=verbose)

    dungeon = create_dungeon(width=settings.map_width, height=settings.map_height)
    settings.dungeon = dungeon
    settings.current_level = dungeon[0]

    random_starting_room = random.choice(settings.current_level.rooms)
    settings.player.add_component("position", random_starting_room.center)

    settings.entities[player.position] = player

    for position, tile in settings.current_level:
        # setup console
        render_tile(position, tile)

    for position, entity in settings.entities.items():
        if entity == settings.player:
            handle_lighting(entity.position, entity.position, settings.current_level)
            handle_view(entity.position, entity.position, settings.current_level)
        render_entity(entity)


def initialize_random_seed(seed=None, debug=None, verbose=None):
    verbose = 1 if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    seed = seed or random.randint(0, 2 ** 32 - 1)
    settings.seed = seed
    random.seed(seed)
    np.random.seed(seed)
    terminal.echo(f'Random seed is {seed}', verbose=verbose)


def initialize_typeface(name=None, table=None, size=None, debug=None, verbose=None):
    verbose = 1 if debug else max(int(verbose or 0), 0)  # cap minimum at 0
    name = name or settings.typeface_name
    table = table or settings.typeface_tablename
    size = size or settings.typeface_size

    typeface_path = str(settings.fonts_path / f'{name}.{table}.{size}.png')
    typeface_map_path = settings.fonts_path / f'{name}.{table}.map'
    with typeface_map_path.open() as stream:
        typeface_map = json.loads(stream.read())
    width, height = len(typeface_map), len(typeface_map[0])
    typeface_data = np.array(typeface_map).flatten()

    settings.typeface_mapper = {
        chr(value): index
        for index, value in enumerate(typeface_data)
        }

    tdl.console_set_custom_font(
        typeface_path,
        flags=settings.typeface_flags,
        nb_char_vertic=width,
        nb_char_horiz=height,
        )

    terminal.echo(f"Set font to: {typeface_path} [{width}x{height}]", verbose=verbose)
