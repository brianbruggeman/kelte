import typing
import uuid
from dataclasses import dataclass, field

from .entity import Entity
from .mixins import EcsIdentifierMixin

# Components
#   Only store data
#   Unique id
#   Register with component registry for system access
#   Serializable loading/storing

# Component Registry
#   Entry point for System
#   Provides methods for querying entries


@dataclass
class Component:
    data: typing.Any = None
    name: str = None
    entity: Entity = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __add__(self, other):
        return self.data + other

    def __delete__(self, instance):
        my_index = instance.__dict__.setdefault("components", []).index(self)
        instance.__dict__["components"].pop(my_index)
        if not instance.__dict__["components"]:
            instance.__dict__.pop("components")
        instance.__dict__.pop(self.name)

    def __eq__(self, other):
        return self.data == other

    def __floordiv__(self, other):
        return self.data // other

    def __get__(self, instance, owner):
        instance.__dict__.setdefault(self.name, self.data)
        return instance.__dict__[self.name]

    def __getattr__(self, item):
        # all components have `data`...check data
        if hasattr(self.data, item):
            return getattr(self.data, item)
        raise AttributeError(f"`Component` object has no attribute `{item}`")

    def __iter__(self):
        yield from self.data

    def __lt__(self, other):
        return self.data < other

    def __mul__(self, other):
        return self.data * other

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        instance.__dict__.setdefault("components", []).append(self)
        self.data = value
        self.entity = instance

    def __set_name__(self, owner, name):
        self.name = name

    def __setattr__(self, item, value):
        try:
            super().__setattr__(item, value)
        except AttributeError:
            for key in self.__annotations__.keys():
                attr = getattr(self, key)
                if hasattr(attr, item):
                    setattr(attr, item, value)
                    return
            raise AttributeError(f"`Component` object has no attribute `{item}`")

    def __sub__(self, other):
        return self.data - other

    def __str__(self):
        return str(self.data)

    def __truediv__(self, other):
        return self.data / other
