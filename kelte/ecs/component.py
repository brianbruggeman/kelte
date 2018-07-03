import uuid

from .registry import EcsRegistry

# Components
#   Only store data
#   Unique id
#   Register with component registry for system access
#   Serializable loading/storing

# Component Registry
#   Entry point for System
#   Provides methods for querying entries


class Component(metaclass=EcsRegistry):
    @property
    def name(self):
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
        old_name = getattr(self, "_name", None)
        if old_name:
            delattr(self.entity, old_name)
        setattr(self, "_name", value)
        setattr(self.entity, value, self)

    def __add__(self, other):
        data = self.data + other
        return data

    def __eq__(self, other):
        if isinstance(other, Component):
            return self.data == other.data
        else:
            return self.data == other

    def __get__(self, instance, owner):
        return instance.__dict__["data"]

    def __getattr__(self, key):
        data = object.__getattribute__(self, "data")
        if hasattr(data, key):
            return getattr(data, key)
        else:
            raise AttributeError(f"Attribute, {key}, not found")

    def __init__(self, entity, name=None, data=None, id=None):
        self.entity = entity
        self.name = name
        self.data = data
        self.id = id or uuid.uuid4().hex

    def __repr__(self):
        return f"{type(self).__name__}(entity={self.entity.name or self.entity.id}, name={self.name}, data={self.data}, id={self.id})"

    def __set__(self, instance, value):
        instance.__dict__["data"] = value

    def __set_name__(self, instance, name):
        self.name = name
        instance.__dict__[name] = self

    def __str__(self):
        return str(self.data)
