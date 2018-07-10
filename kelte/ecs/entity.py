"""
Entity is the entry point for creating new ecs-based entities.
"""
from dataclasses import dataclass

from .mixins import ECSAutoRegisterMixin, EcsIdentifierMixin
from .registry import Registrar

# Requirements:
#   Access entries through class attribute
#   Unique identifier
#   Can be labeled through a name, but not required to have a name
#   Serializable storing and loading


@dataclass()
class Entity(EcsIdentifierMixin, ECSAutoRegisterMixin, metaclass=Registrar):
    name: str = ""
    type: str = ''

    def add_component(self, name, data):
        # Removes a circular dependency
        from .component import Component

        component = Component(data)
        component.__set_name__(self, name)
        setattr(self, name, component)
        return component

    def remove_component(self, name):
        component = getattr(self, name)
        delattr(self, name)
        return component

    def copy(self):
        # Removes a circular dependency
        from .component import Component

        new_entity = Entity(name=self.name, type=self.type)
        for key, value in self.__dict__.items():
            if isinstance(value, Component):
                new_entity.add_component(key, value.copy())

        return new_entity

    def __hash__(self):
        return hash(self.name)


