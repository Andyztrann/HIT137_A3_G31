# HIT137 Assignment 3
# Owner: Naro
# Purpose: Tkinter GUI, visual feedback and display updates.
# Actual implementation will be added by Naro.

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError

#Main GUI for puzzle game
class PuzzleView:
    # Set up main window and GUI components
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.root.geometry("1200x750")

        self.grid_size = tk.StringVar(value="3x3")
        self.moves = tk.StringVar(value="Moves: 0")
        self.tiles_left = tk.StringVar(value="Tiles Left: 0")
        self.selected_image_path = None
        self.original_photo = None
        self.puzzle_photo = None
       
        
        self.create_controls()
        self.create_image_area()
        self.draw_grid_lines()
        self.set_hint_enabled(False)
    
    # Create control area grid size, buttons and counters    
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        grid_label = tk.Label(control_frame, text="Grid Size")
        grid_label.pack(side="left", padx=5)
        
        grid_menu = tk.OptionMenu(
            control_frame,
            self.grid_size,
            "3x3",
            "4x4",
            "5x5",
            command=self.grid_changed
        )
        
        grid_menu.pack(side="left", padx=5)
        select_button = tk.Button(
            control_frame,
            text="Select Photo",
            command=self.select_photo
        )
        select_button.pack(side="left", padx=5)
        
        self.hint_button = tk.Button(
            control_frame,
            text="Hint",
            command=self.show_hint
        )
        self.hint_button.pack(side="left", padx=5)
        
        self.solve_button = tk.Button(
            control_frame,
            text="Solve",
            command=self.solve_puzzle
        )
        self.solve_button.pack(side="left", padx=5)
        
        moves_label = tk.Label(
            control_frame,
            textvariable=self.moves
        )
        moves_label.pack(side="left", padx=15)
        
        tiles_label = tk.Label(
            control_frame,
            textvariable=self.tiles_left
        )
        tiles_label.pack(side="left", padx=5)
    
    # Create two canvas
    def create_image_area(self):
        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=20)
        
        original_label = tk.Label(
            image_frame,
            text="Original Image",
            font=("Arial", 14, "bold")
        )
        original_label.grid(row=0,column=0, padx=20)
        
        puzzle_label = tk.Label(
            image_frame,
            text="Puzzle Image",
            font=("Arial", 14, "bold")
        )
        puzzle_label.grid(row=0,column=1, padx=20)
        
        self.original_canvas = tk.Canvas(
            image_frame,
            width=500,
            height=500,
            bg="lightgrey"
        )
        self.original_canvas.grid(row=1, column=0, padx=20, pady=10)
        
        self.puzzle_canvas = tk.Canvas(
            image_frame,
            width=500,
            height=500,
            bg="lightgrey"
        )
        self.puzzle_canvas.grid(row=1, column=1, padx=20,pady=10)
        self.puzzle_canvas.bind("<Button-1>", self.puzzle_left_click)
        self.puzzle_canvas.bind("<Button-3>", self.puzzle_right_click)
        self.puzzle_canvas.bind("<Shift-Button-1>", self.puzzle_shift_click)
    
    
    # Open file dialog    
    def select_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp")
            ]
        )
        if file_path:
            self.selected_image_path = file_path

            self.reset_view()

            print("Selected image:", file_path)

            if self.display_original_image(file_path):
                self.set_hint_enabled(True)
    
    # Display the selected image            
    def display_original_image(self, file_path):
        try:
            image = Image.open(file_path)

            image.thumbnail((500, 500))

            self.original_photo = ImageTk.PhotoImage(image)

            self.original_canvas.delete("all")

            self.original_canvas.create_image(
                250,
                250,
                image=self.original_photo,
                anchor="center"
            )
            
            return True
            
        except (UnidentifiedImageError, OSError):
            messagebox.showerror(
                "Invalid Image",
                "The selected file could not be opened as an image."
            )

            return False

    # Draw grid lines on the puzzle canvas
    def draw_grid_lines(self):
        self.puzzle_canvas.delete("grid_line")

        grid_number = int(self.grid_size.get()[0])
        tile_size = 500 / grid_number

        for i in range(1, grid_number):
            position = i * tile_size

            self.puzzle_canvas.create_line(
                position, 0,
                position, 500,
                fill="gray",
                width=1,
                tags="grid_line"
            )

            self.puzzle_canvas.create_line(
                0, position,
                500, position,
                fill="gray",
                width=1,
                tags="grid_line"
            )
    
    # Refresh puzzle and clear previous visual 
    def grid_changed(self, choice):
        self.clear_selection_highlight()
        self.clear_correct_ticks()
        self.clear_hint_circles()
        self.draw_grid_lines()
    
    # Draw a red border around the puzzle tile   
    def highlight_selected_tile(self, row, column):
        self.puzzle_canvas.delete("selection")

        grid_number = int(self.grid_size.get()[0])
        tile_size = 500 / grid_number

        x1 = column * tile_size
        y1 = row * tile_size
        x2 = x1 + tile_size
        y2 = y1 + tile_size

        self.puzzle_canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline="red",
            width=4,
            tags="selection"
        )
    
    # Remove the selected tile border
    def clear_selection_highlight(self):
        self.puzzle_canvas.delete("selection")
    
    # Display a green tick on a tile
    def draw_correct_tick(self, row, column):
        grid_number = int(self.grid_size.get()[0])
        tile_size = 500 / grid_number

        x = (column + 1) * tile_size - 15
        y = row * tile_size + 15

        self.puzzle_canvas.create_text(
            x,
            y,
            text="✓",
            fill="green",
            font=("Arial", 18, "bold"),
            tags="correct_tick"
        )
    
    # Remove all green correct-tile ticks from the puzzle
    def clear_correct_ticks(self):
        self.puzzle_canvas.delete("correct_tick")
    
    # Draw blue hint circles on the current tile
    def draw_hint_circles(self, current_row, current_column,
                      home_row, home_column):

        self.clear_hint_circles()

        grid_number = int(self.grid_size.get()[0])
        tile_size = 500 / grid_number

        current_x = current_column * tile_size + tile_size / 2
        current_y = current_row * tile_size + tile_size / 2

        home_x = home_column * tile_size + tile_size / 2
        home_y = home_row * tile_size + tile_size / 2

        radius = 15

        self.puzzle_canvas.create_oval(
            current_x - radius,
            current_y - radius,
            current_x + radius,
            current_y + radius,
            outline="blue",
            width=3,
            tags="hint_circle"
        )

        self.original_canvas.create_oval(
            home_x - radius,
            home_y - radius,
            home_x + radius,
            home_y + radius,
            outline="blue",
            width=3,
            tags="hint_circle"
        )
        
    # Remove the blue hint circles    
    def clear_hint_circles(self):
        self.puzzle_canvas.delete("hint_circle")
        self.original_canvas.delete("hint_circle") 
    
    # Update the number of moves shown on the GUI
    def update_moves(self, move_count):
        self.moves.set(f"Moves: {move_count}")

    # Update the number of incorrect tiles remaining
    def update_tiles_left(self, count):
        self.tiles_left.set(f"Tiles Left: {count}")
    
    # Reset counters and visual feedback when starting a new puzzle
    def reset_view(self):
        self.update_moves(0)
        self.update_tiles_left(0)
        self.set_hint_enabled(False)
        
        self.clear_selection_highlight()
        self.clear_correct_ticks()
        self.clear_hint_circles()

        self.puzzle_canvas.delete("all")
        self.draw_grid_lines()

        self.enable_puzzle_input()
    
    # Display the transformed puzzle image on the puzzle canvas    
    def display_puzzle_image(self, image):
        image.thumbnail((500, 500))

        self.puzzle_photo = ImageTk.PhotoImage(image)

        self.puzzle_canvas.delete("all")

        self.puzzle_canvas.create_image(
            250,
            250,
            image=self.puzzle_photo,
            anchor="center"
        )

        self.draw_grid_lines()
    
    # Detect a normal left click on the puzzle canvas
    def puzzle_left_click(self, event):
        print("Left click:", event.x, event.y)

    # Detect a right click on the puzzle canvas
    def puzzle_right_click(self, event):
        print("Right click:", event.x, event.y)

    # Detect Shift + left click on the puzzle canvas
    def puzzle_shift_click(self, event):
        print("Shift + left click:", event.x, event.y)
        return "break"
    
    # Stop the player from interacting with the puzzle canvas
    def disable_puzzle_input(self):
        self.puzzle_canvas.unbind("<Button-1>")
        self.puzzle_canvas.unbind("<Button-3>")
        self.puzzle_canvas.unbind("<Shift-Button-1>")

    # Allow puzzle mouse controls to work again
    def enable_puzzle_input(self):
        self.puzzle_canvas.bind("<Button-1>", self.puzzle_left_click)
        self.puzzle_canvas.bind("<Button-3>", self.puzzle_right_click)
        self.puzzle_canvas.bind("<Shift-Button-1>", self.puzzle_shift_click)
    
    # Temporary Hint button action until it is connected to the controller               
    def show_hint(self):
        print("Hint Clicked")
    
    # Temporary Solve button action until it is connected to the controller    
    def solve_puzzle(self):
        print("Solve Clicked")
    
    # Enable or disable the Hint button    
    def set_hint_enabled(self, enabled):
        if enabled:
            self.hint_button.config(state="normal")
        else:
            self.hint_button.config(state="disabled")
    
    # Show a message box when the player completes the puzzle
    def show_completion_message(self):
        messagebox.showinfo(
            "Puzzle Complete",
            "Congratulations! You completed the puzzle."
    )       

# Run this file directly for standalone GUI testing            
if __name__ == "__main__":
    root = tk.Tk()
    view = PuzzleView(root)
    root.mainloop()

