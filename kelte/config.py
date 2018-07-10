from dataclasses import dataclass, field
from pathlib import Path

import tcod
from munch import munchify

from .__metadata__ import package_metadata

pkg_data = munchify(package_metadata)


@dataclass()
class Settings:
    """Basic defaults"""

    # Package
    name: str = pkg_data.name
    package_path: Path = Path(__file__).parent.parent
    assets_path: Path = package_path / "assets"
    data_path: Path = assets_path / "data"
    fonts_path: Path = assets_path / "fonts"
    version = package_metadata["version"]

    # screen data
    screen_width: int = 80
    screen_height: int = 50
    title: str = f"Kelte  (v{version})"
    full_screen: bool = False
    main_console: int = 0

    # typeface
    typeface_name: str = "Deferral-Square"
    typeface_tablename: str = "cp437"
    typeface_size: int = 16
    typeface_flags: int = tcod.lib.TCOD_FONT_LAYOUT_ASCII_INROW | tcod.lib.TCOD_FONT_TYPE_GREYSCALE
    renderer: str = tcod.lib.TCOD_RENDERER_SDL
    typeface_mapper: dict = field(default_factory=dict)

    # Panel data
    log_height: int = int(screen_height * 0.15)
    main_log: list = field(default_factory=list)
    log_pane: int = 0

    mob_pane_width = int(screen_width * 0.2)
    mob_pane_height = screen_height
    mob_pane: int = 0

    map_width = screen_width - mob_pane_width
    map_height = screen_height - log_height

    # Misc
    expletives: list = field(default_factory=list)
    keyboard_bindings = {}

    # Map
    dungeon: list = field(default_factory=list)
    current_level: object = None  # actual object


settings = Settings()
