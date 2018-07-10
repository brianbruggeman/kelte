from .colors import Color, get_color
from .config import settings
from .maths import Position
from .procgen import Level
from .rendering import render_tile


def cast_light(position: Position, level: Level, intensity: int = None, color: Color = None, threshold: int = None):
    light_color = color if color is not None else get_color('grey')
    light_intensity = intensity if intensity is not None else 2048
    visibility_threshold = threshold if threshold is not None else 10
    intensity_gradient = []
    for light_distance in range(1, 20):
        denom = light_distance ** 2
        current_intensity = min(512, light_intensity) // denom
        if current_intensity < visibility_threshold:
            break
        intensity_gradient.append(current_intensity)
    light_radius = len(intensity_gradient)

    for edge in get_edges_from_radius(position, radius=light_radius):
        for index, point in enumerate(position.ray(edge)):
            dx, dy = point.x - position.x, point.y - position.y
            if index >= len(intensity_gradient):
                break
            elif dx ** 2 + dy ** 2 > light_radius ** 2:
                break
            tile = level[point]
            entity = settings.entities.get(point)
            if entity:
                tile = entity.tile
            new_tint = tile.lit_color.tint(light_color)
            yield point, new_tint, intensity_gradient[index] / (light_intensity / (len(intensity_gradient) * 2))
            if tile.opaque:
                break


def get_edges_from_radius(position: Position, radius: int):
    max_x = position.x + radius
    min_x = position.x - radius
    max_y = position.y + radius
    min_y = position.y - radius
    for x in range(min_x, max_x + 1):
        yield Position(x, min_y)
        yield Position(x, max_y)
    for y in range(min_y, max_y + 1):
        yield Position(min_x, y)
        yield Position(max_x, y)


def handle_lighting(old: Position, new: Position, level: Level, color: Color = None):
    # Add new lighting
    light_color = color or get_color('grey')
    old_positions = {p: (c, i) for p, c, i in cast_light(old, level, color=light_color)}
    new_positions = {p: (c, i) for p, c, i in cast_light(new, level, color=light_color)}
    unlit_positions = set(old_positions.keys()) - set(new_positions.keys())
    for newly_lit_position, (tint, intensity) in new_positions.items():
        old_positions.pop(newly_lit_position, None)
        tile = level[newly_lit_position]
        tile.explored = True
        entity = settings.entities.get(newly_lit_position)
        if entity:
            tile = entity.tile
            tile.explored = True
        tile_color = tile.lit_color * intensity + tint
        background_tile_color = tile.background_lit_color
        render_tile(newly_lit_position, tile, tile_color, background_tile_color)

    # Remove old lighting
    for unlit_position in unlit_positions:
        tile = level[unlit_position]
        render_tile(unlit_position, tile)


if __name__ == '__main__':
    import random
    from .procgen import create_level

    level = create_level()
    for position, tile in level:
        tile.visible = True
        tile.explored = True

    position, tile = random.choice([
        (position, tile)
        for position, tile in level
        if tile.transparent
        ])
    tile.character = '@'
    tile.lit_color = get_color('yellow')

    light_color = get_color('black')

    cast_light(position, level, color=light_color)

    print(level)
