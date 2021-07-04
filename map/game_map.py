import numpy as np
from tcod import Console

from map import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.height, self.width = height, width

        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]


