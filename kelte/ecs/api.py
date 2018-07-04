import typing

from .component import Component
from .entity import Entity


def add_component(entity: Entity, name: str, data: typing.Any) -> Component:
    return Component(entity, name, data)


def remove_component(entity: Entity, name: str) -> None:
    delattr(entity, name)
