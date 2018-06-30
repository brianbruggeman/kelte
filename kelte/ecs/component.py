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

    def __init__(self, entity, name=None, data=None, id=None):
        self.entity = entity
        self.name = name
        self.data = data
        self.id = id or uuid.uuid4().hex

        # Auto-add component to entity
        setattr(entity, name, self)
        # entity.components[name] = self

    def __get__(self, obj, obj_type):
        if obj is None:
            return self
        else:
            return self.data

    def __getattr__(self, key):
        data = object.__getattribute__(self, "data")
        if hasattr(data, key):
            return getattr(data, key)
        else:
            raise AttributeError(f"Attribute, {key}, not found")

    def __delete__(self, instance):
        raise AttributeError

    def __repr__(self):
        return f"{type(self).__name__}(entity={self.entity}, name={self.name}, data={self.data}, id={self.id})"

    def __set__(self, obj, value):
        if obj is None:
            raise AttributeError
        else:
            setattr(self, "data", value)
            return self.data

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other

    def __add__(self, other):
        Class = self.__class__
        data = self.data + other
        inst = Class(self.entity, self.name, data, self.id)
        return inst
