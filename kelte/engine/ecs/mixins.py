from dataclasses import dataclass, field

from .descriptors import EcsIdentifierDescriptor


class ECSAutoRegisterMixin:
    def __getattr__(self, name):
        value = object.__getattribute__(self, name)
        if hasattr(value, "__get__"):
            value.__set_name__(self.__class__, name)
            value = value.__get__(self, self.__class__)
        for key in self.__annotations__.keys():
            obj = getattr(self, key)
            if hasattr(obj, name):
                return getattr(obj, name)
        return value

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, "__set__"):
                obj.name = name
                obj.entity = self
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)


class EcsIdentifierMixin:
    id: int = field(default_factory=EcsIdentifierDescriptor)
