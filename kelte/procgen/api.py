import random
import typing

from kelte.engine.ecs import Entity
from kelte.engine.maths import Position
from kelte.engine.maths.vector import DOWN, DOWN_LEFT, DOWN_RIGHT, LEFT, RIGHT, UP, UP_LEFT, UP_RIGHT
from kelte.items import get_item
from kelte.mobs import get_mob

from ..config import settings
from ..tiles import Tile, get_tile
from ..utils import terminal
from .cooridors import Cooridor
from .levels import Level
from .rooms import Room


def create_door(position: Position, tile: Tile, level: Level, verbose: typing.Union[int, bool] = None) -> typing.Union[Tile, None]:
    verbose = max(int(verbose or 0), 0)
    terminal.echo('Adding doors', verbose=verbose)
    wall = get_tile('wall')
    floor = get_tile('floor')
    if tile.name != 'floor':
        return None

    door = random.choice([get_tile('closed door'), get_tile('hidden door')])

    up, down, left, right = level[position + UP], level[position + DOWN], level[position + LEFT], level[position + RIGHT]
    up_right, up_left, down_right, down_left = level[position + UP_RIGHT], level[position + UP_LEFT], level[position + DOWN_RIGHT], level[position + DOWN_LEFT]
    if (up == down == wall):
        if (left == right == floor):
            if (up_right == floor or down_right == floor) and (up_left == wall or down_left == wall):
                return door
            elif (up_right == wall or down_right == wall) and (up_left == floor or down_left == floor):
                return door
    elif (left == right == wall):
        if (up == down == floor):
            if (up_right == floor or up_left == floor) and (down_right == wall or down_left == wall):
                return door
            elif (up_right == wall or up_left == wall) and (down_right == floor or down_left == floor):
                return door


def create_dungeon(level_count=None, width=None, height=None, verbose: typing.Union[int, bool] = None):
    verbose = max(int(verbose or 0), 0)
    level_count = level_count or 5
    width, height = width or random.randint(50, 150), height or random.randint(50, 150)

    levels = []
    terminal.echo("Building dungeon...")
    for level_index in range(level_count):
        if level_index == 0:
            levels.append(create_level(width=width, height=height, verbose=verbose - 1))
        else:
            last_level = levels[-1]
            seed_room = random.choice(last_level.rooms).copy()
            # add stairs
            # TODO
            levels.append(create_level(width=width, height=height, rooms=[seed_room]))
    terminal.echo(f"Dungeon built...{level_count} levels created.")
    return levels


def create_item(name: str = None) -> Entity:
    items = ['sword', 'dagger', 'cloak', 'boots', 'gloves']
    new_item = get_item(name=name or random.choice(items))
    return new_item


def create_level(width=None, height=None, room_count: int = None, rooms: typing.List[Room] = None, verbose: typing.Union[int, bool] = None):
    verbose = max(int(verbose or 0), 0)
    room_count = room_count or random.randint(8, 12)
    max_attempts = room_count * 5
    width, height = random.randint(50, 150) if width is None else width, random.randint(50, 150) if height is None else height

    level = Level(width, height)
    if rooms:
        level.rooms.extend(rooms)

    total_space = width * height
    terminal.echo('Building rooms', verbose=verbose)
    for attempt in range(max_attempts):
        # create the room
        position = Position(
            random.randint(1, level.width - 1), random.randint(1, level.height - 1)
            )
        new_room = create_room(position=position)

        # update its position on the map
        new_room.position = position

        # Check for overlap of existing rooms
        if any(new_room in room for room in level.rooms):
            continue

        if new_room not in level:
            continue

        # Save the room to the list of rooms
        level.rooms.append(new_room)

        if len(level.rooms) == room_count:
            break

    # load cooridors
    terminal.echo('Building cooridors', verbose=verbose)
    for index, room in enumerate(level.rooms):
        start = level.rooms[index - 1]
        end = room
        cooridor = Cooridor(start, end)
        level.cooridors.append(cooridor)

    open_positions = []
    terminal.echo('Adding doors', verbose=verbose)
    for position, current_tile in level:
        # Add doors
        tile = create_door(position, current_tile, level)
        if tile:
            level[position] = tile
        elif current_tile.name == 'floor':
            open_positions.append(position)

    level_density = len(open_positions) / total_space
    terminal.echo(f'Density: {level_density:0.2f}', verbose=verbose)

    # Add mobs
    terminal.echo('Adding mobs', verbose=verbose)
    max_mob_count = random.randint(3, len(level.rooms))
    max_attempts = max_mob_count * 2
    for attempt in range(max_attempts):
        mob = create_mob()

        position = random.choice(open_positions)
        mob.position = position
        position_index = open_positions.index(position)
        open_positions.pop(position_index)
        settings.entities[position] = mob

        level.entities.append(mob)

        if len(level.mobs) >= max_mob_count:
            break

    # Add items
    terminal.echo('Adding items', verbose=verbose)
    max_item_count = random.randint(3, len(level.rooms))
    max_attempts = max_item_count * 2
    for attempt in range(max_attempts):
        item = create_item()

        position = random.choice(open_positions)
        position_index = open_positions.index(position)
        open_positions.pop(position_index)
        item.position = position
        settings.entities[position] = item

        level.entities.append(item)

        if len(level.items) >= max_item_count:
            break

    return level


def create_mob(name: str = None) -> Entity:
    mob = get_mob(name=name)
    mob.tile.walkable = False
    return mob


def create_room(position: Position = None, width: int = None, height: int = None) -> Room:
    position = position or Position()
    width, height = width or random.randint(7, 12), height or random.randint(7, 12)
    room = Room(position=position, width=width, height=height)
    return room


if __name__ == "__main__":
    for level in create_dungeon(level_count=2):
        print(level)
