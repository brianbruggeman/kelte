import datetime
import typing
from dataclasses import dataclass

from ..entity import Entity


@dataclass()
class Event:
    type: str = "event"
    target: Entity = None
    data: typing.Any = None
    timestamp: datetime.datetime = datetime.datetime.utcnow()
