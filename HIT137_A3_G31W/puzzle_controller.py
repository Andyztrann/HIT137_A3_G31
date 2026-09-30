import random

from image_processor import ImageProcessor

from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)


class PuzzleController:
    """Controls puzzle setup, player actions, hints and completion."""

    SCRAMBLE_COUNTS = {
        3: 6,
        4: 12,
        5: 20
    }

    MAX_HINTS = 3

    def __init__(self, model, processor=None):
        self.model = model
        self.processor = processor or ImageProcessor()

        self.moves = 0
        self.selected_index = None
        self.hints_used = 0
        self.current_hint = None
        self.game_over = False

        self.scramble_log = []

        self.on_change = None
        self.on_complete = None

    def get_state(self):
        """Return the current game state for the GUI."""
        return {
            "moves": self.moves,
            "tiles_left": self.model.count_incorrect(),
            "hints_remaining": self.MAX_HINTS - self.hints_used,
            "selected_index": self.selected_index,
            "hint": self.current_hint,
            "game_over": self.game_over
        }

    def _notify(self):
        if self.on_change is not None:
            self.on_change(
                self.get_state()
            )

    def _valid_position(self, index):
        if not isinstance(index, int):
            return False

        if not 0 <= index < self.model.grid_size ** 2:
            return False

        row, col = divmod(
            index,
            self.model.grid_size
        )

        return self.model.get_tile(
            row,
            col
        ) is not None

    def _after_move(self):
        self.moves += 1

        self.current_hint = None
        self.selected_index = None

        self.game_over = self.model.is_solved()

        self._notify()

        if (
            self.game_over
            and self.on_complete is not None
        ):
            self.on_complete()

    def start_game(self, file_path, grid_size):
        """Load an image and start a new scrambled puzzle."""
        if grid_size not in (3, 4, 5):
            raise ValueError(
                "Grid size must be 3, 4 or 5."
            )

        image = self.processor.load_image(
            file_path
        )

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

        self.model.load_puzzle(
            prepared,
            tiles
        )

        self.scramble(
            grid_size
        )

        return prepared

    def _build_scramble_transformations(self, grid_size):
        """Generate all transformations before applying them."""
        available = list(
            range(grid_size ** 2)
        )

        random.shuffle(
            available
        )

        index1 = available.pop()
        index2 = available.pop()

        transformations = [
            SwapTransformation(
                index1,
                index2
            )
        ]

        log_entries = [
            (
                "swap",
                index1,
                index2
            )
        ]

        operation_types = [
            "rotate",
            "flip"
        ]

        remaining_operations = (
            self.SCRAMBLE_COUNTS[grid_size] - 3
        )

        operation_types += random.choices(
            [
                "rotate",
                "flip"
            ],
            k=remaining_operations
        )

        random.shuffle(
            operation_types
        )

        for operation in operation_types:
            index = available.pop()

            if operation == "rotate":
                angle = random.choice(
                    [
                        90,
                        180,
                        270
                    ]
                )

                transformations.append(
                    RotateTransformation(
                        index,
                        angle
                    )
                )

                log_entries.append(
                    (
                        "rotate",
                        index,
                        angle
                    )
                )

            else:
                direction = random.choice(
                    [
                        "horizontal",
                        "vertical"
                    ]
                )

                transformations.append(
                    FlipTransformation(
                        index,
                        direction
                    )
                )

                log_entries.append(
                    (
                        "flip",
                        index,
                        direction
                    )
                )

        return transformations, log_entries

    def scramble(self, grid_size=None):
        """Generate and apply a random puzzle scramble."""
        if grid_size is None:
            grid_size = self.model.grid_size

        if grid_size not in self.SCRAMBLE_COUNTS:
            raise ValueError(
                "Invalid grid size."
            )

        if (
            grid_size != self.model.grid_size
            or len(self.model.tiles) != grid_size ** 2
        ):
            raise ValueError(
                "Load the correct number of tiles first."
            )

        self.moves = 0
        self.selected_index = None
        self.hints_used = 0
        self.current_hint = None
        self.game_over = False

        transformations, log_entries = (
            self._build_scramble_transformations(
                grid_size
            )
        )

        for transformation in transformations:
            transformation.apply(
                self.model
            )

        self.scramble_log = log_entries

        self._notify()

    def swap_tiles(self, index1, index2):
        """Swap two puzzle positions as one move."""
        if self.game_over:
            return False

        if not all(
            map(
                self._valid_position,
                (
                    index1,
                    index2
                )
            )
        ):
            return False

        if index1 == index2:
            return False

        SwapTransformation(
            index1,
            index2
        ).apply(
            self.model
        )

        self._after_move()

        return True

    def select_tile(self, index):
        """Select, deselect or swap a tile."""
        if (
            self.game_over
            or not self._valid_position(index)
        ):
            return False

        if self.selected_index is None:
            self.selected_index = index

            self._notify()

            return False

        if self.selected_index == index:
            self.selected_index = None

            self._notify()

            return False

        return self.swap_tiles(
            self.selected_index,
            index
        )

    def rotate_tile(self, index):
        """Rotate a tile 90 degrees clockwise."""
        if (
            self.game_over
            or not self._valid_position(index)
        ):
            return False

        RotateTransformation(
            index,
            90
        ).apply(
            self.model
        )

        self._after_move()

        return True

    def flip_tile(self, index):
        """Flip a tile horizontally."""
        if (
            self.game_over
            or not self._valid_position(index)
        ):
            return False

        FlipTransformation(
            index,
            "horizontal"
        ).apply(
            self.model
        )

        self._after_move()

        return True

    def use_hint(self):
        """Return a hint for one incorrect tile."""
        if (
            self.game_over
            or self.hints_used >= self.MAX_HINTS
        ):
            return None

        incorrect = self.model.get_incorrect_tiles()

        if not incorrect:
            return None

        tile = random.choice(
            incorrect
        )

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

    def solve(self):
        """Restore every tile and finish the puzzle."""
        if (
            not self.model.tiles
            or self.game_over
        ):
            return False

        for tile in self.model.tiles:
            tile.restore()

        self.moves = 0
        self.selected_index = None
        self.current_hint = None
        self.game_over = True

        self._notify()

        return True

    def get_puzzle_image(self):
        """Rebuild and return the current puzzle image."""
        return self.processor.rebuild_image(
            self.model.tiles,
            self.model.grid_size
        )