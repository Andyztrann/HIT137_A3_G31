import tkinter as tk

from tkinter import messagebox

import cv2

from PIL import (
    Image,
    ImageTk
)

from puzzle_model import PuzzleModel
from puzzle_controller import PuzzleController
from puzzle_view import PuzzleView


def main():
    root = tk.Tk()

    model = PuzzleModel(3)

    controller = PuzzleController(
        model
    )

    view = PuzzleView(
        root
    )

    canvas_size = 500

    def convert_image(image):
        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        return Image.fromarray(
            rgb
        ).resize(
            (
                canvas_size,
                canvas_size
            )
        )

    def display_original():
        if model.original_image is None:
            return

        image = convert_image(
            model.original_image
        )

        view.original_photo = ImageTk.PhotoImage(
            image
        )

        view.original_canvas.delete(
            "all"
        )

        view.original_canvas.create_image(
            250,
            250,
            image=view.original_photo,
            anchor="center"
        )

    def refresh(state):
        view.update_moves(
            state["moves"]
        )

        view.update_tiles_left(
            state["tiles_left"]
        )

        view.set_hint_enabled(
            bool(model.tiles)
            and state["hints_remaining"] > 0
            and not state["game_over"]
        )

        if not model.tiles:
            return

        puzzle_image = convert_image(
            controller.get_puzzle_image()
        )

        view.display_puzzle_image(
            puzzle_image
        )

        view.clear_hint_circles()
        view.clear_correct_ticks()

        for tile in model.tiles:
            if tile.correctness():
                view.draw_correct_tick(
                    tile.current_row,
                    tile.current_col
                )

        selected = state[
            "selected_index"
        ]

        if selected is not None:
            row, col = divmod(
                selected,
                model.grid_size
            )

            view.highlight_selected_tile(
                row,
                col
            )

        hint = state["hint"]

        if hint is not None:
            (
                current_row,
                current_col
            ) = hint["current"]

            (
                home_row,
                home_col
            ) = hint["home"]

            view.draw_hint_circles(
                current_row,
                current_col,
                home_row,
                home_col
            )

    def lock_puzzle():
        view.disable_puzzle_input()

        view.puzzle_canvas.unbind(
            "<Button-2>"
        )

        view.puzzle_canvas.unbind(
            "<Control-Button-1>"
        )

    def handle_completion():
        lock_puzzle()

        view.show_completion_message()

    def get_clicked_tile(event):
        if (
            not model.tiles
            or controller.game_over
        ):
            return None

        if not (
            0 <= event.x < canvas_size
            and 0 <= event.y < canvas_size
        ):
            return None

        col = (
            event.x
            * model.grid_size
            // canvas_size
        )

        row = (
            event.y
            * model.grid_size
            // canvas_size
        )

        return (
            row
            * model.grid_size
            + col
        )

    def handle_left_click(event):
        index = get_clicked_tile(
            event
        )

        if index is not None:
            controller.select_tile(
                index
            )

    def handle_right_click(event):
        index = get_clicked_tile(
            event
        )

        if index is not None:
            controller.rotate_tile(
                index
            )

        return "break"

    def handle_shift_click(event):
        index = get_clicked_tile(
            event
        )

        if index is not None:
            controller.flip_tile(
                index
            )

        return "break"

    def bind_mouse_controls():
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

        canvas.bind(
            "<Button-2>",
            handle_right_click
        )

        canvas.bind(
            "<Control-Button-1>",
            handle_right_click
        )

    def handle_hint():
        if model.tiles:
            controller.use_hint()

    def handle_solve():
        if (
            model.tiles
            and controller.solve()
        ):
            lock_puzzle()

    def handle_photo_selected(
        file_path,
        grid_size
    ):
        try:
            controller.start_game(
                file_path,
                grid_size
            )

            view.selected_image_path = (
                file_path
            )

            view.reset_view()

            display_original()

            refresh(
                controller.get_state()
            )

            bind_mouse_controls()

        except (
            ValueError,
            OSError,
            cv2.error
        ) as error:
            messagebox.showerror(
                "Image Error",
                str(error)
            )

    def handle_grid_changed(grid_size):
        if (
            view.selected_image_path
            is not None
        ):
            handle_photo_selected(
                view.selected_image_path,
                grid_size
            )

    controller.on_change = refresh

    controller.on_complete = (
        handle_completion
    )

    view.hint_button.config(
        command=handle_hint
    )

    view.solve_button.config(
        command=handle_solve
    )

    view.on_photo_selected = (
        handle_photo_selected
    )

    view.on_grid_changed = (
        handle_grid_changed
    )

    bind_mouse_controls()

    root.mainloop()


if __name__ == "__main__":
    main()