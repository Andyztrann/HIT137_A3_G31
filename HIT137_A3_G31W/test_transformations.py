from transformations import SwapTransformation


class FakeModel:
    def __init__(self):
        self.tiles = ["A", "B", "C"]


model = FakeModel()

swap = SwapTransformation(0, 2)
swap.apply(model)

print(model.tiles)

from transformations import RotateTransformation

class FakeTile:
    def __init__(self):
        self.rotation = 0
        self.flipped_horizontal = False
        self.flipped_vertical = False

model.tiles = [FakeTile()]

rotate = RotateTransformation(0, 90)

rotate.apply(model)
print(model.tiles[0].rotation)

rotate.apply(model)
print(model.tiles[0].rotation)

from transformations import FlipTransformation

tile = model.tiles[0]

tile.flipped_horizontal = False
tile.flipped_vertical = False

flip = FlipTransformation(0, "horizontal")

flip.apply(model)
print(tile.flipped_horizontal, tile.flipped_vertical)

flip.apply(model)
print(tile.flipped_horizontal, tile.flipped_vertical)

from puzzle_controller import PuzzleController

model.tiles = ["A", "B", "C"]

controller = PuzzleController(model)

controller.swap_tiles(0, 2)
controller.swap_tiles(1, 1)

print(model.tiles)
print("Moves:", controller.moves)

# Test scrambling
# Test all three grid sizes
for size in [3, 4, 5]:
    print(f"\nTesting {size}x{size}")

    model.tiles = [
        FakeTile() for _ in range(size * size)
    ]

    controller = PuzzleController(model)
    controller.scramble(size)

    print("Player moves:", controller.moves)
    
    print("Rotated tiles:", sum(
    tile.rotation != 0 for tile in model.tiles
    ))

    print("Flipped tiles:", sum(
        tile.flipped_horizontal or tile.flipped_vertical
        for tile in model.tiles
    ))
    
    expected = {3: 6, 4: 12, 5: 20}

    rotated = sum(
        tile.rotation != 0 for tile in model.tiles
    )

    flipped = sum(
        tile.flipped_horizontal or tile.flipped_vertical
        for tile in model.tiles
    )

    assert rotated + flipped == expected[size] - 1
    assert controller.moves == 0

    print("TEST PASSED")