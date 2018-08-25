# Collection of various effects that can be used independently
import enum
import typing

from kelte.engine.ecs import Entity
from kelte.engine.maths import Position

from .procgen.levels import Level


class DamageType(enum.Enum):
    undefined = 0
    physical = 1
    magical = 2
    spiritual = 3


def electrify(start: Position, end: Position, level: Level, entities: typing.Dict[Position, Entity]):
    damage_value = 10
    damaged = set()
    for position in start.ray(end):
        if damage_value < 0:
            break
        tile = level[position]
        if position in entities:
            damaged.add(position)
            entity = entities[position]
            damage(entity, damage_value, DamageType.magical)
            damage_value = damage_value - (damage_value // 2 or 1)
            for neighbor in position.neighbors:
                if neighbor in damaged:
                    continue
                damaged

        else:
            if not tile.walkable:
                break


def flame(start: Position, end: Position, level: Level):
    pass


def damage(entity: Entity, value: int, type: DamageType):
    return update_health(entity, value, type)


def heal(entity: Entity, value: int, type: DamageType):
    return update_health(entity, value, type)


def update_health(entity: Entity, value: int, type: DamageType):
    if not (hasattr(entity, 'health') and hasattr(entity, 'max_health')):
        return -1
    health = entity.health
    max_health = entity.max_health
    if hasattr(entity, 'resistances'):
        if type in entity.resistances:
            value = value * (1 - entity.resistances[type])
    health = max(0, min(max_health, health + value))
    entity.health = health
    return health
