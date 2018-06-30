import random

from ..math import Position
from .levels import Level
from .rooms import BoundingBox, Room


def create_level(size: BoundingBox = None, room_count: int = None) -> Level:
    room_count = room_count or random.randint(8, 10)
    max_attempts = room_count * 5
    size = size or BoundingBox(0, 0, random.randint(50, 80), random.randint(50, 80))
    level = Level(size.width, size.height)

    for attempt in range(max_attempts):
        # create the room
        position = Position(random.randint(1, level.width - 1), random.randint(1, level.height -1))
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

    print(level)

    return level


def create_room(position: Position = None, size: BoundingBox = None) -> Room:
    position = position or Position()
    size = size or BoundingBox(0, 0, random.randint(5, 12), random.randint(5, 12))
    size.x = position.x
    size.y = position.y
    return Room(bounding_box=size)


def build_dungeon():
    pass
