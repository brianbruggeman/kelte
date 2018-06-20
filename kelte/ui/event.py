import enum
from dataclasses import dataclass

import tcod as tdl

from .modifier import KeyboardModifiers, MouseModifier
from ..math import Direction, Position


class UserInputAction(enum.Enum):
    PRESSED = 1  # button down
    RELEASED = 2  # button up
    HELD = 3  # button is still down


class UserInputType(enum.Enum):
    KEYBOARD = 1
    MOUSE = 2


@dataclass()
class KeyboardEvent:
    button: int = 0
    action: UserInputAction = UserInputAction.PRESSED
    label: str = 'Undefined'
    keyboard_modifiers: KeyboardModifiers = KeyboardModifiers()

    @property
    def tdl_key(self):
        """Unmapper from tcod types"""
        return tdl.libtcodpy.Key(
            self.button,
            self.label,
            True if self.action == UserInputAction.PRESSED else False,
            True if self.keyboard_modifiers.left_alt else False,
            True if self.keyboard_modifiers.left_control else False,
            True if self.keyboard_modifiers.right_alt else False,
            True if self.keyboard_modifiers.right_control else False,
            True if self.keyboard_modifiers.shift else False
            )

    @tdl_key.setter
    def tdl_key(self, value):
        """Mapper to tcod types"""
        if isinstance(value, tdl.libtcodpy.Key):
            self.button = value.vk
            if value.pressed:
                self.action = UserInputAction.PRESSED
            else:
                self.action = UserInputAction.RELEASED
            if value.c:
                self.label = value.c
            if value.lalt:
                self.keyboard_modifiers.left_alt = True
            if value.ralt:
                self.keyboard_modifiers.right_alt = True
            if value.lctrl:
                self.keyboard_modifiers.left_control = True
            if value.ralt:
                self.keyboard_modifiers.right_control = True
            if value.shift:
                self.keyboard_modifiers.shift = True

    def __init__(self, tdl_key=None, *args, **kwds):
        super().__init__(*args, **kwds)
        if tdl_key:
            self.tdl_key = tdl_key


@dataclass()
class MouseEvent:
    button: int = 0
    action: UserInputAction = UserInputAction.PRESSED
    pixel_position: Position = Position(0, 0)
    coordinate_position: Position = Position(0, 0)
    delta_coordinate: Position = Position(0, 0)
    wheel_vector: Direction = Direction.NONE

    left_button_held: bool = False
    right_button_held: bool = False
    middle_button_held: bool = False

    left_button_released: bool = False
    right_button_released: bool = False
    middle_button_released: bool = False

    mouse_modifiers: MouseModifier = MouseModifier()
    keyboard_modifiers: KeyboardModifiers = KeyboardModifiers()
