import pathlib
import typing
from dataclasses import dataclass

from kelte.config import settings


@dataclass()
class Window:
    id: int = 0
    name: str = "main"
    font_path: typing.Union[str, pathlib.Path] = settings.font_path
    bindings = settings.keyboard_bindings

    def handle_event(self, event):
        """Handles event for this window"""

        # key = UserInputEvent(
        #     button = tdl.KEY_UP,
        #     label =
        #     )
        # movement_mapping = {
        #     tdl.KEY_UP: UserInputEvent(action='move', data=Direction.UP),
        #     tdl.KEY_DOWN: UserInputEvent(action='move', data=Direction.DOWN),
        #     tdl.KEY_LEFT: UserInputEvent(action='move', data=Direction.LEFT),
        #     tdl.KEY_RIGHT: UserInputEvent(action='move', data=Direction.RIGHT),
        #     }
        #
        # event = movement_mapping.get(key)
