from .maths import Position
from .procgen import Level
from .rendering import render_tile
# from .utils.decorators import profile


# @profile
def cast_view(position: Position, level: Level):
    # TODO: This is damn slow.
    for edge in level.edges:
        for point in position.ray(edge, maxx=level.width, maxy=level.height, minx=0, miny=0):
            tile = level[point]
            if tile.lit:
                yield point
            if tile.opaque:
                break


def handle_view(old: Position, new: Position, level: Level):
    # Handle field of view
    old_visible_positions = [p for p in cast_view(old, level)]
    new_visible_positions = [p for p in cast_view(new, level)]
    unviewable_positions = set(old_visible_positions) - set(new_visible_positions)
    for newly_viewable_position in new_visible_positions:
        tile = level[newly_viewable_position]
        tile.explored = True
        tile.visible = True if tile.lit else False
        x, y = newly_viewable_position
        render_tile(newly_viewable_position, tile)

    for unviewable_position in unviewable_positions:
        tile = level[unviewable_position]
        tile.visible = False
        render_tile(unviewable_position, tile)

