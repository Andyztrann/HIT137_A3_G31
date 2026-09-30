import numpy as np

from puzzle_controller import PuzzleController
from image_processor import ImageProcessor
from puzzle_model import PuzzleModel


for grid in (3, 4, 5):

    # Generate a test image.
    rng = np.random.default_rng(grid)

    image = rng.integers(
        0,
        256,
        size=(grid * 10, grid * 10, 3),
        dtype=np.uint8
    )

    # Create Vinh's image processor and puzzle model.
    processor = ImageProcessor()
    model = PuzzleModel(grid)

    tiles = processor.split_image(image, grid)

    model.load_puzzle(image, tiles)

    # Create our controller.
    controller = PuzzleController(model)

    # Check the puzzle starts correctly.
    assert model.is_solved()

    # Test scrambling.
    controller.scramble(grid)

    expected = {
        3: 6,
        4: 12,
        5: 20
    }

    assert len(controller.scramble_log) == expected[grid]

    assert controller.moves == 0

    assert model.count_incorrect() == expected[grid] + 1

    # Check image reconstruction.
    rebuilt = controller.get_puzzle_image()

    assert rebuilt.shape == image.shape

    # Test player rotation.
    assert controller.rotate_tile(0)

    # Test player flipping.
    assert controller.flip_tile(1)

    assert controller.moves == 2

    # Test hints.
    hint = controller.use_hint()

    assert hint is not None
    assert controller.hints_used == 1

    # Hints must disappear after the next move.
    assert controller.rotate_tile(1)
    assert controller.current_hint is None

    # Test selecting and deselecting a tile.
    assert controller.select_tile(0) is False
    assert controller.selected_index == 0

    assert controller.select_tile(0) is False
    assert controller.selected_index is None

    # Test selecting two different tiles.
    assert controller.select_tile(0) is False
    assert controller.select_tile(1) is True

    assert controller.moves == 4

    # Test the Solve button's gameplay logic.
    assert controller.solve()

    assert controller.moves == 0
    assert model.is_solved()
    assert controller.game_over

    # Player actions must be disabled after completion.
    assert not controller.flip_tile(0)
    assert controller.use_hint() is None

    print(f"{grid}x{grid}: PASSED")


print("\nALL CONTROLLER TESTS PASSED")