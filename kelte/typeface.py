import json
import os
import sys
import time
import typing
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import freetype as ft
import numpy as np
from fontTools.ttLib import TTFont
from fuzzywuzzy import fuzz
from PIL import Image, ImageDraw, ImageFont

package_path = Path(__file__).parent.parent
darwin = sys.platform == "darwin"
linux = sys.platform.startswith("linux")
windows = sys.platform.startswith("win")


FREETYPE_SCALAR = 64


cp437 = [
    (0x0000, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022, 0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C),
    (0x25BA, 0x25C4, 0x2195, 0x203C, 0x00B6, 0x00A7, 0x25AC, 0x21A8, 0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC),
    (0x0020, 0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F),
    (0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F),

    (0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F),
    (0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x005F),
    (0x0060, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067, 0x0068, 0x0069, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F),
    (0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077, 0x0078, 0x0079, 0x007A, 0x007B, 0x007C, 0x007D, 0x007E, 0x2302),

    (0x00C7, 0x00FC, 0x00E9, 0x00E2, 0x00E4, 0x00E0, 0x00E5, 0x00E7, 0x00EA, 0x00EB, 0x00E8, 0x00EF, 0x00EE, 0x00EC, 0x00C4, 0x00C5),
    (0x00C9, 0x00E6, 0x00C6, 0x00F4, 0x00F6, 0x00F2, 0x00FB, 0x00F9, 0x00FF, 0x00D6, 0x00DC, 0x00A2, 0x00A3, 0x00A5, 0x20A7, 0x0192),
    (0x00E1, 0x00ED, 0x00F3, 0x00FA, 0x00F1, 0x00D1, 0x00AA, 0x00BA, 0x00BF, 0x2310, 0x00AC, 0x00BD, 0x00BC, 0x00A1, 0x00AB, 0x00BB),
    (0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556, 0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510),

    (0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F, 0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567),
    (0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B, 0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580),
    (0x03B1, 0x00DF, 0x0393, 0x03C0, 0x03A3, 0x03C3, 0x00B5, 0x03C4, 0x03A6, 0x0398, 0x03A9, 0x03B4, 0x221E, 0x03C6, 0x03B5, 0x2229),
    (0x2261, 0x00B1, 0x2265, 0x2264, 0x2320, 0x2321, 0x00F7, 0x2248, 0x00B0, 0x2219, 0x00B7, 0x221A, 0x207F, 0x00B2, 0x25A0, 0x00A0),
    ]

cp850 = cp437[0:8] + [
    (0x00C7, 0x00FC, 0x00E9, 0x00E2, 0x00E4, 0x00E0, 0x00E5, 0x00E7, 0x00EA, 0x00EB, 0x00E8, 0x00EF, 0x00EE, 0x00EC, 0x00C4, 0x00C5),
    (0x00C9, 0x00E6, 0x00C6, 0x00F4, 0x00F6, 0x00F2, 0x00FB, 0x00F9, 0x00FF, 0x00D6, 0x00DC, 0x00F8, 0x00A3, 0x00D8, 0x00D7, 0x0192),
    (0x00E1, 0x00ED, 0x00F3, 0x00FA, 0x00F1, 0x00D1, 0x00AA, 0x00BA, 0x00BF, 0x00AE, 0x00AC, 0x00BD, 0x00BC, 0x00A1, 0x00AB, 0x00BB),
    (0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x00C1, 0x00C2, 0x00C0, 0x00A9, 0x2563, 0x2551, 0x2557, 0x255D, 0x00A2, 0x00A5, 0x2510),

    (0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x00E3, 0x00C3, 0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x00A4),
    (0x00F0, 0x00D0, 0x00CA, 0x00CB, 0x00C8, 0x0131, 0x00CD, 0x00CE, 0x00CF, 0x2518, 0x250C, 0x2588, 0x2584, 0x00A6, 0x00CC, 0x2580),
    (0x00D3, 0x00DF, 0x00D4, 0x00D2, 0x00F5, 0x00D5, 0x00B5, 0x00FE, 0x00DE, 0x00DA, 0x00DB, 0x00D9, 0x00FD, 0x00DD, 0x00AF, 0x00B4),
    (0x00AD, 0x00B1, 0x2017, 0x00BE, 0x00B6, 0x00A7, 0x00F7, 0x00B8, 0x00B0, 0x00A8, 0x00B7, 0x00B9, 0x00B3, 0x00B2, 0x25A0, 0x00A0),
    ]

cp866 = cp437[0:8] + [
    (0x0410, 0x0411, 0x0412, 0x0413, 0x0414, 0x0415, 0x0416, 0x0417, 0x0418, 0x0419, 0x041A, 0x041B, 0x041C, 0x041D, 0x041E, 0x041F),
    (0x0420, 0x0421, 0x0422, 0x0423, 0x0424, 0x0425, 0x0426, 0x0427, 0x0428, 0x0429, 0x042A, 0x042B, 0x042C, 0x042D, 0x042E, 0x042F),
    (0x0430, 0x0431, 0x0432, 0x0433, 0x0434, 0x0435, 0x0436, 0x0437, 0x0438, 0x0439, 0x043A, 0x043B, 0x043C, 0x043D, 0x043E, 0x043F),
    (0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556, 0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510),

    (0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F, 0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567),
    (0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B, 0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580),
    (0x0440, 0x0441, 0x0442, 0x0443, 0x0444, 0x0445, 0x0446, 0x0447, 0x0448, 0x0449, 0x044A, 0x044B, 0x044C, 0x044D, 0x044E, 0x044F),
    (0x0401, 0x0451, 0x0404, 0x0454, 0x0407, 0x0457, 0x040E, 0x045E, 0x00B0, 0x2219, 0x00B7, 0x221A, 0x2116, 0x00A4, 0x25A0, 0x00A0),
]


class Shape(typing.NamedTuple):
    rows: int = 0
    cols: int = 0

    @property
    def flat_count(self):
        return self.rows * self.cols


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
    bitmap: bytes = None

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
        if not hasattr(self, "_path"):
            path = find_typeface(self.name)
            if path is None:
                raise RuntimeError(f"Could not find {self.name}")
            elif not path.exists():
                raise RuntimeError(f"Could not find {self.name}")
            setattr(self, "_path", path)
        return getattr(self, "_path")

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
        assets_path = package_path / 'assets'
        fonts_path = assets_path / 'fonts'
        path = fonts_path / f"{self.path.stem}_typeface.dat"
        if path.exists():
            with path.open() as stream:
                data = json.loads(stream.read())
                return data
        else:
            print(f"Memoized data was not found, building new file.")

    @available.setter
    def available(self, value):
        assets_path = package_path / 'assets'
        fonts_path = assets_path / 'fonts'
        path = fonts_path / f"{self.path.stem}_typeface.dat"
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

    def render(self, size=None, table_name=None, unicode_values=None, filepath=None):
        typeface_size = size or 16
        assets_path = package_path / 'assets'
        fonts_path = assets_path / 'fonts'
        table_mapping = {
            'cp437': cp437,
            'cp850': cp850,
            'cp866': cp866,
            'all': self.available,
            }
        table_name = table_name or 'all'
        unicode_values = unicode_values or table_mapping.get(table_name)
        if not isinstance(unicode_values[0], (list, tuple)):
            count = len(unicode_values)
            shape = self._best_shape(count)
            new_array = np.zeros(shape.flat_count, dtype=int)
            new_array[0:count] = np.array(unicode_values, dtype=int)
            unicode_values = new_array.reshape(shape).tolist()

        im = Image.new("RGB", (1440, 900))
        draw = ImageDraw.Draw(im)

        typeface_path = find_typeface('Deferral-Square')
        font = ImageFont.truetype(str(typeface_path), typeface_size)
        for index, row in enumerate(unicode_values):
            text = "".join(chr(c) for c in row)
            index = index * typeface_size
            draw.text((0, index), text, font=font)

        # remove unneccessory whitespaces if needed
        im = im.crop(im.getbbox())

        # write into file
        default_image_path = fonts_path / f"{self.path.stem}.{table_name}.{size}.png"
        image_path = filepath or default_image_path
        im.save(str(image_path))

        # write out unicode mapping
        default_map_path = fonts_path / f"{self.path.stem}.{table_name}.map"
        with default_map_path.open('w') as stream:
            stream.write(json.dumps(unicode_values, indent=4))

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
    from kelte.vendored import click

    @click.command()
    @click.option('-t', '--table', metavar='NAME', help='table to dump', type=click.Choice(['cp437', 'cp850', 'cp866', 'all']))
    @click.option('-n', '--name', metavar='NAME', help='typeface name', default='Deferral-Square', show_default=True)
    @click.option('-s', '--size', metavar='SIZE', help='typeface size', default=8, show_default=True, type=int)
    @click.option('-a', '--all', 'all_sizes', is_flag=True, help='build all sizes', show_default=True)
    def cli(table, name, size, all_sizes):
        typeface = Typeface(name)
        start, end = 5, 25
        if all_sizes:
            typeface.build(start, end)
            for size in range(start, end + 1):
                typeface.render(size, table_name=table)
        else:
            typeface.build(start, end)
            typeface.render(size, table_name=table)

    cli()
