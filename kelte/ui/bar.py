from dataclasses import dataclass, field

from ..colors import Color, get_color
from ..maths import Position


@dataclass()
class Bar:
    value: float = 100
    label: str = ''
    width: int = 10
    position: Position = field(default_factory=Position)
    active_color: Color = field(default=get_color('green'))
    inactive_color: Color = field(default=get_color('darker_red'))

    @property
    def active_cells(self):
        return int(self.width * self.value)

    @property
    def inactive_cells(self):
        return int(self.width * (1 - self.value))
