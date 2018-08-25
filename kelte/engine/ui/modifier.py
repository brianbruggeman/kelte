from dataclasses import dataclass

import tcod as tdl


@dataclass
class KeyboardModifiers:
    # ------------------------------------------------------------------
    #  Control
    # ------------------------------------------------------------------
    left_control: bool = False
    right_control: bool = False

    @property
    def control(self):
        return self.left_control or self.right_control

    @control.setter
    def control(self, value):
        self.left_control = self.right_control = value

    # ------------------------------------------------------------------
    #  Shift
    # ------------------------------------------------------------------
    left_shift: bool = False
    right_shift: bool = False

    @property
    def shift(self):
        return self.left_shift or self.right_shift

    @shift.setter
    def shift(self, value):
        self.left_shift = self.right_shift = value

    # ------------------------------------------------------------------
    #  Alt
    # ------------------------------------------------------------------
    right_alt: bool = False
    left_alt: bool = False

    @property
    def alt(self):
        return self.left_alt or self.right_alt

    @alt.setter
    def alt(self, value):
        self.left_alt = self.right_alt = value

    # ------------------------------------------------------------------
    #  Meta
    # ------------------------------------------------------------------
    left_meta: bool = False
    right_meta: bool = False

    @property
    def meta(self):
        return self.left_meta or self.right_meta

    @meta.setter
    def meta(self, value):
        self.left_meta = self.right_meta = value

    # ------------------------------------------------------------------
    #  Extras
    # ------------------------------------------------------------------
    num_key: bool = False
    caps_key: bool = False
    mode_key: bool = False

    @property
    def sdl_mod(self) -> int:
        # See: https://wiki.libsdl.org/SDL_Keymod
        mod = (
            tdl.lib.KMOD_LSHIFT & self.left_shift
            | tdl.lib.KMOD_RSHIFT & self.right_shift
            | tdl.lib.KMOD_LCTRL & self.left_control
            | tdl.lib.KMOD_RCTL & self.right_control
            | tdl.lib.KMOD_LALT & self.left_alt
            | tdl.lib.KMOD_RALT & self.right_alt
            | tdl.lib.KMOD_LGUI & self.left_meta
            | tdl.lib.KMOD_RGUI & self.right_meta
            | tdl.lib.KMOD_NUM & self.num_key
            | tdl.lib.KMOD_CAPS & self.caps_key
            | tdl.lib.KMOD_MODE & self.mode_key
        )
        return mod

    @sdl_mod.setter
    def sdl_mod(self, value):
        self.left_shift = bool(tdl.lib.KMOD_LSHIFT & value)
        self.right_shift = bool(tdl.lib.KMOD_RSHIFT & value)

        self.left_control = bool(tdl.lib.KMOD_LCTRL & value)
        self.right_control = bool(tdl.lib.KMOD_RCTRL & value)

        self.left_alt = bool(tdl.lib.KMOD_LALT & value)
        self.right_alt = bool(tdl.lib.KMOD_RALT & value)

        self.left_meta = bool(tdl.lib.KMOD_LGUI & value)
        self.right_meta = bool(tdl.lib.KMOD_RGUI & value)

        self.num_key = bool(tdl.lib.KMOD_NUM & value)
        self.caps_key = bool(tdl.lib.KMOD_CAPS & value)
        self.mode_key = bool(tdl.lib.KMOD_MODE & value)

    def __bool__(self):
        if (
            self.shift
            or self.alt
            or self.control
            or self.meta
            or self.caps_key
            or self.num_key
            or self.mode_key
        ):
            return True
        return False

    def __eq__(self, other):
        if (self.shift == other.shift
            and self.control == other.control
            and self.alt == other.alt
            and self.meta == other.meta
            and self.num_key == other.num_key
            and self.caps_key == other.caps_key
            and self.mode_key == other.mode_key):
            return True
        return False

    def __hash__(self):
        number = (
            1 << 0
            if self.shift
            else 0 + 1 << 1
            if self.alt
            else 0 + 1 << 2
            if self.control
            else 0 + 1 << 3
            if self.meta
            else 0 + 1 << 4
            if self.num_key
            else 0 + 1 << 5
            if self.caps_key
            else 0 + 1 << 6
            if self.mode_key
            else 0
        )
        return number

    def __str__(self):
        string = []
        if self.shift:
            string.append("SHIFT")
        if self.control:
            string.append("CONTROL")
        if self.alt:
            string.append("ALT")
        if self.meta:
            string.append("META")

        if self.num_key:
            string.append("NUM")
        if self.caps_key:
            string.append("CAPS")
        if self.mode_key:
            string.append("MODE")

        return "+".join(string)


@dataclass
class MouseModifier:

    # ------------------------------------------------------------------
    #  Meta
    # ------------------------------------------------------------------
    left_button_held: bool = False
    right_button_held: bool = False
    middle_button_held: bool = False

    left_button_released: bool = False
    right_button_released: bool = False
    middle_button_released: bool = False
