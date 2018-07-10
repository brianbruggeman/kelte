import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_dynamic_libs

repo_path = Path(__file__).parent.parent.parent.parent
binary_ext = '*.so' if sys.platform not in ['win32'] else '*.dll'

binaries = collect_dynamic_libs("kelte", destdir=".")

data_locations = {
    'assets': repo_path / 'assets',
    'kelte/tiles/data': repo_path / 'kelte' / 'tiles' / 'data',
    }

datas = [(v, k) for k, v in data_locations.items()]
