import json
import os
import sys
import time
import typing
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import freetype as ft
import numpy as np
from fontTools.ttLib import TTFont
from fuzzywuzzy import fuzz
from PIL import Image
from cairocffi import ImageSurface

package_path = Path(__file__).parent.parent
darwin = sys.platform == "darwin"
linux = sys.platform.startswith("linux")
windows = sys.platform.startswith("win")


FREETYPE_SCALAR = 64


class Shape(typing.NamedTuple):
    rows: int = 0
    cols: int = 0


class PixelSize(typing.NamedTuple):
    height: int = 16
    width: int = 16

    @property
    def size(self):
        return self.width * self.height


@dataclass
class Glyph:
    unicode: int
    char: str = None
    name: str = ""
    slot: ft.Glyph = None
    pixel_size: PixelSize = None
    bitmap = None

    @property
    def advance(self):
        return self.slot.advance

    @property
    def bitmap_top(self):
        return self.bitmap.bitmap_top

    @property
    def rows(self):
        return self.bitmap.rows


@dataclass
class TypefaceMatch:
    score: int
    path: typing.Union[Path, str]

    def __lt__(self, other):
        return self.score < other.score


@dataclass
class Typeface:
    name: str

    @property
    def path(self):
        if not hasattr(self, '_path'):
            path = find_typeface(self.name)
            if path is None:
                raise RuntimeError(f'Could not find {self.name}')
            elif not path.exists():
                raise RuntimeError(f'Could not find {self.name}')
            setattr(self, '_path', path)
        return getattr(self, '_path')

    @property
    def face(self):
        if not hasattr(self, "_face"):
            try:
                self._face = ft.Face(str(self.path))
            except ft.ft_errors.FT_Exception:
                raise RuntimeError(f"Could not open {self.path}")
        return getattr(self, "_face")

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._data = {}
        return self._data

    @property
    def available(self):
        """Memoizes looking through the typeface unicode availability
        """
        path = Path(f"assets/{self.path.stem}_typeface.dat")
        if path.exists():
            with path.open() as stream:
                data = json.loads(stream.read())
                return data
        else:
            print(f'Memoized data was not found, building new file.')

    @available.setter
    def available(self, value):
        path = Path(f"assets/{self.path.stem}_typeface.dat")
        with path.open("w") as stream:
            stream.write(json.dumps(value))

    @property
    def ttf(self):
        typeface = TTFont(str(self.path))
        return typeface

    def build(self, min_size=None, max_size=None, min_unicode=None, max_unicode=None):
        """populates data field based on typeface

        Iterates over all possible unicode values up to
        max_value and extracts available unicode values.  This list
        is memoized on the local filesystem so subsequent calls are
        significantly faster for sparse fonts.

        """
        if min_size is None and max_size is None:
            min_size = max_size = 16
        elif min_size is not None and max_size is None:
            max_size = min_size
        elif min_size is None and max_size is not None:
            min_size = 1
        min_unicode = min_unicode or 1
        max_unicode = max_unicode or 1024 * 64 - 1

        available = self.available or []
        times = []

        for size in range(min_size, max_size + 1):
            # print(f'Building bitmaps for pixel size: {size} for {self.name}')
            start = time.time()
            pixel_size = PixelSize(size, size)
            self.data.setdefault(size, dict())
            available_ready = available != []
            for unicode in available or range(min_unicode, max_unicode + 1):
                if not available_ready and not self.unicode_in_typeface(unicode):
                    continue
                char = chr(unicode)
                # if not available_ready:
                #     print(f'  {unicode} -> {char}')
                self.face.set_char_size(pixel_size.width * FREETYPE_SCALAR)
                self.face.load_char(char)
                slot = self.face.glyph
                bitmap = slot.bitmap
                try:
                    name = unicodedata.name(char).lower()
                except ValueError:
                    name = ""
                glyph = Glyph(unicode, char, name, slot, pixel_size, bitmap)
                self.data[size][unicode] = glyph
                if not available_ready:
                    available.append(unicode)
            end = time.time()
            duration = end - start
            times.append(duration)
            if not available_ready:
                self.available = available

    def render(self, size=16, unicode_values=None, filepath=None):
        filepath = filepath or f"{self.path.stem}_sprite_sheet.{size}.png"
        unicode_values = unicode_values or self.available
        glyphs = self.data[size]
        shape = self._best_shape(count=len(unicode_values))
        data = []
        row = []
        for unicode in unicode_values:
            if len(row) > shape.cols:
                data.append(row)
                row = []
            glyph = glyphs.get(unicode)
            row.append(glyph)

    def unicode_is_visible(self, unicode):
        if chr(unicode) in ["\r", "\n", "\t", " "]:
            return False
        return True

    def unicode_in_typeface(self, unicode):
        for cmap in self.ttf["cmap"].tables:
            if cmap.isUnicode():
                if unicode in cmap.cmap:
                    return True
        return False

    def _best_shape(self, count):
        rows = count
        cols = 1
        while cols < rows:
            rows = rows // 2
            cols = cols * 2
        remaining = count - rows * cols
        if remaining:
            rows += 1
        shape = Shape(rows, cols)
        return shape

    def __getitem__(self, key):
        return self.data[key]


def build_typeface_spritesheet():
    pass


def find_typeface(name):
    font_folders = [
        # package
        Path(".").absolute(),
        Path(package_path / "assets" / "fonts"),
        # mac
        Path("~/Library/Fonts").expanduser() if darwin else None,
        Path("/Library/Fonts") if darwin else None,
        Path("/Network/Library/Fonts") if darwin else None,
        Path("/System/Library/Fonts") if darwin else None,
        Path("/System/Folder/Fonts") if darwin else None,
        # linux
        Path("/usr/share/fonts") if linux else None,
        Path("~/.fonts").expanduser() if linux else None,
        # windows
        Path(os.getenv("WINDIR"), "Fonts") if windows else None,
    ]

    qualifier_match_order = {
        "Regular": 10,
        "Normal": 9,
        "Book": 8,
        "Narrow": 7,
        "Condensed": 6,
        "Wide": 5,
        "Expanded": 4,
        "ExtraWide": 3,
        "UltraCondensed": 2,
        "Square": 1,
    }

    possible_matches = []
    for folder in font_folders:
        if folder is None:
            continue
        if not folder.exists():
            continue
        for typeface_path in folder.glob("*.[to]tf"):
            if typeface_path.stem == name or typeface_path.name == name:
                # exact matches here are a win
                return typeface_path

            elif name in typeface_path.name:
                possible_matches.append(typeface_path)

    # Only do this if we don't have an exact match
    fuzzy_matched = []

    for typeface_path in possible_matches:
        name_score = fuzz.ratio(name, str(typeface_path))
        if name_score is None:
            continue
        name_match = TypefaceMatch(name_score, typeface_path)
        best_qualifier_match = None
        for qualifier in qualifier_match_order:
            if qualifier not in typeface_path.name:
                continue
            qualifier_score = fuzz.ratio(qualifier, str(typeface_path))
            qualifier_match = TypefaceMatch(qualifier_score, qualifier)
            if not best_qualifier_match:
                best_qualifier_match = qualifier_match
            else:
                best_qualifier_match = max(qualifier_match, best_qualifier_match)
        match_score = (
            name_match.score + best_qualifier_match.score
        ) * qualifier_match_order.get(best_qualifier_match.path)
        match = (match_score, typeface_path)
        fuzzy_matched.append(match)

    for score, path in reversed(sorted(fuzzy_matched)):
        return path


if __name__ == "__main__":
    import sys

    def run(font_name):
        typeface = Typeface(font_name)
        typeface.build(5, 25)

    font_name = "Deferral"
    if len(sys.argv) > 1:
        args = [v for v in sys.argv[1:] if not v.startswith("-")]
        if args:
            font_name = args[-1]

    run(font_name)
