class PuzzleModel:

    def __init__(self, grid_size=3):

        if grid_size not in (3, 4, 5):
            raise ValueError("Grid size must be 3, 4, or 5.")

        self.grid_size = grid_size
        self.tiles = []
        self.original_image = None

    def load_puzzle(self, original_image, tiles):

        expected_tiles = self.grid_size ** 2

        if len(tiles) != expected_tiles:
            raise ValueError(
                f"Expected {expected_tiles} tiles, "
                f"but received {len(tiles)}."
            )

        self.original_image = original_image.copy()
        self.tiles = tiles
    def get_tile(self, row, col):

        for tile in self.tiles:

            if (
                tile.current_row == row
                and tile.current_col == col
            ):
                return tile

        return None
    def swap_tiles(self, first_tile, second_tile):

        if first_tile is second_tile:
            return

        first_row = first_tile.current_row
        first_col = first_tile.current_col

        second_row = second_tile.current_row
        second_col = second_tile.current_col

        first_tile.set_position(
            second_row,
            second_col
        )

        second_tile.set_position(
            first_row,
            first_col
        )

    def count_incorrect(self):

        count = 0

        for tile in self.tiles:
            if not tile.correctness():
                count += 1

        return count
    def is_solved(self):

        if not self.tiles:
            return False

        for tile in self.tiles:
            if not tile.correctness():
                return False

        return True
    def get_incorrect_tiles(self):

        incorrect_tiles = []

        for tile in self.tiles:
            if not tile.correctness():
                incorrect_tiles.append(tile)

        return incorrect_tiles
    


   
