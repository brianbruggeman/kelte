import math
from functools import lru_cache

from .config import settings
from .colors import Color, get_color
from .tiles import Tile, get_tile
from .engine.ecs import Entity
from .engine.maths import Position
from .procgen import Level
from .rendering import render_tile
from .engine.ui import Panel


light_registry = {}


def cast_light(light_source: Entity, level: Level=None):
    level = settings.current_level if level is None else level
    gradient = light_source.light_gradient
    position = light_source.position
    point_data = {}

    if not (light_source.lit or light_source.debug):
        return point_data

    for edge in light_source.light_edges:
        edge = edge + position
        for index, pos in enumerate(position.ray(edge)):
            if index >= len(gradient):
                break
            if pos not in level:
                break
            tile = level[pos]
            gradient_value = gradient[index]
            tint = calculate_light_tint(tile.color, light_source.color, gradient_value)
            new_tile = tile.copy()
            new_tile.lit_color = tint
            print(index, pos, edge, tile, tint, light_source)
            new_tile.background_lit_color = light_source.color * gradient_value
            new_tile.lit = True
            new_tile.visible = True
            point_data[pos] = new_tile
            if tile.opaque:
                break
    return point_data


def create_light_source(name: str, type: str, tile: Tile = None, position: Position = None, color: Color = None, lit: bool = None, intensity: int = None, debug: bool = None):
    tile = get_tile(name) if tile is None else tile
    position = Position() if position is None else position
    color = tile.lit_color if color is None else color
    intensity = intensity or 255
    debug = debug or settings.debug

    gradient = calculate_light_gradient(intensity)
    radius = len(gradient)
    edges = calculate_light_edges(radius)
    print(name, radius, intensity, gradient)

    light_source = Entity(name=name, type=type)
    light_source.add_component('position', position)
    light_source.add_component('tile', tile)
    light_source.add_component('color', color)
    light_source.add_component('radius', radius)
    light_source.add_component('intensity', intensity)
    light_source.add_component('lit', lit)
    light_source.add_component('debug', debug)
    light_source.add_component('light_edges', edges)
    light_source.add_component('light_gradient', gradient)
    return light_source


def get_light_source(name: str, tile: Tile = None, copy: bool = True) -> Entity:
    global light_registry

    if name is not None and name not in light_registry:
        tile = tile or get_tile(name)
        light_source = create_light_source(name, type='items.lights', tile=tile)
        light_registry[name] = light_source

    elif name:
        light_source = light_registry[name]

    else:
        light_source = random.choice([m for m in light_registry.values()])

    return light_source.copy() if copy else light_source


def handle_lighting(level: Level):
    # Add new lighting
    grid = {}
    for light_source in level.light_sources:
        if not light_source.lit:
            continue
        point_data = cast_light(light_source, level)
        for pos, tile in point_data.items():
            grid[pos] = tile
    return grid


def populate_lighting_data(data_registry):
    global light_registry

    types = set()
    for light_type, data in data_registry.items():
        if not data:
            continue
        if not light_type.startswith('items.lights'):
            types.add(light_type)
            continue

        for light_data in data:
            light_name = light_data.get('name')
            intensity = light_data.get('intensity')
            light_source = create_light_source(name=light_name, type=light_type, intensity=intensity)
            light_registry[light_name] = light_source

    return light_registry


# ######################################################################
# Maths
# ######################################################################
@lru_cache()
def calculate_light_edges(radius: int):
    edges = set()
    area = []
    outside = []
    r2 = radius ** 2
    # capture all of the points segregating by "inside" vs "outside"
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 < r2:
                area.append(Position(x, y))
            else:
                outside.append(Position(x, y))

    # look at all of the outside points that neighbor inside points
    #   and save only the neighbors that are inside.
    for point in outside:
        for neighbor in point.neighbors:
            neighbor = Position(*neighbor)
            if neighbor in area:
                edges.add(neighbor)

    return sorted(edges)


@lru_cache()
def calculate_light_gradient(intensity: int = 255, intensity_maximum: int = None):
    intensity_k_value = 10  # controls how fast light degrades.  A higher value is faster
    intensity_maximum = settings.light_intensity_maximum if intensity_maximum is None else intensity_maximum
    gradient = []
    radius = 200
    for distance in range(radius):
        adjusted_intensity = min((intensity, intensity_maximum))
        gradient.append(adjusted_intensity)
        dist_calc = (1 if distance == 0 else distance) * intensity_k_value
        denom = math.log(dist_calc)
        if denom < 1:
            denom = 1
        intensity = math.floor(intensity / denom)
        if intensity <= 0:
            break
    return gradient


@lru_cache()
def calculate_light_tint(tile_color: Color, light_color: Color, intensity: int):
    new_tint = tile_color.tint(light_color, intensity=intensity / 256)
    print(tile_color, light_color, intensity, new_tint)
    return new_tint


if __name__ == '__main__':
    import random
    from .config import settings
    from .initialization import initialize, find_data

    initialize(level_count=1)

    level = settings.current_level

    for entity in level.entities:
        tile = entity.tile
        tile.name = entity.name
        tile.lit = True
        tile.explored = True
        tile.visible = True
        level[entity.position] = tile
        print(entity.name, tile.character, tile.c, tile.rendered)

    position, tile = random.choice([
        (position, tile)
        for position, tile in level
        if tile.transparent
        ])
    entity = Entity('player')
    entity.add_component('tile', tile.copy())
    tile.character = '@'
    tile.lit_color = get_color('yellow')

    torch = get_light_source('torch')
    torch.position = position
    torch.lit = True
    level.entities.append(torch)

    lighting_grid = handle_lighting(level)
    for pos, tile in lighting_grid.items():
        level[pos] = tile
        tile.lit = True

    for pos, tile in level:
        tile.visible = True
        tile.explored = True
        tile.lit = True
        if tile.type.startswith('dungeon'):
            continue
        print(f'{tile.name}={tile.rendered} vis={tile.visible} exp={tile.explored} lit={tile.lit}')


    print(level)
