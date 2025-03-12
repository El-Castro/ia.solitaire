from tkinter import Tk
from FreecellGui import FreeCellGUI
from FreecellState import FreeCellState

def main():
    # Initialize the game state with random tableau
    game = FreeCellState.create_random_state()

    # Initialize the game and GUI
    root = Tk()
    gui = FreeCellGUI(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()