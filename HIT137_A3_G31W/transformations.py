import cv2


class Transformation:
    """Base class for all puzzle transformations."""

    @staticmethod
    def get_tile_at(model, index):
        if not 0 <= index < model.grid_size ** 2:
            raise IndexError(
                "Tile position is outside the puzzle grid."
            )

        row, col = divmod(
            index,
            model.grid_size
        )

        tile = model.get_tile(
            row,
            col
        )

        if tile is None:
            raise ValueError(
                "No tile exists at the requested position."
            )

        return tile

    def apply(self, model):
        raise NotImplementedError(
            "Each transformation must implement apply()."
        )


class SwapTransformation(Transformation):
    """Swap the tiles at two puzzle positions."""

    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2

    def apply(self, model):
        first = self.get_tile_at(
            model,
            self.index1
        )

        second = self.get_tile_at(
            model,
            self.index2
        )

        if first is second:
            return False

        model.swap_tiles(
            first,
            second
        )

        return True


class RotateTransformation(Transformation):
    """Rotate one tile by 90, 180 or 270 degrees."""

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

        tile = self.get_tile_at(
            model,
            self.index
        )

        tile.image = cv2.rotate(
            tile.image,
            rotations[self.angle]
        )

        tile.add_rotation(
            self.angle
        )

        return True


class FlipTransformation(Transformation):
    """Flip one tile horizontally or vertically."""

    def __init__(self, index, direction="horizontal"):
        self.index = index
        self.direction = direction

    def apply(self, model):
        if self.direction not in (
            "horizontal",
            "vertical"
        ):
            raise ValueError(
                "Flip direction must be horizontal or vertical."
            )

        tile = self.get_tile_at(
            model,
            self.index
        )

        if self.direction == "horizontal":
            flip_code = 1
        else:
            flip_code = 0

        tile.image = cv2.flip(
            tile.image,
            flip_code
        )

        if self.direction == "horizontal":
            tile.toggle_horizontal_flip()
        else:
            tile.toggle_vertical()

        return True