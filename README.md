# 🃏 FreeCell Solitaire - AI Project

## Group T03G08

**Afonso Castro** @up202208026  
**Fernando Rodrigues** @up201105620  
**Sofia Bliznyuk** @up202209448

## Project Overview

![Game Screenshot](assets/screenshot.png)

This project implements the classic FreeCell Solitaire game using Python and Tkinter's graphical interface.
This game comes combined with AI search algorithms like **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, and **A Star with heuristics**, in order to solve the game automatically.


## Requirements

Make sure you have the following installed:
- Python 3.10 or higher
- Tkinter (usually comes with Python)
- Standard Python libraries used (time, random, json, PIL, etc.)


## How to Run

No compilation is necessary since it's written in Python.

To run the game, run the command:

```python3 main.py```

Or just run it using your IDE's way of running the main.py file.

This will open the game's GUI, where you can play the game and perform all the actions.

## How to Play

FreeCell is a solitaire card game played using a standard 52-card deck. The goal is to move all the cards to the four foundation piles (one for each suit), starting from Ace up to King.

### Game Interface

The game window opens with:
- 8 Tableau columns (where cards are initially dealt)
- 4 FreeCells (temporary storage for one card each)
- 4 Foundation piles (where you build each suit in order)

### Game Rules

- You can move cards between tableau columns as long as they follow descending order and alternate colors (e.g., red 7 on black 8).
- You can place one card at a time into a free cell.
- Cards from the tableau or free cells can be moved to the foundation piles in ascending order by suit.

### Controls

- Click on a card to select it.
- Click on a destination (another tableau column, free cell, or foundation) to move the selected card (if it's possible).
- The game applies automatic moves to the foundation when possible.




