from dataclasses import dataclass, field
from pathlib import Path

from munch import munchify

from .__metadata__ import package_metadata

pkg_data = munchify(package_metadata)

import tcod


@dataclass()
class Settings:
    """Basic defaults"""

    name: str = pkg_data.name

    package_path: Path = Path(__file__).parent.parent
    assets_path: Path = package_path / "assets"

    version = package_metadata["version"]

    width: int = 80
    height: int = 50
    title: str = f"Kelte  (v{version})"
    full_screen: bool = False
    typeface_name: str = "Deferral-Square"
    typeface_tablename: str = "all"
    typeface_size: int = 13
    typeface_flags: int = tcod.lib.TCOD_FONT_LAYOUT_ASCII_INROW | tcod.lib.TCOD_FONT_TYPE_GREYSCALE
    main_console: int = 0
    keyboard_bindings = {}
    renderer: str = tcod.lib.TCOD_RENDERER_SDL

    dungeon: list = field(default_factory=list)
    current_level: object = None  # actual object


settings = Settings()
