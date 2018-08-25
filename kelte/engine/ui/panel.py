import typing
from dataclasses import dataclass, field

import tcod

from kelte.engine.maths import Position


@dataclass
class Panel:
    name: str = 'main'
    width: int = 80
    height: int = 50
    position: Position = field(default_factory=Position)
    colors: typing.Dict[Position, tuple] = field(default_factory=dict)
    glyphs: typing.Dict[Position, str] = field(default_factory=dict)

    @property
    def pane(self):
        if not hasattr(self, '_pane'):
            self._pane = tcod.console_new(self.width, self.height)
        return self._pane

    def render(self, dst_con, dst_pos, dst_width, dst_height):
        width = min(dst_width, self.width)
        height = min(dst_height, self.height)
        tcod.console_blit(src=self._pane, x=0, y=0, w=width, h=height,
                          dst=dst_con, xdst=dst_pos.x, ydst=dst_pos.y,
                          ffade=1.0, bfade=1.0)

    def __del__(self):
        # try and release this, but sometimes python is wacky in its
        #  garbage collection, so use try/except
        try:
            tcod.console_delete(self._pane)
        except Exception as e:
            print(e)
            pass

    def __str__(self):
        lines = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                pos = Position(y, x)
                character = str(self.glyphs[pos])
                color = self.colors
            lines.append(row)
