from tkinter import Tk
#from FreeCellGui import FreeCellGUI
#from FreeCellState import FreeCellState
from FreecellMenu import FreecellMenu

def main():
    #Show the menu 

    # Initialize the game state with random tableau
    #game = FreeCellState.create_random_state()

    # Initialize the game and GUI
    root = Tk()
    menu = FreecellMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()