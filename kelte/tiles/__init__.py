from pathlib import Path

import yaml

from .api import Tile, get_color


data_folder = Path(__file__).parent / "data"

for data_file in data_folder.glob("**/*.yml"):
    print(f"Loading data from: {data_file.name}")
    with data_file.open() as stream:
        items = yaml.load(stream.read())
        if not items:
            continue
        for item in items:
            # ----------------------------------------------------------
            # colors
            # ----------------------------------------------------------
            lit_color = item.get("lit_color")
            if isinstance(lit_color, str):
                item["lit_color"] = get_color(lit_color)
            unlit_color = item.get("unlit_color")
            if isinstance(unlit_color, str):
                item["unlit_color"] = get_color(unlit_color)
            # ----------------------------------------------------------
            # simple
            # ----------------------------------------------------------
            code = item.pop('code', None)
            if code:
                character = chr(code)
                item["character"] = character
            if not item.get("character"):
                name = item.get("name")
                item["character"] = name[0]

            Tile(**item)
