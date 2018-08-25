from kelte.engine.maths import Position

from .config import settings
from .procgen import Level
from .rendering import render_tile


def cast_view(position: Position, level: Level):
    # TODO: This is damn slow.
    for edge in level.edges:
        for point in position.ray(edge, maxx=level.width, maxy=level.height, minx=0, miny=0):
            tile = level[point]
            entity = settings.entities.get(point)
            tile = entity.tile if entity else tile
            if tile.lit:
                yield point
            if tile.opaque:
                break


def handle_view(old: Position, new: Position, level: Level):
    # Handle field of view
    old_visible_positions = [] if old is None else [p for p in cast_view(old, level)]
    new_visible_positions = [p for p in cast_view(new, level)]
    unviewable_positions = set(old_visible_positions) - set(new_visible_positions)
    for newly_viewable_position in new_visible_positions:
        tile = level[newly_viewable_position]
        tile.explored = True
        entity = settings.entities.get(newly_viewable_position)
        if entity is not None:
            entity.tile.visible = True if tile.lit else False
            render_tile(newly_viewable_position, entity.tile)
        else:
            tile.visible = True if tile.lit else False
            render_tile(newly_viewable_position, tile)

    for unviewable_position in unviewable_positions:
        tile = level[unviewable_position]
        tile.visible = False
        entity = settings.entities.get(unviewable_position)
        if entity:
            entity.tile.visible = False
        render_tile(unviewable_position, tile)
