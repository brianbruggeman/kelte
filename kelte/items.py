import random

from kelte.engine.ecs import Entity
from kelte.engine.maths import Position
from kelte.tiles import Tile, get_tile

item_registry = {}


def create_item(name: str, type: str, tile: Tile = None, inventory: dict = None, position: Position = None):
    tile = get_tile(name) if tile is None else tile
    position = Position() if position is None else position
    inventory = {} if inventory is None else inventory

    item = Entity(name=name, type=type)
    item.add_component('tile', tile)
    item.add_component('position', position)
    if item is not None:
        item.add_component('inventory', inventory)
    return item


def populate_item_data(registry):
    global item_registry

    for item_type, data in registry.items():
        if not data:
            continue
        if not item_type.startswith('item'):
            continue

        for item_data in data:
            item_name = item_data.get('name')
            item_inventory = None if 'container' not in item_type else {}
            item = create_item(item_name, type=item_type, inventory=item_inventory)
            item_registry[item_name] = item

    return item_registry


def get_item(name: str, tile: Tile = None, copy: bool = True) -> Entity:
    global item_registry

    if name not in item_registry:
        tile = tile or get_tile(name)
        item = create_item(name, type='item', tile=tile)
        item_registry[name] = item

    elif name:
        item = item_registry[name]

    else:
        item = random.choice([m for m in item_registry.values()])

    return item.copy() if copy else item
