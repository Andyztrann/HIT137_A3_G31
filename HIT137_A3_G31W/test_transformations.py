import cv2
import numpy as np

from image_processor import ImageProcessor
from puzzle_model import PuzzleModel
from puzzle_controller import PuzzleController

from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)


# Create a real puzzle model for testing.
def make_model(size):

    rng = np.random.default_rng(42 + size)

    image = rng.integers(
        0,
        256,
        size=(size * 10, size * 10, 3),
        dtype=np.uint8
    )

    processor = ImageProcessor()

    tiles = processor.split_image(image, size)

    model = PuzzleModel(size)

    model.load_puzzle(image, tiles)

    return model


# TEST 1: Swapping
model = make_model(3)

first = model.get_tile(0, 0)
second = model.get_tile(0, 1)

controller = PuzzleController(model)

assert controller.swap_tiles(0, 1)

assert model.get_tile(0, 0) is second
assert model.get_tile(0, 1) is first

assert controller.moves == 1

# Swapping the same position must not count.
assert not controller.swap_tiles(1, 1)
assert controller.moves == 1

print("Swap: PASSED")


# TEST 2: Rotation
RotateTransformation(0, 90).apply(model)

expected_image = cv2.rotate(
    second.original_image,
    cv2.ROTATE_90_CLOCKWISE
)

assert np.array_equal(second.image, expected_image)

print("Rotation: PASSED")


# TEST 3: Flipping
FlipTransformation(0, "horizontal").apply(model)

expected_image = cv2.flip(
    expected_image,
    1
)

assert np.array_equal(second.image, expected_image)

print("Flip: PASSED")


# TEST 4: Restore the original orientation
FlipTransformation(0, "horizontal").apply(model)
RotateTransformation(0, 270).apply(model)

assert np.array_equal(
    second.image,
    second.original_image
)

print("Orientation restoration: PASSED")


# TEST 5: Scrambling all grid sizes
expected_counts = {
    3: 6,
    4: 12,
    5: 20
}

for size in [3, 4, 5]:

    model = make_model(size)

    assert model.count_incorrect() == 0

    controller = PuzzleController(model)

    controller.scramble(size)

    # Scrambling must not count as player moves.
    assert controller.moves == 0

    # One swap affects two positions.
    # Each remaining transformation affects one.
    expected_affected = expected_counts[size] + 1

    assert model.count_incorrect() == expected_affected

    # Check that the resulting puzzle can be rebuilt.
    processor = ImageProcessor()

    rebuilt = processor.rebuild_image(
        model.tiles,
        size
    )

    assert rebuilt.shape == model.original_image.shape

    print(f"{size}x{size} scrambling: PASSED")


print("\nALL INTEGRATION TESTS PASSED")

