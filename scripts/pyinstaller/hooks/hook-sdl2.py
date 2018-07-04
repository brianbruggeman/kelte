import sys
from pathlib import Path

# Install shared libraries to the working directory.
binaries = (
    [(Path(__file__).parent / "SDL2.dll", ".")] if sys.platform == "win32" else []
)
