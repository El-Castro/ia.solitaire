import tkinter as tk
from tkinter import Canvas
from FreecellState import FreeCellState
import FreecellMove
from Card import Card
from Move import Move

class FreeCellGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.canvas = tk.Canvas(root, width=800, height=600, bg="green")
        self.canvas.pack()
        self.selected_card = None  # Store selected card (tuple: (area, index))
        
        self.draw_board()
        
    def draw_board(self):
        self.canvas.delete("all")

        # Draw Free Cells (top-left)
        for i in range(4):
            x, y = 50 + i * 100, 50
            self.canvas.create_rectangle(x, y, x+80, y+100, outline="white", width=2)
            if self.game.free_cells[i]:
                self.draw_card(self.game.free_cells[i], x+10, y+10, area="freecell", index=i)

        # Draw Foundations (top-right)
        for i, suit in enumerate(["hearts", "diamonds", "clubs", "spades"]):
            x, y = 500 + i * 100, 50
            self.canvas.create_rectangle(x, y, x+80, y+100, outline="white", width=2)
            if self.game.foundations[suit]:
                self.draw_card(self.game.foundations[suit][-1], x+10, y+10, area="foundation", index=suit)

        # Draw Tableau (bottom)
        for i, col in enumerate(self.game.tableau):
            x, y = 50 + i * 100, 200
            for j, card in enumerate(col):
                self.draw_card(card, x, y + j * 30, area="tableau", index=(i, j))

    def draw_card(self, card, x, y, area, index):
        """Draws a single card"""
        card_id = self.canvas.create_rectangle(x, y, x+60, y+90, fill="white", outline="black")
        text_id = self.canvas.create_text(x+30, y+45, text=f"{card.rank} {card.suit[0]}", font=("Arial", 12))
        
        # Bind click event
        self.canvas.tag_bind(card_id, "<Button-1>", lambda event: self.handle_click(area, index))
        self.canvas.tag_bind(text_id, "<Button-1>", lambda event: self.handle_click(area, index))

    def handle_click(self, area, index):
        """Handles card selection and moves"""
        if self.selected_card is None:
            self.selected_card = (area, index)
        else:
            src_area, src_index = self.selected_card
            dest_area, dest_index = area, index
            
            # Create Move object
            card = None
            if src_area == "tableau":
                card = self.game.tableau[src_index[0]][-1]
            elif src_area == "freecell":
                card = self.game.free_cells[src_index]
            
            move_type = None
            if src_area == "tableau" and dest_area == "tableau":
                move_type = "tableau_to_tableau"
            elif src_area == "tableau" and dest_area == "freecell":
                move_type = "tableau_to_freecell"
            elif src_area == "freecell" and dest_area == "tableau":
                move_type = "freecell_to_tableau"
            elif src_area == "tableau" and dest_area == "foundation":
                move_type = "tableau_to_foundation"
            elif src_area == "freecell" and dest_area == "foundation":
                move_type = "freecell_to_foundation"

            move = Move(move_type, src_index[0], dest_index[0], card)

            print(f"Selected move: {move}")
            possible_moves = FreecellMove.get_possible_moves(self.game)
            if move in possible_moves:
                self.game = self.game.apply_move(move)
            else:
                print("Move not possible")
            
            # Reset selection and redraw
            self.selected_card = None
            self.draw_board()
