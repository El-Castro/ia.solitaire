from tkinter import Tk
from FreecellMenu import FreecellMenu

def main():
    """The main function initializes the GUI for the Freecell game. It creates the root window and the FreecellMenu, then starts the Tkinter main loop."""

    # Initialize the game and GUI
    root = Tk()
    FreecellMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()