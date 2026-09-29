# HIT137 Assignment 3
# Owner: Andy
# Purpose: Connect Model, Controller and View.

import tkinter as tk
from tkinter import messagebox

import cv2
from PIL import Image, ImageTk

from puzzle_model import PuzzleModel
from puzzle_controller import PuzzleController
from puzzle_view import PuzzleView


def main():

    # ==========================================
    # 1. CREATE AND CONNECT COMPONENTS
    # ==========================================

    root = tk.Tk()

    model = PuzzleModel(3)
    controller = PuzzleController(model)
    view = PuzzleView(root)

    view.controller = controller

    CANVAS_SIZE = 500

    # ==========================================
    # 2. DISPLAY IMAGES
    # ==========================================

    def convert_image(image):
        """Convert an OpenCV image into a Pillow image."""

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        result = Image.fromarray(rgb)

        return result.resize(
            (CANVAS_SIZE, CANVAS_SIZE)
        )

    def display_original():
        """Display the prepared original image."""

        if model.original_image is None:
            return

        image = convert_image(model.original_image)

        view.original_photo = ImageTk.PhotoImage(image)

        view.original_canvas.delete("all")

        view.original_canvas.create_image(
            250,
            250,
            image=view.original_photo,
            anchor="center"
        )

    # ==========================================
    # 3. REFRESH THE GUI
    # ==========================================

    def refresh(state):

        # Update counters.
        view.update_moves(state["moves"])
        view.update_tiles_left(state["tiles_left"])

        # Update the Hint button.
        view.set_hint_enabled(
            bool(model.tiles)
            and state["hints_remaining"] > 0
            and not state["game_over"]
        )

        if not model.tiles:
            return

        # Rebuild and display the current puzzle.
        puzzle = controller.get_puzzle_image()

        puzzle_image = convert_image(puzzle)

        view.display_puzzle_image(puzzle_image)

        # Draw green ticks on correctly placed tiles.
        view.clear_correct_ticks()

        for tile in model.tiles:

            if tile.correctness():

                view.draw_correct_tick(
                    tile.current_row,
                    tile.current_col
                )

        # Highlight the currently selected tile.
        selected = state["selected_index"]

        if selected is not None:

            row, col = divmod(
                selected,
                model.grid_size
            )

            view.highlight_selected_tile(row, col)

        # Display hint circles.
        hint = state["hint"]

        if hint is not None:

            current_row, current_col = hint["current"]
            home_row, home_col = hint["home"]

            view.draw_hint_circles(
                current_row,
                current_col,
                home_row,
                home_col
            )

    controller.on_change = refresh

    # ==========================================
    # 4. COMPLETION
    # ==========================================

    def lock_puzzle():

        view.disable_puzzle_input()

        # Additional macOS mouse bindings.
        view.puzzle_canvas.unbind("<Button-2>")
        view.puzzle_canvas.unbind("<Control-Button-1>")

    def handle_completion():

        lock_puzzle()

        view.show_completion_message()

    controller.on_complete = handle_completion

    # ==========================================
    # 5. MOUSE CONTROLS
    # ==========================================

    def get_clicked_tile(event):
        """Convert mouse coordinates into a tile index."""

        if not model.tiles or controller.game_over:
            return None

        x = event.x
        y = event.y

        # Ignore clicks outside the puzzle.
        if not (
            0 <= x < CANVAS_SIZE
            and 0 <= y < CANVAS_SIZE
        ):
            return None

        # Calculate the selected tile.
        col = x * model.grid_size // CANVAS_SIZE
        row = y * model.grid_size // CANVAS_SIZE

        index = row * model.grid_size + col

        return index

    def handle_left_click(event):
        """Select or swap tiles."""

        index = get_clicked_tile(event)

        if index is None:
            return

        controller.select_tile(index)

    def handle_right_click(event):
        """Rotate the selected tile clockwise."""

        index = get_clicked_tile(event)

        if index is None:
            return

        controller.rotate_tile(index)

        return "break"

    def handle_shift_click(event):
        """Flip the selected tile horizontally."""

        index = get_clicked_tile(event)

        if index is not None:

            controller.flip_tile(index)

        # Prevent the normal left-click action.
        return "break"

    def bind_mouse_controls():
        """
        Connect mouse actions to the controller.

        Call this AFTER loading an image because
        reset_view() restores the original GUI bindings.
        """

        canvas = view.puzzle_canvas

        canvas.bind(
            "<Button-1>",
            handle_left_click
        )

        canvas.bind(
            "<Button-3>",
            handle_right_click
        )

        canvas.bind(
            "<Shift-Button-1>",
            handle_shift_click
        )

        # Alternative right-click bindings for macOS.
        canvas.bind(
            "<Button-2>",
            handle_right_click
        )

        canvas.bind(
            "<Control-Button-1>",
            handle_right_click
        )

    # ==========================================
    # 6. HINT AND SOLVE BUTTONS
    # ==========================================

    def handle_hint():

        if not model.tiles:
            return

        controller.use_hint()

        # The controller automatically calls refresh().

    def handle_solve():

        if not model.tiles:
            return

        if controller.solve():

            lock_puzzle()

    # Connect buttons to the controller.
    view.hint_button.config(
        command=handle_hint
    )

    view.solve_button.config(
        command=handle_solve
    )

    # ==========================================
    # 7. LOAD IMAGE AND START THE GAME
    # ==========================================

    def handle_photo_selected(file_path, grid_size):

        try:

            # Load, split and scramble the image.
            controller.start_game(
                file_path,
                grid_size
            )

            # Display the prepared original image.
            display_original()

            # Display the scrambled puzzle.
            refresh(controller.get_state())

            # IMPORTANT:
            # Reconnect mouse handlers AFTER
            # Naro's reset_view() has executed.
            bind_mouse_controls()

        except (ValueError, OSError, cv2.error) as error:

            messagebox.showerror(
                "Image Error",
                str(error)
            )

    # Connect Naro's photo selection callback.
    view.on_photo_selected = handle_photo_selected

    # Initial mouse bindings.
    bind_mouse_controls()

    # ==========================================
    # 8. START APPLICATION
    # ==========================================

    root.mainloop()


if __name__ == "__main__":
    main()