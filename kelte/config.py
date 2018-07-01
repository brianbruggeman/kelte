from dataclasses import dataclass, field
from pathlib import Path

from munch import munchify

from .__metadata__ import package_metadata

pkg_data = munchify(package_metadata)

@dataclass()
class Settings:
    """Basic defaults"""

    name: str = pkg_data.name

    repo_path: Path = Path(__file__).parent.parent
    assets_path: Path = repo_path / "assets"

    width: int = 80
    height: int = 50
    title: str = "Kelte"
    full_screen: bool = False
    font_path: bool = str(assets_path / "terminal8x8.png")
    main_console: int = 0
    keyboard_bindings = {}

    dungeon: list = field(default_factory=list)
    current_level: object = None  # actual object


settings = Settings()
