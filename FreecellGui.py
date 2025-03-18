import tkinter as tk
from tkinter import Canvas, Button
from FreecellState import FreeCellState
import FreecellMove
from Card import Card
from Move import Move
from FreecellAI import solve_game

class FreeCellGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=850, height=600, bg="green")
        self.canvas.pack()
        self.selected = None
        
        self.draw_board()
        
        # Add a button to solve the game using AI
        solve_button = Button(self.root, text="Solve Game", command=self.solve_game)
        solve_button.pack()

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
        """Draws a single card"""
        card_id = self.canvas.create_rectangle(x, y, x+60, y+90, fill="white", outline="black")
        text_id = self.canvas.create_text(x+40, y+15, text=f"{card.rank} {card.suit[0]}", font=("Arial", 12))
        
        # Bind click event
        self.canvas.tag_bind(card_id, "<Button-1>", lambda event: self.handle_click(type, index, isCard))
        self.canvas.tag_bind(text_id, "<Button-1>", lambda event: self.handle_click(type, index, isCard))


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
