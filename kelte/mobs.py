import random

from kelte.maths import Position
from kelte.tiles import get_tile, Tile
from kelte.ecs import Entity


mob_registry = {}


def create_mob(name: str, type: str, tile: Tile = None, health: int = None, inventory: dict = None, position: Position = None):
    tile = get_tile(name) if tile is None else tile
    position = Position() if position is None else position
    health = 10 if health is None else health
    inventory = {} if inventory is None else inventory

    mob = Entity(name=name, type=type)
    mob.add_component('tile', tile)
    mob.add_component('position', position)
    mob.add_component('health', health)
    mob.add_component('inventory', inventory)
    return mob


def populate_mob_data(registry):
    global mob_registry

    for mob_type, data in registry.items():
        if not data:
            continue
        if not mob_type.startswith('mob'):
            continue

        for mob_data in data:
            mob_name = mob_data.get('name')
            mob = create_mob(name=mob_name, type=mob_type)
            mob_registry[mob_name] = mob

    return mob_registry


def get_mob(name: str, tile: Tile = None, copy: bool = True) -> Entity:
    global mob_registry

    if name is not None and name not in mob_registry:
        tile = tile or get_tile(name)
        mob = create_mob(name, type='mob', tile=tile)
        mob_registry[name] = mob

    elif name:
        mob = mob_registry[name]

    else:
        mob = random.choice([m for m in mob_registry.values()])

    return mob.copy() if copy else mob
