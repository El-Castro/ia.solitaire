import tkinter as tk
from tkinter import Button, PhotoImage
from PIL import Image, ImageTk
from FreecellState import FreeCellState
import FreecellMove
from Card import Card
from Move import Move
from FreecellAI import solve_game

class FreeCellGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.card_images = {}
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=850, height=600, bg="green")
        self.canvas.pack()
        self.selected = None
        
        self.draw_board()
        
        # Add a button to solve the game using AI
        solve_button = Button(self.root, text="Solve Game", command=self.solve_game)
        solve_button.pack()

    def load_card_image(self, card):
        """Loads and resizes the card image"""
        card_name = f"{card.rank}_of_{card.suit}.png"  # Ensure image filenames match this format
        if card_name not in self.card_images:
            image = Image.open(f"assets/cards/{card_name}")  # Adjust the path to your images
            image = image.resize((60, 90), Image.LANCZOS)  # Resize to fit the card size
            self.card_images[card_name] = ImageTk.PhotoImage(image)
        return self.card_images[card_name]


    def draw_board(self):
        self.canvas.delete("all")

        # Draw Free Cells
        for i in range(4):
            x, y = 50 + i * 100, 50
            rect_id = self.canvas.create_rectangle(x, y, x+60, y+90, outline="white", width=2, fill="green")
            
            if self.game.free_cells[i]:
                self.draw_card(self.game.free_cells[i], x, y, type="freecell", index=i, isCard=True)
            else:
                # Bind click event to empty FreeCell
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="freecell", index=None, isCard=False: self.handle_click(type, index, isCard))

        # Draw Foundations
        for i, suit in enumerate(["hearts", "diamonds", "clubs", "spades"]):
            x, y = 450 + i * 100, 50
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
                self.draw_card(Card(self.game.foundations[suit],suit), x, y, type="foundation", index=suit, isCard=True)
            else:
                # Bind click event to empty Foundation
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="foundation", index=suit, isCard=False: self.handle_click(type, index, isCard))

        # Draw Tableau
        for i, col in enumerate(self.game.tableau): # i-> num column
            x, y = 50 + i * 100, 200
            rect_id = self.canvas.create_rectangle(x, y, x+60, y+300, outline="white", width=2, fill="green")
            
            for j, card in enumerate(col): # j-> num card
                self.draw_card(card, x, y + j * 30, type="tableau", index=i, isCard=True)

            if not col:
                # Bind click event to empty Tableau column
                self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, type="tableau", index=i, isCard=False: self.handle_click(type, index, isCard))


    def draw_card(self, card, x, y, type, index, isCard):


        image = self.load_card_image(card)
        img_id = self.canvas.create_image(x + 30, y + 45, image=image, anchor="center")  # Center the image

        # Bind click event to the card
        self.canvas.tag_bind(img_id, "<Button-1>", lambda event: self.handle_click(type, index, isCard))


    def handle_click(self, type, index, isCard):
        print(type)
        print(index)
        """Handles card selection and moves"""
        if self.selected!=None and self.selected[0]=="freecell" and type=="freecell":
            print("Freecell to Freecell move is irrelevant.")
        elif self.selected is None and isCard:
                self.selected = (type, index)
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
            possible_moves = FreecellMove.get_possible_moves(self.game)
            if move in possible_moves:
                self.game = self.game.apply_move(move)
            else: print("Move not possible")
            
            # Reset selection and redraw
            self.selected = None
            self.draw_board()

    def solve_game(self):
        if solve_game(self.game):
            print("Game solved by AI!")
        else:
            print("AI could not solve the game.")
