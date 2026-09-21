# HIT137 Assignment 3
# Owner: Andy
# Purpose: Transformation classes and Swap / Rotate / Flip logic.
# Actual implementation will be added by Andy.

class Transformation:
    def apply(self, model):
        raise NotImplementedError


class SwapTransformation(Transformation):
    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2

    def apply(self, model):
        model.tiles[self.index1], model.tiles[self.index2] = \
            model.tiles[self.index2], model.tiles[self.index1]


class RotateTransformation(Transformation):
    def __init__(self, index, angle):
        self.index = index
        self.angle = angle

    def apply(self, model):
        tile = model.tiles[self.index]
        tile.rotation = (tile.rotation + self.angle) % 360


class FlipTransformation(Transformation):
    def __init__(self, index, direction="horizontal"):
        self.index = index
        self.direction = direction

    def apply(self, model):
        tile = model.tiles[self.index]

        if self.direction == "horizontal":
            tile.flipped_horizontal = not tile.flipped_horizontal

        elif self.direction == "vertical":
            tile.flipped_vertical = not tile.flipped_vertical