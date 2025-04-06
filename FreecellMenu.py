import tkinter as tk
import os
import json
from tkinter import Button
from PIL import Image, ImageTk
from FreecellState import FreecellState
from FreecellGui import FreeCellGUI

class FreecellMenu:
    def __init__(self, root):
        """Initialize the FreecellMenu with the given root window."""
        self.root = root
        self.setup_menu()

    def setup_menu(self):
        """Set up the main menu interface."""
        self.root.title("FreeCell Solitaire")
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

        self.new_game_button = Button(self.root, text="Start New Game", font=button_font, bg="lightgrey", command=self.new_game_menu)
        self.load_game_button = Button(self.root, text="Load Saved Game", font=button_font, bg="lightgrey", command=self.load_game)
        self.exit_button = Button(self.root, text="Exit", font=button_font, bg="lightgrey", command=self.exit_game)

        # Place buttons in the center of the screen
        self.canvas.create_window(425, 200, window=self.new_game_button, width=200, height=50)
        self.canvas.create_window(425, 270, window=self.load_game_button, width=200, height=50)
        self.canvas.create_window(425, 340, window=self.exit_button, width=200, height=50)

    def load_game(self):
        """Load a saved game state."""
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
        """Exit the game."""
        self.root.quit()
    
    def new_game_menu(self):
        """Display the new game menu."""
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create buttons
        button_font = ("Arial", 14, "bold")

        self.random_game_button = Button(self.root, text="Random Game", font=button_font, bg="lightgrey", command=self.start_random_game)
        self.preset_game_button = Button(self.root, text="Preset Game", font=button_font, bg="lightgrey", command=self.preset_game_options)
        self.back_button = Button(self.root, text="Back", font=button_font, bg="lightgrey", command=self.back_button)

        self.canvas.create_window(220, 270, window=self.random_game_button, width=150, height=50)
        self.canvas.create_window(420, 270, window=self.preset_game_button, width=150, height=50)
        self.canvas.create_window(620, 270, window=self.back_button, width=150, height=50)
    
    def start_random_game(self):
        """Update a window for a new game with random option."""
        game = FreecellState.create_random_state()
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        FreeCellGUI(self.root, game)
    
    def preset_game_options(self):
        """Load presets and dynamically creates buttons for each preset."""
        print("Loading Preset Menu")
        try:
            # Load saved presets
            presets = FreecellState.load_presets('presets.json')

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
            button_font = ("Arial", 10, "bold")
            padding = 0 

            for preset in presets:
                padding +=1  
                preset_name= preset["name"]

                btn = Button(self.root, text=preset_name, font=button_font, bg="lightgrey",
                         command=lambda p=preset: self.start_game(p))  
                # Add button to canvas
                self.canvas.create_window(padding * 125, 270, window=btn, width=110, height=50)

            #back button to the menu
            self.back_to_menu = Button(self.root, text="Back to Menu", font=button_font, bg="lightgrey", command=self.back_to_menu)
            self.canvas.create_window(440, 400, window=self.back_to_menu, width=150, height=50)

        except FileNotFoundError:
            print("Error: presets.json not found!")
        except json.JSONDecodeError:
            print("Error: presets.json is not properly formatted.")

    def start_game(self, preset):
        """Start the game with the selected preset."""
        game = FreecellState.create_from_preset(preset)

        for widget in self.root.winfo_children():
            widget.destroy()

        FreeCellGUI(self.root, game)
    
    def back_button(self):
        """Back button."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_menu()
    
    #duplicated function cause python does not allow to use the same 
    def back_to_menu(self):
        """Go back to the menu."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_menu()
    









