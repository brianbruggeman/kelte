from dataclasses import dataclass
from pathlib import Path


@dataclass()
class Settings:
    """Basic defaults"""

    repo_path: Path = Path(__file__).parent.parent
    assets_path: Path = repo_path / "assets"

    width: int = 80
    height: int = 50
    title: str = "Kelte"
    full_screen: bool = False
    font_path: bool = str(assets_path / "terminal8x8.png")
    main_console: int = 0
    keyboard_bindings = {}


settings = Settings()
