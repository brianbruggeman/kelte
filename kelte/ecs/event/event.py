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

    def __hash__(self):
        return hash((self.type, self.target, self.data))

    def __str__(self):
        string = [f'[{self.timestamp}]', self.type]
        target = self.target.name or self.target.id
        string.append(target)
        string.append(str(self.data))
        return ' '.join(string)
