import random
import typing

from ..maths import Position
from .cooridors import Cooridor
from .levels import Level, LevelSize
from .rooms import BoundingBox, Room, RoomSize


def create_level(
    size: RoomSize = None, room_count: int = None, rooms: typing.List[Room] = None
) -> Level:
    room_count = room_count or random.randint(8, 10)
    max_attempts = room_count * 5
    size = size or LevelSize(random.randint(50, 80), random.randint(50, 80))
    level = Level(size.width, size.height)
    if rooms:
        level.rooms.extend(rooms)

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

    for index, room in enumerate(level.rooms):
        start = level.rooms[index - 1]
        end = room
        cooridor = Cooridor(start, end)
        level.cooridors.append(cooridor)

    return level


def create_room(position: Position = None, size: RoomSize = None) -> Room:
    position = position or Position()
    size = size or BoundingBox(0, 0, random.randint(7, 12), random.randint(7, 12))
    size.x = position.x
    size.y = position.y
    return Room(bounding_box=size)


def create_dungeon(level_count=None, level_size=None):
    level_count = level_count or 5
    level_size = level_size or LevelSize(random.randint(50, 80), random.randint(50, 80))

    levels = []
    for level_index in range(level_count):
        if level_index == 0:
            levels.append(create_level(size=level_size))
        else:
            last_level = levels[-1]
            seed_room = random.choice(last_level.rooms).copy()
            levels.append(create_level(size=level_size, rooms=[seed_room]))
    return levels


if __name__ == "__main__":
    for level in create_dungeon(level_count=2):
        print(level)
