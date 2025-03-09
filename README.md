# FreeCell Solitaire - AI Project

## Group T03G08

**Afonso Castro** @up202208026  
**Fernando Rodrigues** @up201105620
**Sofia Bliznyuk** @up202209448  

---

## 1. **Work Specification**

Freecell Solitaire is a card-based puzzle game played with a standard deck of 52 playing cards.

### Game Components

Tableau (Columns): Eight columns where cards are placed in descending order and alternating colors. The first four columns contain seven cards each, while the last four contain six cards each at the start of the game.
Freecells: Four temporary storage spaces for individual cards that can be used strategically to maneuver other cards.
Foundation Piles: Four piles, one for each suit (Hearts, Diamonds, Clubs, and Spades), where cards must be stacked in ascending order from Ace to King.

### Game Rules

Any card at the top of a column or in a Freecell can be moved.
A card can be placed on another column if it follows descending order and alternates in color (e.g., a red 7 can be placed on a black 8).
A card can be moved to an empty Freecell as a temporary holding space, but only one card per Freecell is allowed.
A card can be moved to the foundation if it follows the correct ascending order for its suit (e.g., Ace of Spades first, then 2 of Spades, etc.).
The game is won when all 52 cards are placed in the foundation Piles in the correct order.

## 2. **Related Work**

...

---

## 3. **Problem Formulation**

In order to formulate this game as a search problem, we can break it apart in its various details.
In terms of State Representation, we can represent the game state as a tuple consisting of its components mentioned before:

Tableau: List of 8 columns, each column being a list of cards, where each card is a tuple of (suit, rank).
Free Cells: A list of 4 free cells. Each free cell can either contain a card or be empty (None).
Foundations: A dictionary where each key is a suit (hearts, diamonds, clubs, spades) and the value is a list representing the foundation of that suit (ordered from the Ace to the King).

So in the end, we have (state) = (tableau, free_cells, foundations).

The initial state represents the starting configuration of the game where the tableau is populated with randomly shuffled cards forming four columns of 7 and four columns of 6, the free cells are empty (None), and the foundations are also empty.

tableau = [shuffled deck of cards]
free_cells = [None, None, None, None]
foundations = {'hearts': [], 'diamonds': [], 'clubs': [], 'spades': []}

This being a card game, the objective test checks if the current state represents a solved/finished game.
The game is considered to have concluded if all the foundations contain exactly 13 cards (one for each rank in each suit) in the correct order (Ace to King).

all(len(self.foundations[suit]) == 13 for suit in self.foundations

The possible actions (operators) the player can perform during the game in order to progress in it consist of the following:

- Move from tableau to foundation.
  - Preconditions: The top card in a tableau column must be able to be placed on the corresponding foundation of the corresponding suit (either the foundation is empty and the card is the Ace, or the top card of the foundation is one rank less than the card to be moved).
  - Effects: The card is removed from the tableau column and added to the corresponding foundation.

- Move from tableau to freecell.
  - Preconditions: A tableau column must have at least one card, and there must be an empty free cell.
  - Effects: The card is moved from the tableau to the free cell.

- Move from freecell to foundation.
  - Preconditions: The free cell must contain a card that can be placed on the foundation (similar to the tableau to foundation move).
  - Effects: The card is removed from the free cell and added to the foundation.

- Move from tableau to tableau.
  - Preconditions: A tableau column must have a card that can be placed on another tableau column (following the descending order of alternating colors rule).
  - Effects: The card is moved from one tableau column to another.

- Move from freecell to tableau.
  - Preconditions: The free cell must contain a card that can be placed on a tableau column (following the descending order of alternating colors rule).
  - Effects: The card is removed from the free cell and added to the tableau column.

- Move from foundation to tableau
  - Preconditions: The foundation must contain a card that can be placed on a tableau column (following the descending order of alternating colors rule).
  - Effects: The card is removed from the foundation and added to the tableau column.

- Move from foundation to freecell
  - Preconditions: The foundation must contain a card and there must be an empty free cell.
  - Effects: The card is removed from the foundation and added to the freecell.

Heuristics/evaluation function

## 4. **Work Implementation**

...
