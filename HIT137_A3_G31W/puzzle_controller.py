# HIT137 Assignment 3
# Owner: Andy
# Purpose: Controller, gameplay logic and Model ↔ View coordination.
# Actual implementation will be added by Andy.

import random
from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)

class PuzzleController:
    def __init__(self, model):
        self.model = model
        self.moves = 0
        self.selected_index = None
        self.hints_used = 0

    def swap_tiles(self, index1, index2):
        if index1 == index2:
            return False

        swap = SwapTransformation(index1, index2)
        swap.apply(self.model)

        self.moves += 1
        return True
    
    def scramble(self, grid_size):
        counts = {3: 6, 4: 12, 5: 20}

        available = list(range(grid_size * grid_size))
        random.shuffle(available)

        print("Transformations:", counts[grid_size])
        print("Available positions:", available)
        
        index1 = available.pop()
        index2 = available.pop()

        swap = SwapTransformation(index1, index2)
        swap.apply(self.model)

        print("Swapped:", index1, index2)
        print("Remaining:", available)
        # One transformation (Swap) has already been performed.
        remaining = counts[grid_size] - 1

        # Guarantee at least one Rotate and one Flip.
        operations = ["rotate", "flip"]

        # Randomly choose the other transformations.
        operations += random.choices(
            ["rotate", "flip"],
            k=remaining - 2
        )

        random.shuffle(operations)

        print("Remaining operations:", operations)
        for operation in operations:
            index = available.pop()

            if operation == "rotate":
                angle = random.choice([90, 180, 270])
                transformation = RotateTransformation(index, angle)

            elif operation == "flip":
                direction = random.choice(["horizontal", "vertical"])
                transformation = FlipTransformation(index, direction)

            transformation.apply(self.model)
            print("Applied:", operation, "to tile:", index)