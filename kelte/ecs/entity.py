"""
Entity is the entry point for creating new ecs-based entities.
"""
from dataclasses import dataclass, field

from ..maths import Position
from ..tiles import Tile
from .mixins import ECSAutoRegisterMixin, EcsIdentifierMixin
from .registry import Registrar

# Requirements:
#   Access entries through class attribute
#   Unique identifier
#   Can be labeled through a name, but not required to have a name
#   Serializable storing and loading


@dataclass()
class Entity(EcsIdentifierMixin, ECSAutoRegisterMixin, metaclass=Registrar):
    type: str = "entity"
    name: str = ""

    def add_component(self, name, data):
        from .component import Component

        component = Component(data)
        component.__set_name__(self, name)
        setattr(self, name, component)
        return component

    def remove_component(self, name):
        component = getattr(self, name)
        delattr(self, name)
        return component

    def __hash__(self):
        return hash(self.name)


@dataclass()
class PhysicalEntity(Entity):
    type: str = "physical"

    tile: Tile = field(default_factory=Tile)
    position: Position = field(default_factory=Position)
