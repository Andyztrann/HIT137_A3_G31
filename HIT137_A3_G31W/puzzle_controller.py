# HIT137 Assignment 3
# Owner: Andy
# Purpose: Controller, transformations and gameplay logic.

import random

from image_processor import ImageProcessor

from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)


class PuzzleController:

    def __init__(self, model, processor=None):
        self.model = model
        self.processor = processor or ImageProcessor()

        self.moves = 0
        self.selected_index = None
        self.hints_used = 0
        self.current_hint = None
        self.game_over = False

        self.scramble_log = []

        # These will connect to Naro's GUI later.
        self.on_change = None
        self.on_complete = None

    # Get the current game information.
    def get_state(self):
        return {
            "moves": self.moves,
            "tiles_left": self.model.count_incorrect(),
            "hints_remaining": 3 - self.hints_used,
            "selected_index": self.selected_index,
            "hint": self.current_hint,
            "game_over": self.game_over
        }

    # Tell the GUI when something changes.
    def _notify(self):
        if self.on_change is not None:
            self.on_change(self.get_state())

    # Check whether a tile position exists.
    def _valid_position(self, index):
        if not isinstance(index, int):
            return False

        if not 0 <= index < self.model.grid_size ** 2:
            return False

        row, col = divmod(index, self.model.grid_size)

        return self.model.get_tile(row, col) is not None

    # Update the game after a successful player move.
    def _after_move(self):
        self.moves += 1

        # Hints disappear after the next move.
        self.current_hint = None
        self.selected_index = None

        # Check whether the puzzle is complete.
        self.game_over = self.model.is_solved()

        self._notify()

        if self.game_over and self.on_complete is not None:
            self.on_complete()

    # Load a new image and start a fresh puzzle.
    def start_game(self, file_path, grid_size):

        if grid_size not in (3, 4, 5):
            raise ValueError("Grid size must be 3, 4 or 5.")

        image = self.processor.load_image(file_path)

        prepared = self.processor.prepare_image(
            image,
            grid_size,
            max_size=500
        )

        tiles = self.processor.split_image(
            prepared,
            grid_size
        )

        self.model.grid_size = grid_size
        self.model.load_puzzle(prepared, tiles)

        self.scramble(grid_size)

        return prepared

    # Randomly scramble the puzzle.
    def scramble(self, grid_size=None):

        if grid_size is None:
            grid_size = self.model.grid_size

        counts = {
            3: 6,
            4: 12,
            5: 20
        }

        if grid_size not in counts:
            raise ValueError("Invalid grid size.")

        if (
            grid_size != self.model.grid_size
            or len(self.model.tiles) != grid_size ** 2
        ):
            raise ValueError(
                "Load the correct number of tiles first."
            )

        # Reset game information.
        self.moves = 0
        self.selected_index = None
        self.hints_used = 0
        self.current_hint = None
        self.game_over = False
        self.scramble_log = []

        # Create and randomise available tile positions.
        available = list(range(grid_size ** 2))
        random.shuffle(available)

        # Perform one swap.
        index1 = available.pop()
        index2 = available.pop()

        SwapTransformation(
            index1,
            index2
        ).apply(self.model)

        self.scramble_log.append(
            ("swap", index1, index2)
        )

        # Guarantee at least one rotation and one flip.
        operations = ["rotate", "flip"]

        # Randomly generate the remaining transformations.
        operations += random.choices(
            ["rotate", "flip"],
            k=counts[grid_size] - 3
        )

        random.shuffle(operations)

        # Apply each transformation to an unused position.
        for operation in operations:

            index = available.pop()

            if operation == "rotate":

                angle = random.choice(
                    [90, 180, 270]
                )

                RotateTransformation(
                    index,
                    angle
                ).apply(self.model)

                self.scramble_log.append(
                    ("rotate", index, angle)
                )

            else:

                direction = random.choice(
                    ["horizontal", "vertical"]
                )

                FlipTransformation(
                    index,
                    direction
                ).apply(self.model)

                self.scramble_log.append(
                    ("flip", index, direction)
                )

        self._notify()

    # Swap two selected tile positions.
    def swap_tiles(self, index1, index2):

        if self.game_over:
            return False

        if not all(
            map(self._valid_position, (index1, index2))
        ):
            return False

        if index1 == index2:
            return False

        SwapTransformation(
            index1,
            index2
        ).apply(self.model)

        self._after_move()

        return True

    # Handle tile selection and swapping.
    def select_tile(self, index):

        if self.game_over or not self._valid_position(index):
            return False

        # First click selects a tile.
        if self.selected_index is None:

            self.selected_index = index
            self._notify()

            return False

        # Clicking the same tile deselects it.
        if self.selected_index == index:

            self.selected_index = None
            self._notify()

            return False

        # Clicking a different tile swaps them.
        return self.swap_tiles(
            self.selected_index,
            index
        )

    # Rotate the selected tile 90 degrees clockwise.
    def rotate_tile(self, index):

        if self.game_over or not self._valid_position(index):
            return False

        RotateTransformation(
            index,
            90
        ).apply(self.model)

        self._after_move()

        return True

    # Flip the selected tile horizontally.
    def flip_tile(self, index):

        if self.game_over or not self._valid_position(index):
            return False

        FlipTransformation(
            index,
            "horizontal"
        ).apply(self.model)

        self._after_move()

        return True

    # Provide a hint for an incorrect tile.
    def use_hint(self):

        if self.game_over or self.hints_used >= 3:
            return None

        incorrect = self.model.get_incorrect_tiles()

        if not incorrect:
            return None

        # Randomly select one incorrect tile.
        tile = random.choice(incorrect)

        # Store its current and original positions.
        self.current_hint = {
            "current": (
                tile.current_row,
                tile.current_col
            ),
            "home": (
                tile.original_row,
                tile.original_col
            )
        }

        self.hints_used += 1

        self._notify()

        return self.current_hint

    # Automatically restore the puzzle.
    def solve(self):

        if not self.model.tiles or self.game_over:
            return False

        for tile in self.model.tiles:

            # Restore original tile position.
            tile.set_position(
                tile.original_row,
                tile.original_col
            )

            # Restore original image.
            tile.image = tile.original_image.copy()

            # Reset transformation information.
            tile.rotation = 0
            tile.flipped_horizontal = False
            tile.flipped_vertical = False

        # Reset gameplay information.
        self.moves = 0
        self.selected_index = None
        self.current_hint = None

        self.game_over = True

        self._notify()

        return True

    # Rebuild the current puzzle image for the GUI.
    def get_puzzle_image(self):

        return self.processor.rebuild_image(
            self.model.tiles,
            self.model.grid_size
        )