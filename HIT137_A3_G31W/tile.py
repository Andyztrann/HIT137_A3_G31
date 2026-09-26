import numpy as np

class Tile:
    def __init__(self, image, original_row, original_col):
        self.original_image = image.copy()
        self.image = image.copy()
        self.original_row = original_row
        self.original_col = original_col 
        self.current_row = original_row
        self.current_col = original_col

        self.rotation = 0 
        self.flipped_horizontal = False
        self.flipped_vertical = False

    def set_position(self, row, col):
        self.current_row  = row
        self.current_col  = col

    def add_rotation(self, angle):
        self.rotation = (self.rotation + angle) % 360

    def toggle_horizontal_flip(self):
        self.flipped_horizontal != self.flipped_horizontal

    def toggle_vertical(self):
        self.flipped_vertical !=  self.flipped_vertical

    def  correctness(self):
        correct_position = (self.current_row == self.original_row and self.current_col == self.original_col)
        correct_orientation = np.array_equal(self.image, self.original_image)
        return correct_orientation and correct_position

    def __repr__(self):
        return (f"Tile(original=({self.original_row}, {self.original_col}), "
            f"current=({self.current_row}, {self.current_col}), "
            f"rotation={self.rotation})")

            
