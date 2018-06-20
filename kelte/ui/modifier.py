from dataclasses import dataclass


@dataclass()
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


@dataclass()
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
