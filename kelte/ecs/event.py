import typing
from dataclasses import dataclass

from .entity import Entity


@dataclass()
class Event:
    action: str = None
    entity: Entity = None
    data: typing.Any = None


