import datetime
import enum
import unicodedata
from dataclasses import dataclass

import tcod as tdl
from munch import munchify

from ..math import Direction, Position
from .modifier import KeyboardModifiers

SDL_PRESSED = 1
SDL_RELEASED = 0

SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3


class UserInputAction(enum.Enum):
    PRESSED = 1  # button down
    RELEASED = 2  # button up
    HELD = 3  # button is still down
    UNDEFINED = 4  # initial value

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class UserInputType(enum.Enum):
    KEYBOARD = 1
    MOUSE = 2


class Event:

    @property
    def sdl_event(self):
        raise NotImplementedError

    @sdl_event.setter
    def sdl_event(self, value):
        raise NotImplementedError


class KeyboardEvent(Event):

    def __init__(self, label=None, button=None, action=None, **keyboard_modifiers):
        self.label = label or ''

        if not button and len(self.label) == 1:
            button = ord(self.label)
        elif not button and len(self.label) > 1:
            button = ord(unicodedata.lookup(self.label.upper()))
        self.button = button or 0

        self.action = action or UserInputAction.PRESSED
        self.keyboard_modifiers = KeyboardModifiers()
        for mod_name, mod_value in keyboard_modifiers.items():
            try:
                setattr(self.keyboard_modifiers, mod_name, mod_value)
            except AttributeError:
                pass
        self.timestamp = datetime.datetime.utcnow()

    def __getattr__(self, item):
        if hasattr(self.keyboard_modifiers, item):
            return getattr(self.keyboard_modifiers, item)
        else:
            raise AttributeError(f'Could not find "{item}" on {self}')

    def __bool__(self):
        return True if self.button != 0 else False

    @property
    def sdl_event(self):
        if self.action is not UserInputAction.UNDEFINED:
            # see: https://wiki.libsdl.org/SDL_Keysym
            scancode = 0  # how do I get this... ?
            key = self.button
            mod = self.keyboard_modifiers.sdl_mod
            return tdl.lib.SDL_Keysym(scancode, key, mod)

    @sdl_event.setter
    def sdl_event(self, value):
        if value.type == tdl.lib.SDL_KEYDOWN:
            self.action = UserInputAction.PRESSED
        elif value.type == tdl.lib.SDL_KEYUP:
            self.action = UserInputAction.RELEASED

        # scancode = value.key.keysym.code  # why do I care about this?
        self.button = value.key.keysym.sym
        name = tdl.lib.SDL_GetKeyName(self.button)
        label = b''
        for i in range(100):
            if name[i] == b'\x00':
                break
            label += name[i]
        self.label = label.decode('utf-8').lower()
        self.keyboard_modifiers.sdl_mod = value.key.keysym.mod
        self.timestamp = datetime.datetime.utcnow()

    @property
    def tdl_key(self):
        key = tdl.libtcodpy.Key(
            self.button,
            self.label,
            True if self.action == UserInputAction.PRESSED else False,
            True if self.keyboard_modifiers.left_alt else False,
            True if self.keyboard_modifiers.left_control else False,
            True if self.keyboard_modifiers.right_alt else False,
            True if self.keyboard_modifiers.right_control else False,
            True if self.keyboard_modifiers.shift else False,
        )
        return key

    @tdl_key.setter
    def tdl_key(self, value):
        if isinstance(value, tdl.libtcodpy.Key):
            self.button = value.vk

            self.action = UserInputAction.PRESSED if value.pressed else UserInputAction.RELEASED
            self.label = value.c if value.c else self.label

            self.keyboard_modifiers.left_alt = True if value.lalt else self.keyboard_modifiers.left_alt
            self.keyboard_modifiers.right_alt = True if value.ralt else self.keyboard_modifiers.right_alt
            self.keyboard_modifiers.left_control = True if value.lctrl else self.keyboard_modifiers.left_control
            self.keyboard_modifiers.right_control = True if value.rctrl else self.keyboard_modifiers.right_control
            self.keyboard_modifiers.shift = True if value.shift else self.keyboard_modifiers.shift

            self.timestamp = datetime.datetime.utcnow()

    def __hash__(self):
        return hash((
            self.button,
            self.action,
            self.keyboard_modifiers.shift,
            self.keyboard_modifiers.alt,
            self.keyboard_modifiers.control,
            self.keyboard_modifiers.meta,
            self.keyboard_modifiers.num_key,
            self.keyboard_modifiers.caps_key,
            self.keyboard_modifiers.mode_key
            ))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        label = self.label or self.button
        key_mod = f'{self.keyboard_modifiers}+' if self.keyboard_modifiers else ''
        string = f'[{self.timestamp}] {self.action.name} {key_mod}{label}'
        return string


@dataclass()
class MouseEvent(Event):
    pixel_position: Position = Position(0, 0)
    delta_pixel: Position = Position(0, 0)
    coordinate_position: Position = Position(0, 0)
    delta_coordinate: Position = Position(0, 0)
    wheel_vector: Direction = Direction.NONE
    click_count: int = 0

    left_button_held: bool = False
    right_button_held: bool = False
    middle_button_held: bool = False

    left_button_released: bool = False
    right_button_released: bool = False
    middle_button_released: bool = False

    timestamp: datetime.datetime = datetime.datetime.utcnow()

    @property
    def tdl_mouse(self):
        """Unmapper from tcod types"""
        key = tdl.libtcodpy.Mouse(
            self.pixel_position.x,
            self.pixel_position.y,
            self.delta_pixel.x,
            self.delta_pixel.y,
            self.coordinate_position.x,
            self.coordinate_position.y,
            self.delta_coordinate.x,
            self.delta_coordinate.y,
            self.left_button_held,
            self.right_button_held,
            self.middle_button_held,
            self.left_button_released,
            self.right_button_released,
            self.middle_button_released,
            True if self.wheel_vector == Direction.UP else False,
            True if self.wheel_vector == Direction.DOWN else False,
        )
        return key

    @tdl_mouse.setter
    def tdl_mouse(self, value):
        """Mapper to tcod types"""
        if isinstance(value, tdl.libtcodpy.Mouse):
            self.pixel_position = Position(value.x, value.y)
            self.delta_pixel = Position(value.dx, value.dy)

            self.coordinate_position = Position(value.cx, value.cy)
            self.delta_coordinate = Position(value.cx, value.cy)

            self.left_button_held = value.lbutton
            self.right_button_held = value.rbutton

            self.middle_button_held = value.mbutton
            self.left_button_released = value.lbutton_pressed

            self.right_button_released = value.rbutton_pressed
            self.middle_button_released = value.mbutton_pressed

            if value.wheel_up:
                self.wheel_vector = Direction.UP
            elif value.wheel_down:
                self.wheel_vector = Direction.DOWN

            self.timestamp = datetime.datetime.utcnow()

    @property
    def sdl_event(self):
        pass

    @sdl_event.setter
    def sdl_event(self, value):

        if value.type in [tdl.lib.SDL_MOUSEBUTTONDOWN, tdl.lib.SDL_MOUSEBUTTONUP]:
            value = value.button
            # see: https://wiki.libsdl.org/SDL_MouseButtonEvent
            self.timestamp = datetime.datetime.utcnow()
            self.click_count = value.clicks
            self.pixel_position = Position(value.x, value.y)

            if value.state == SDL_PRESSED:
                if value.button == SDL_BUTTON_LEFT:
                    self.left_button_held = True
                elif value.button == SDL_BUTTON_MIDDLE:
                    self.middle_button_held = True
                elif value.button == SDL_BUTTON_RIGHT:
                    self.right_button_held = True

            elif value.state == SDL_RELEASED:
                if value.button == SDL_BUTTON_LEFT:
                    self.left_button_released = True
                elif value.button == SDL_BUTTON_MIDDLE:
                    self.middle_button_released = True
                elif value.button == SDL_BUTTON_RIGHT:
                    self.right_button_released = True

        elif value.type in [tdl.lib.SDL_MOUSEWHEEL]:
            value = value.wheel
            self.timestamp = datetime.datetime.utcnow()
            horizontal_scroll = value.x if value.direction == tdl.lib.SDL_MOUSEWHEEL_NORMAL else -value.x
            vertical_scroll = value.y if value.direction == tdl.lib.SDL_MOUSEWHEEL_NORMAL else -value.y
            x_direction = int(horizontal_scroll / horizontal_scroll if horizontal_scroll else 0)
            y_direction = int(vertical_scroll / vertical_scroll if vertical_scroll else 0)
            self.wheel_vector = Direction.get(Position(x_direction, y_direction))
            self.delta_pixel = Position(horizontal_scroll, vertical_scroll)

        elif value.type in [tdl.lib.SDL_MOUSEMOTION]:
            value = value.motion
            self.timestamp = datetime.datetime.utcnow()
            self.pixel_position = Position(value.x, value.y)
            self.delta_pixel = Position(value.xrel, value.yrel)

    def __hash__(self):
        buttons = (
            1 << 0 if self.left_button_held else 0
            + 1 << 1 if self.left_button_released else 0
            + 1 << 2 if self.right_button_held else 0
            + 1 << 3 if self.right_button_released else 0
            + 1 << 4 if self.middle_button_held else 0
            + 1 << 5 if self.middle_button_released else 0
            + 1 << 6 if self.click_count == 1 else 0
            + 1 << 7 if self.click_count == 2 else 0
        )

        hashable = (
            self.pixel_position.x, self.pixel_position.y,
            self.delta_pixel.x, self.delta_pixel.y,
            self.coordinate_position.x, self.coordinate_position.y,
            self.delta_coordinate.x, self.delta_coordinate.y,
            self.wheel_vector,
            buttons,
        )
        return hash(hashable)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        string = [f'[{self.timestamp}]', 'MOUSE']
        if self.wheel_vector.name != 'NONE':
            string.append('SCROLL')

        if self.pixel_position:
            string.append(str(self.pixel_position))
        if self.delta_pixel:
            string.append(str(self.delta_pixel))

        if self.left_button_held:
            string.append('PRESSED LEFT')
        if self.right_button_held:
            string.append('PRESSED RIGHT')
        if self.middle_button_held:
            string.append('PRESSED MIDDLE')

        if self.left_button_released:
            string.append('RELEASED LEFT')
        if self.right_button_released:
            string.append('RELEASED RIGHT')
        if self.middle_button_released:
            string.append('RELEASED MIDDLE')
        return ' '.join(string)


class QuitEvent(Event):
    timestamp: datetime.datetime = datetime.datetime.utcnow()

    @property
    def sdl_event(self):
        pass

    @sdl_event.setter
    def sdl_event(self, value):
        self.timestamp = datetime.datetime.utcnow()


def get_events(timeout: int = None, blocking: bool = True, **event_filters):
    user_event_mapping = _setup_filtering(**event_filters)

    if timeout is not None:
        tdl.lib.SDL_WaitEventTimeout(tdl.ffi.NULL, timeout)

    elif blocking:
        tdl.lib.SDL_WaitEvent(tdl.ffi.NULL)

    sdl_event = tdl.ffi.new('SDL_Event*')
    while tdl.lib.SDL_PollEvent(sdl_event):
        if sdl_event.type in user_event_mapping:
            event = user_event_mapping[sdl_event.type]()
            event.sdl_event = sdl_event
            if event:
                yield event
                # tdl.lib.SDL_FlushEvent(sdl_event)


def _setup_filtering(**event_filters):
    default_filter = {
        'keyboard': True,
        'mouse_wheel': True,
        'mouse_motion': True,
        'mouse_button': True,
        'pressed': True,
        'released': True,
        'quit': True
        }
    event_filters = event_filters or {}

    # Determine if the filters remove specific event types or include
    #  specific event types
    filter_out_events = any(v is False for v in event_filters.values())
    filter_on_events = any(v is True for v in event_filters.values())

    if not event_filters:
        event_filters = default_filter

    elif filter_out_events and not filter_on_events:
        for name, value in default_filter.items():
            event_filters.setdefault(name, value)

    elif filter_on_events and not filter_out_events:
        for name in default_filter:
            event_filters.setdefault(name, False)

    else:
        for name, value in default_filter.items():
            event_filters.setdefault(name, value)

    filters = munchify(event_filters)

    user_event_mapping = {}
    if filters.keyboard:
        if filters.pressed:
            user_event_mapping[tdl.lib.SDL_KEYDOWN] = KeyboardEvent
        if filters.released:
            user_event_mapping[tdl.lib.SDL_KEYUP] = KeyboardEvent

    if filters.mouse_wheel:
        user_event_mapping[tdl.lib.SDL_MOUSEWHEEL] = MouseEvent

    if filters.mouse_motion:
        user_event_mapping[tdl.lib.SDL_MOUSEMOTION] = MouseEvent

    if filters.mouse_button:
        if filters.pressed:
            user_event_mapping[tdl.lib.SDL_MOUSEBUTTONDOWN] = MouseEvent
        if filters.released:
            user_event_mapping[tdl.lib.SDL_MOUSEBUTTONUP] = MouseEvent

    if filters.quit:
        user_event_mapping[tdl.lib.SDL_QUIT] = QuitEvent

    return user_event_mapping
