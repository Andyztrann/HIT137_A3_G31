# HIT137 Assignment 3 - Group 31

Image Puzzle Game

This project is a Python desktop image puzzle game developed for HIT137 Software Now Assignment 3.

The program loads an image, divides it into a 3x3, 4x4 or 5x5 grid, randomly scrambles the tiles using swaps, rotations and flips, and allows the player to restore the original image.

## Team Members

Vinh - Core Model and Image Processing
Developed the tile and puzzle model, image loading, resizing, padding, splitting and rebuilding functions.

Andy - Controller, Transformations and Gameplay
Developed the transformation classes, scrambling, player actions, hints, Solve logic, completion detection and application integration.

Naro - Tkinter GUI, Visual Feedback and Testing
Developed the Tkinter interface, image canvases, grid display, selection feedback, correct-tile indicators and hint visuals.

## Project Structure

The project follows this structure:

Model / Image Processing
↓
Controller / Gameplay Logic
↓
View / Tkinter GUI

Main files:

```text
HIT137_A3_G31/
├── main.py
├── tile.py
├── puzzle_model.py
├── image_processor.py
├── transformations.py
├── puzzle_controller.py
├── puzzle_view.py
├── test_controller.py
├── test_transformations.py
├── requirements.txt
├── README.md
└── github_link.txt