import cv2


class Transformation:
    """
    Parent class for all puzzle transformations.
    """

    @staticmethod
    def get_tile_at(model, index):
        # Check whether the selected position is valid.
        if not 0 <= index < model.grid_size ** 2:
            raise IndexError("Tile position is outside the puzzle grid.")

        # Convert the position into row and column.
        row, col = divmod(index, model.grid_size)

        # Find the tile currently occupying that position.
        tile = model.get_tile(row, col)

        if tile is None:
            raise ValueError("No tile exists at the requested position.")

        return tile

    def apply(self, model):
        raise NotImplementedError(
            "Each transformation must implement apply()."
        )


class SwapTransformation(Transformation):

    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2

    def apply(self, model):
        first = self.get_tile_at(model, self.index1)
        second = self.get_tile_at(model, self.index2)

        # Swapping a tile with itself changes nothing.
        if first is second:
            return False

        # Use Vinh's existing swapping method.
        model.swap_tiles(first, second)

        return True


class RotateTransformation(Transformation):

    def __init__(self, index, angle):
        self.index = index
        self.angle = angle

    def apply(self, model):

        rotations = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }

        if self.angle not in rotations:
            raise ValueError(
                "Rotation must be 90, 180 or 270 degrees."
            )

        tile = self.get_tile_at(model, self.index)

        # Actually rotate the tile's image.
        tile.image = cv2.rotate(
            tile.image,
            rotations[self.angle]
        )

        # Update the rotation information.
        tile.add_rotation(self.angle)

        return True


class FlipTransformation(Transformation):

    def __init__(self, index, direction="horizontal"):
        self.index = index
        self.direction = direction

    def apply(self, model):

        if self.direction not in ("horizontal", "vertical"):
            raise ValueError(
                "Flip direction must be horizontal or vertical."
            )

        tile = self.get_tile_at(model, self.index)

        # OpenCV: 1 = horizontal; 0 = vertical.
        flip_code = 1 if self.direction == "horizontal" else 0

        # Actually flip the tile's image.
        tile.image = cv2.flip(tile.image, flip_code)

        # Record which flip was performed.
        if self.direction == "horizontal":
            tile.flipped_horizontal = not tile.flipped_horizontal

        else:
            tile.flipped_vertical = not tile.flipped_vertical

        return True