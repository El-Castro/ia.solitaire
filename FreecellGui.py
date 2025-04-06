import re
import time
import tkinter as tk
from tkinter import Button, PhotoImage
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter
from PIL import Image, ImageTk
import FreecellMove as fcm
from Card import Card
from Move import Move
from FreecellAI import solve_game_astar,solve_game_bfs, solve_game_dfs
from FreecellState import FreecellState
import random


class FreeCellGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.card_images = {}
        self.highlight_id = None
        # Load saved time instead of resetting it
        self.minutes = 0
        self.seconds = 0
        self.setup_ui()


# Initialization / Setup Methods ------------------------------------------------------------------------------------------------------------------------------

    def setup_ui(self):
        """Sets up the user interface for the FreeCell game."""
        self.root.title("FreeCell Solitaire")
        self.canvas = tk.Canvas(self.root, width=950, height=700)
        self.canvas.pack()

        # Load the background image
        self.bg_image = Image.open("assets/table.png")  
        self.bg_image = self.bg_image.resize((950, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Place the image on the canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw") 

        self.selected = None
        self.button_ids = [] 
        self.setup_buttons()

        print(self.game.heuristic())
        fcm.apply_automatic_moves(self.game)
        self.draw_board()
  
    def setup_buttons(self):
        """Creates and places buttons that remain static."""
        self.save_button = Button(self.root, text="Save Game", command=self.save_game)
        self.solve_button = Button(self.root, text="Solve Game", command=self.solve_game)
        self.undo_button = Button(self.root, text="Undo",command=self.undo_move)
        self.hint_button = Button(self.root, text="Hint",command=self.hint_move)
        
        self.start_time = time.time()  # Get the current time
        self.running = True  # Ensure the timer runs
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=("Arial", 14), bg="green", fg="white")
        self.canvas.create_window(950, 7000, window=self.timer_label, width=100, height=35)

        # Place buttons and timer, store their IDs
        self.button_ids = [
            self.canvas.create_window(200, 570, window=self.save_button, width=110, height=35),
            self.canvas.create_window(350, 570, window=self.solve_button, width=110, height=35),
            self.canvas.create_window(500, 570, window=self.undo_button, width=110, height=35),
            self.canvas.create_window(650, 570, window=self.hint_button, width=110, height=35),
            self.canvas.create_window(850, 660, window=self.timer_label, width=120, height=35),
            
        ]
        self.update_timer() 

    def update_timer(self):
        """Updates the timer label every second."""
        if self.running:
            if self.game.minutes != None or self.game.seconds != None:
                elapsed_time = int((self.game.minutes * 60 + self.game.seconds + time.time()) - self.start_time)
            else:
                elapsed_time = int(time.time() - self.start_time)
            
            self.minutes = elapsed_time // 60
            self.seconds = elapsed_time  % 60

            # Update the timer label to reflect the current minutes and seconds
            # If timer_label still exists, update it
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                self.timer_label.config(text=f"Time: {self.minutes:02}:{self.seconds:02}")

            # Schedule the next update after 1000ms (1 second)
            self.timer_after_id = self.root.after(1000, self.update_timer)


# Rendering / Drawing Methods ---------------------------------------------------------------------------------------------------------------------------------

      
    def load_card_image(self, card):
        """Loads and resizes the card image."""
        card_name = f"{card.rank}_of_{card.suit}.png"  # Ensure image filenames match this format
        if card_name not in self.card_images:
            image = Image.open(f"assets/cards/{card_name}")  # Adjust the path to your images
            image = image.resize((60, 90), Image.LANCZOS)  # Resize to fit the card size
            self.card_images[card_name] = ImageTk.PhotoImage(image)
        return self.card_images[card_name]

    def draw_board(self):
        """Draws the game board, including free cells, foundations, and tableau."""
        for item in self.canvas.find_all():
            if item not in self.button_ids:  # Prevent deletion of buttons and timer
                self.canvas.delete(item)
        # Re-add background image after clearing the canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Draw Free Cells
        for i in range(4):
            x, y = 85 + i * 100, 50
            rect_id = self.canvas.create_rectangle(x, y, x+60, y+90, outline="white", width=2, fill="green")
            
            if self.game.free_cells[i]:
                self.draw_card(self.game.free_cells[i], x, y, type="freecell", index=i, isCard=True)
            else:
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="freecell", index=None, isCard=False: self.handle_click(type, index, isCard))

        # Draw Foundations
        for i, suit in enumerate(["hearts", "diamonds", "clubs", "spades"]):
            x, y = 485 + i * 100, 50
            rect_id = self.canvas.create_rectangle(x, y, x+60, y+90, outline="white", width=2, fill="green")
            
            match suit:
                case "hearts":
                    text_id = self.canvas.create_text(x+30, y+40, text=f"♥", font=("Arial", 35), fill="white")
                case "diamonds":
                    text_id = self.canvas.create_text(x+30, y+40, text=f"♦", font=("Arial", 35), fill="white")
                case "clubs":
                    text_id = self.canvas.create_text(x+30, y+40, text=f"♣", font=("Arial", 35), fill="white")
                case "spades":
                    text_id = self.canvas.create_text(x+30, y+40, text=f"♠", font=("Arial", 35), fill="white")

            if self.game.foundations[suit]:
                self.draw_card(Card(self.game.foundations[suit], suit), x, y, type="foundation", index=suit, isCard=True)
            else:
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="foundation", index=suit, isCard=False: self.handle_click(type, index, isCard))
                self.canvas.tag_bind(text_id, "<Button-1>", lambda event, type="foundation", index=suit, isCard=False: self.handle_click(type, index, isCard))

        # Draw Tableau
        for i, col in enumerate(self.game.tableau):  
            x, y = 85 + i * 100, 200
            rect_id = self.canvas.create_rectangle(x, y, x+60, y+300, outline="white", width=2, fill="green")

            for j, card in enumerate(col):  
                self.draw_card(card, x, y + j * 30, type="tableau", index=i, isCard=True)

            if not col:
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="tableau", index=i, isCard=False: self.handle_click(type, index, isCard))

    def draw_card(self, card, x, y, type, index, isCard):
        """Draws a card at the specified position."""
        image = self.load_card_image(card)
        img_id = self.canvas.create_image(x + 30, y + 45, image=image, anchor="center")  # Center the image

        # Bind click event to the card
        self.canvas.tag_bind(img_id, "<Button-1>", lambda event: self.handle_click(type, index, isCard))


# Interaction Methods -----------------------------------------------------------------------------------------------------------------------------------------


    def handle_click(self, type, index, isCard):
        """Handles click events on cards and empty slots."""

        if self.selected != None and self.selected[0] == "freecell" and type == "freecell":
            print("Freecell to Freecell move is irrelevant.")
            self.selected = None
            self.remove_highlight()
        elif self.selected != None and self.selected[0] == "foundation" and type == "foundation":
            print("Foundation to Foundation move is irrelevant.")
            self.selected = None
            self.remove_highlight()
        elif self.selected is None and isCard:
            self.selected = (type, index)

            # Highlight the selected card
            card_x, card_y = self.get_card_position(type, index)
            self.highlight_card(card_x, card_y)

        else:
            src_type, src_index = self.selected
            dest_type, dest_index = type, index
            
            # Create Move object            
            move_type = None
            if src_type == "tableau" and dest_type == "tableau":
                move_type = "tableau_to_tableau"
            elif src_type == "tableau" and dest_type == "freecell":
                move_type = "tableau_to_freecell"
            elif src_type == "freecell" and dest_type == "tableau":
                move_type = "freecell_to_tableau"
            elif src_type == "tableau" and dest_type == "foundation":
                move_type = "tableau_to_foundation"
            elif src_type == "freecell" and dest_type == "foundation":
                move_type = "freecell_to_foundation"
            elif src_type == "foundation" and dest_type == "freecell":
                move_type = "foundation_to_freecell"
            elif src_type == "foundation" and dest_type == "tableau":
                move_type = "foundation_to_tableau"        
            move = Move(move_type, src_index, dest_index)

            print(f"Selected move: {move}")
            possible_moves = fcm.get_possible_moves(self.game)
            if move in possible_moves:
                self.game = self.game.apply_move(move)
                fcm.apply_automatic_moves(self.game)
                self.game.heuristic()
            else: 
                print("Move not possible")

            # Reset selection and redraw
            self.selected = None
            self.remove_highlight()
            self.draw_board()
            self.game.heuristic()

            if self.game.is_solved() : self.winning_state()

    def highlight_card(self, x, y):
        """Draws a highlight rectangle around the selected card."""
        self.remove_highlight()  # Remove previous highlight if exists
        self.highlight_id = self.canvas.create_rectangle(
            x, y, x+60, y+90, outline="yellow", width=4
        )

    def remove_highlight(self):
        """Removes the highlight rectangle."""
        if self.highlight_id:
            self.canvas.delete(self.highlight_id)
            self.highlight_id = None

    def get_card_position(self, type, index):
        """Returns the x, y position of a card based on its type and index."""
        if type == "freecell":
            return (85 + index * 100, 50)  # Adjusted x-coordinate to match draw_board
        elif type == "foundation":
            foundation_map = {"hearts": 0, "diamonds": 1, "clubs": 2, "spades": 3}
            return (485 + foundation_map[index] * 100, 50)  # Adjusted x-coordinate to match draw_board
        elif type == "tableau":
            column = self.game.tableau[index]
            return (85 + index * 100, 200 + (len(column) - 1) * 30)
        return (0, 0)  # Default value if type is unknown


# Game Control Methods ----------------------------------------------------------------------------------------------------------------------------------------        

    def winning_state(self):
        """Displays a pop-up message saying the game is over."""
        try:
            messagebox.showinfo("Game Over", "Game Solved 🎉")
        except Exception as e:
            print(f"Error showing messagebox: {e}")

    def hint_move(self):
        #get possible free moves for the current state 
        possible_moves = FreecellState.get_possible_moves(self.game)
        if not possible_moves:
            tkinter.messagebox.showinfo("Hint", "No available moves at the moment.")
            return
        #print(possible_moves)
        list_size = len(possible_moves)
        random_index = random.randrange(1, list_size)
        #get ramdon move
        hint_move = possible_moves[random_index]
        move_type = hint_move.move_type

        if move_type == "tableau_to_foundation":
            hint_msg = f"Move a card from Tableau {hint_move.source} to Foundation {hint_move.suit}."
        elif move_type == "tableau_to_freecell":
            hint_msg = f"Move a card from Tableau {hint_move.source} to a Freecell."
        elif move_type == "freecell_to_foundation":
            hint_msg = f"Move a card from Freecell {hint_move.source} to Foundation {hint_move.suit}."
        elif move_type == "tableau_to_tableau":
            hint_msg = f"Move a card from Tableau {hint_move.source} to Tableau {hint_move.destination}."
        elif move_type == "freecell_to_tableau":
            hint_msg = f"Move a card from Freecell {hint_move.source} to Tableau {hint_move.destination}."
        elif move_type == "foundation_to_tableau":
            hint_msg = f"Move a card from Foundation {hint_move.source} to Tableau {hint_move.destination}."
        elif move_type == "foundation_to_freecell":
            hint_msg = f"Move a card from Foundation {hint_move.source} to a Freecell."
        else:
            hint_msg = "No valid moves found."

        tkinter.messagebox.showinfo("Hint", hint_msg)

    def undo_move(self):
        """Undoes the last move and redraws the board."""
        self.game.undo()
        self.draw_board()
        print("Undo")

    def save_game(self):
        """Stops the timer and saves the game."""
        if hasattr(self, 'timer_after_id'):
            self.game.minutes = self.minutes
            self.game.seconds = self.seconds
            print(f"Saving time: {self.minutes} minutes, {self.seconds} seconds")
            self.running = False  # Stop the timer
            self.root.after_cancel(self.timer_after_id)
        FreecellState.save_to_file(self.game, "saved_game.json")
        print("Game saved successfully!")
    
    def solve_game(self):
        self.title_id = self.canvas.create_text(450, 610, text="Choose an algorithm to solve the game", font=("Helvetica", 15), fill="white")
    
        self.solve_button_AI = Button(self.root, text="A*", command=self.solve_game_AI)
        self.solve_button_BFS = Button(self.root, text="BFS", command=self.solve_game_bfs)
        self.solve_button_DFS = Button(self.root, text="DFS", command=self.solve_game_dfs)

        # Store canvas windows IDs
        self.solve_button_AI_id = self.canvas.create_window(280, 650, window=self.solve_button_AI, width=110, height=35)
        self.solve_button_BFS_id = self.canvas.create_window(430, 650, window=self.solve_button_BFS, width=110, height=35)
        self.solve_button_DFS_id = self.canvas.create_window(580, 650, window=self.solve_button_DFS, width=110, height=35)

                            
    def solve_game_AI(self):
        if self.hide_solver_ui():
            self.root.after(100, self.solve_game_AI_2)

    def solve_game_bfs(self):
        if self.hide_solver_ui():
            self.root.after(100, self.solve_game_bfs_2)

    def solve_game_dfs(self):
        if self.hide_solver_ui():
            self.root.after(100, self.solve_game_dfs_2)

    def solve_game_AI_2(self):
        result = solve_game_astar(self.game)
        if result is not None:
            print("Game solved by A Star!")
            for move in result:
                if isinstance(move, str) and move.startswith("Supermove"):  # Supermove string
                    # Parse and extract the details from the string
                    match = re.match(r"Supermove\(source=(\d+), destination=(\d+), number of cards=(\d+)\)", move)
                    if match:
                        src = int(match.group(1))
                        dest = int(match.group(2))
                        num_cards = int(match.group(3))
                        self.game = fcm.execute_supermove(self.game, src, dest, num_cards)
                else:  # Regular atomic move
                    self.game = self.game.apply_move(move)
                    
                self.game = fcm.apply_automatic_moves(self.game)
                self.draw_board()
                self.root.update_idletasks()
                time.sleep(0.5)  # Add a delay to visualize the moves
            self.winning_state()  # Call the method to remove buttons and display message
        else:
            print("A Star could not solve the game.")

    def solve_game_bfs_2(self):
        result = solve_game_bfs(self.game)
        if result is not None:
            print("Game solved by BFS!")
            for move in result:
                if isinstance(move, str) and move.startswith("Supermove"):  # Supermove string
                    # Parse and extract the details from the string
                    match = re.match(r"Supermove\(source=(\d+), destination=(\d+), number of cards=(\d+)\)", move)
                    if match:
                        src = int(match.group(1))
                        dest = int(match.group(2))
                        num_cards = int(match.group(3))
                        self.game = fcm.execute_supermove(self.game, src, dest, num_cards)
                else:  # Regular atomic move
                    self.game = self.game.apply_move(move)
                    
                self.game = fcm.apply_automatic_moves(self.game)
                self.draw_board()
                self.root.update_idletasks()
                time.sleep(0.5)  # Add a delay to visualize the moves
            self.winning_state()  # Call the method to remove buttons and display message
        else:
            print("BFS could not solve the game.")

    def solve_game_dfs_2(self):
        result = solve_game_dfs(self.game)
        if result is not None:
            print("Game solved by DFS!")
            for move in result:
                if isinstance(move, str) and move.startswith("Supermove"):  # Supermove string
                    # Parse and extract the details from the string
                    match = re.match(r"Supermove\(source=(\d+), destination=(\d+), number of cards=(\d+)\)", move)
                    if match:
                        src = int(match.group(1))
                        dest = int(match.group(2))
                        num_cards = int(match.group(3))
                        self.game = fcm.execute_supermove(self.game, src, dest, num_cards)
                else:  # Regular atomic move
                    self.game = self.game.apply_move(move)
                    
                self.game = fcm.apply_automatic_moves(self.game)
                self.draw_board()
                self.root.update_idletasks()
                time.sleep(0.5)  # Add a delay to visualize the moves
            self.winning_state()  # Call the method to remove buttons and display message
        else:
            print("DFS could not solve the game.")
    
    def hide_solver_ui(self):
        """Attempts to remove solver UI buttons and returns True if successful."""
        try:
            self.solve_button_AI.destroy()
            self.solve_button_BFS.destroy()
            self.solve_button_DFS.destroy()

            self.canvas.delete(self.solve_button_AI_id)
            self.canvas.delete(self.solve_button_BFS_id)
            self.canvas.delete(self.solve_button_DFS_id)
            self.canvas.delete(self.title_id)

            return True  # All deletions succeeded
        except Exception as e:
            print(f"Error while hiding solver UI: {e}")
            return False  # Something went wrong
        
    def return_to_main_menu(self):
        from FreecellMenu import FreecellMenu  # Avoid circular import at top level

        for widget in self.root.winfo_children():
            widget.destroy()
        
        FreecellMenu.setup_menu(self)

        

        
        






