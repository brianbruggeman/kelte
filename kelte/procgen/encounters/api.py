from pathlib import Path


def populate_encounters():
    for path in (Path(__file__).parent / 'data').glob('**/*.yml'):
        print(path)
