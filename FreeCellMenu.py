import tkinter as tk
import os
import json
from tkinter import Button
from PIL import Image, ImageTk
from FreeCellState import FreecellState
from FreeCellGui import FreeCellGUI

class FreecellMenu:
    def __init__(self, root):
        self.root = root
        self.setup_menu()

    def setup_menu(self):
        self.canvas = tk.Canvas(self.root, width=850, height=600)
        self.canvas.pack()

        # Load the background image (same as game UI)
        self.bg_image = Image.open("assets/board.jpg")  
        self.bg_image = self.bg_image.resize((850, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create Buttons
        button_font = ("Arial", 14, "bold")

        self.new_game_button = Button(self.root, text="Start New Game", font=button_font, bg="lightgrey", command=self.start_new_game)
        self.load_game_button = Button(self.root, text="Load Saved Game", font=button_font, bg="lightgrey", command=self.load_game)
        self.exit_button = Button(self.root, text="Exit", font=button_font, bg="lightgrey", command=self.exit_game)

        # Place buttons in the center of the screen
        self.canvas.create_window(425, 200, window=self.new_game_button, width=200, height=50)
        self.canvas.create_window(425, 270, window=self.load_game_button, width=200, height=50)
        self.canvas.create_window(425, 340, window=self.exit_button, width=200, height=50)

    def start_new_game(self):
        print("Starting a new game...")
        #update the state for a random shuffle
        game = FreecellState.create_random_state()
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        FreeCellGUI(self.root, game)

    def load_game(self):
        print("Loading saved game...")
        try:
            # Load saved game state
            game = FreecellState.load_from_file('saved_game.json')
            for widget in self.root.winfo_children():
                widget.destroy()
            FreeCellGUI(self.root, game)

        except FileNotFoundError:
            print("Error: presets.json not found!")
        except json.JSONDecodeError:
            print("Error: presets.json is not properly formatted.")

    def exit_game(self):
        self.root.quit()


