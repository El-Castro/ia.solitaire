from tkinter import Tk
from FreecellGui import FreeCellGUI
from FreecellGame import FreeCell  # Import FreeCell class
import random  # Import random module

def main():
    # Initialize the game state with random tableau
    tableau = [[] for _ in range(8)]
    deck = [('hearts', i) for i in range(1, 14)] + [('diamonds', i) for i in range(1, 14)] + \
           [('clubs', i) for i in range(1, 14)] + [('spades', i) for i in range(1, 14)]
    random.shuffle(deck)
    for i in range(4):
        tableau[i] = [deck.pop() for _ in range(7)]  # Distribute 7 cards to first 4 columns
    for i in range(4, 8):
        tableau[i] = [deck.pop() for _ in range(6)]  # Distribute 6 cards to last 4 columns

    game = FreeCell(tableau)
    root = Tk()
    gui = FreeCellGUI(root, game)
    gui.canvas.bind("<Button-1>", gui.handle_click)  # Binding click event
    root.mainloop()

if __name__ == "__main__":
    main()