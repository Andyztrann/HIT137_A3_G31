import cv2
import math
import numpy as np

from tile import Tile

class ImageProcessor:
    def load_image(self, file_path):
        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("Image could not be loaded!!!")
        return image

    def prepare_image(self, image, grid_size, max_size = 600):
        if grid_size not in (3, 4, 5):
            raise ValueError("Grid size must be 3, 4, or 5!!")
        height, width = image.shape[:2]

        scale = min(1.0, max_size / max(height, width))
        new_width = int(width * scale)
        new_height = int(height * scale)

        resized = cv2.resize(image, (new_width,new_height),interpolation = cv2.INTER_AREA)

        biggest_size = max(new_width, new_height)

        final_size = math.ceil(biggest_size / grid_size) * grid_size  

        vertical_padding = final_size - new_height
        horizontal_padding = final_size - new_width

        top = vertical_padding // 2
        bottom = vertical_padding - top

        left =horizontal_padding // 2
        right = horizontal_padding - left

        prepared = cv2.copyMakeBorder(
            resized,
            top,
            bottom,
            left,
            right,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )
        return prepared

    def split_image(self, image, grid_size):
        height, width = image.shape[:2]

        if height % grid_size != 0:
            raise ValueError("Image height must be divisible by grid size. ")
        if width % grid_size != 0:
            raise ValueError("Image Width must be divisible by grid size  ")

        tile_height = height // grid_size
        tile_width = width // grid_size

        tiles = []

        for row in range(grid_size):
            for col in range(grid_size):

                y1 = row * tile_height
                y2 = y1 + tile_height

                x1 = col * tile_width
                x2 = x1 + tile_width

                tile_image = image [y1:y2, x1:x2].copy()
                tile = Tile(tile_image, row, col)
                tiles.append(tile)
        return tiles
    
    def rebuild_image(self, tiles, grid_size):

        if not tiles:
            raise ValueError("No tiles available.")

        tile_height, tile_width = tiles[0].image.shape[:2]

        image_height = tile_height * grid_size
        image_width = tile_width * grid_size

        rebuilt = np.zeros(
            (image_height, image_width, 3),
            dtype=tiles[0].image.dtype
        )

        for tile in tiles:

            row = tile.current_row
            col = tile.current_col

            y1 = row * tile_height
            y2 = y1 + tile_height

            x1 = col * tile_width
            x2 = x1 + tile_width

            rebuilt[y1:y2, x1:x2] = tile.image

        return rebuilt            

