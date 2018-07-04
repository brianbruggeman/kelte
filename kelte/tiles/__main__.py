from .api import Tile

if __name__ == "__main__":
    print("\nData")
    print("-" * 79)
    for tile_name, tile in sorted(Tile.registry.items()):
        tile.visible = True
        tile.lit = False
        print(f"{tile_name}: {tile.rendered}", end="")
        tile.lit = True
        print(f" {tile.rendered}")
