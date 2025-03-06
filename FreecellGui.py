import tkinter as tk
from tkinter import Canvas

class FreeCellGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("FreeCell Solitaire")
        self.canvas = Canvas(root, width=1000, height=1000, bg="green")
        self.canvas.pack()
        self.card_width = 80
        self.card_height = 120
        self.selected_card = None
        self.selected_column = None
        self.draw_board()

    def draw_board(self):
        # Draw Free Cells
        for i in range(4):
            self.canvas.create_rectangle(50 + i * 100, 50, 130 + i * 100, 130, outline="white", width=2)
            self.canvas.create_text(90 + i * 100, 90, text=f"Free {i+1}", fill="white")
        
        # Draw Foundations
        for i in range(4):
            self.canvas.create_rectangle(450 + i * 100, 50, 530 + i * 100, 130, outline="white", width=2)
            self.canvas.create_text(490 + i * 100, 90, text=f"Found {i+1}", fill="white")
        
        # Draw Tableau Columns
        for i in range(8):
            self.canvas.create_rectangle(50 + i * 100, 200, 130 + i * 100, 280, outline="white", width=2)
            self.canvas.create_text(90 + i * 100, 240, text=f"Col {i+1}", fill="white")
            self.draw_cards(i)

    def draw_cards(self, column_index):
        column = self.game.tableau[column_index]
        for j, card in enumerate(column):
            card_text = f"{card[1]}{card[0][0].upper()}"
            self.canvas.create_text(90 + column_index * 100, 240 + j * 20, text=card_text, fill="black")

    def handle_click(self, event):
        if event.y < 130:  # Clicked on free cells or foundations (not handled yet)
            pass
        elif event.y > 200:  # Clicked on tableau columns
            column_index = (event.x - 50) // 100
            if self.selected_card is None:
                # Select the card if a tableau column is clicked
                if self.game.tableau[column_index]:
                    self.selected_column = column_index
                    self.selected_card = self.game.tableau[column_index][-1]
                    self.canvas.create_text(event.x, event.y, text=f"Selected: {self.selected_card[1]}{self.selected_card[0][0].upper()}", fill="red")
            else:
                # Move the selected card to this column
                if self.selected_column is not None and column_index != self.selected_column:
                    self.game = self.game.apply_move(("tableau_to_tableau", self.selected_column, column_index))
                    self.selected_card = None
                    self.selected_column = None
                self.update_game_state()

    def update_game_state(self):
        self.canvas.delete("all")  # Clear the canvas
        self.draw_board()