# HIT137 Assignment 3
# Owner: Naro
# Purpose: Tkinter GUI, visual feedback and display updates.
# Actual implementation will be added by Naro.

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PuzzleView:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.root.geometry("1200x750")

        self.grid_size = tk.StringVar(value="3x3")
        self.moves = tk.StringVar(value="Moves: 0")
        self.tiles_left = tk.StringVar(value="Tiles Left: 0")
        self.selected_image_path = None
        self.original_photo = None
        
        self.create_controls()
        self.create_image_area()
        self.draw_grid_lines()
        self.highlight_selected_tile(1, 1)
        
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
        
        hint_button = tk.Button(
            control_frame,
            text="Hint",
            command=self.show_hint
        )
        hint_button.pack(side="left", padx=5)
        
        solve_button = tk.Button(
            control_frame,
            text="Solve",
            command=self.solve_puzzle
        )
        solve_button.pack(side="left", padx=5)
        
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
            bg="lightblue"
        )
        self.original_canvas.grid(row=1, column=0, padx=20, pady=10)
        
        self.puzzle_canvas = tk.Canvas(
            image_frame,
            width=500,
            height=500,
            bg="lightblue"
        )
        self.puzzle_canvas.grid(row=1, column=1, padx=20,pady=10)
    
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
            print("Selected image:", file_path)
            self.display_original_image(file_path)
            
    def display_original_image(self, file_path):
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
    
    
    
    def grid_changed(self, choice):
        self.draw_grid_lines()
        
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
            outline="green",
            width=4,
            tags="selection"
        )
    
    def clear_selection_highlight(self):
        self.puzzle_canvas.delete("selection")
                 
    def show_hint(self):
        print("Hint Clicked")
        
    def solve_puzzle(self):
        print("Solve Clicked")
        
if __name__ == "__main__":
    root = tk.Tk()
    view = PuzzleView(root)
    root.mainloop()

