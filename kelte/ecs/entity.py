"""
Entity is the entry point for creating new ecs-based entities.
"""
from dataclasses import dataclass
from uuid import uuid4

from .component import Component

# Requirements:
#   Access entries through class attribute
#   Unique identifier
#   Can be labeled through a name, but not required to have a name
#   Serializable storing and loading


@dataclass()
class Entity:
    id: int = uuid4().hex
    name: str = None

    def add_component(self, name, data):
        component = Component(self, name, data)
        setattr(self, component.name, component)
        return component

    def remove_component(self, name):
        delattr(self, name)

    def __hash__(self):
        return hash(self.id)
