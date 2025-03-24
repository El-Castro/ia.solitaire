from Card import Card
from Move import Move

def get_possible_moves(state):
    # Get all possible moves from the current state
    moves = []
    for i, column in enumerate(state.tableau):
        if column:
            card = column[-1]
            if column and can_move_to_foundation(state, card):
                moves.append(Move("tableau_to_foundation", i, card.suit))

    for i, column in enumerate(state.tableau):
        if column and can_move_to_freecell(state):
            moves.append(Move("tableau_to_freecell", i, None))
            
    for i, card in enumerate(state.free_cells):
        if card and can_move_to_foundation(state, card):
            moves.append(Move("freecell_to_foundation", i, card.suit))
            
    for i, column in enumerate(state.tableau):
        if column:
            for j, target_column in enumerate(state.tableau):
                if i != j and can_move_to_tableau(state, column[-1], j):
                    moves.append(Move("tableau_to_tableau", i, j))

    for i, card in enumerate(state.free_cells):
        if card:
            for j, column in enumerate(state.tableau):
                if can_move_to_tableau(state, card, j):
                    moves.append(Move("freecell_to_tableau", i, j))

    for suit in state.foundations:
        if state.foundations[suit] > 0:
            for j, column in enumerate(state.tableau):
                card = Card(state.foundations[suit], suit)
                if can_move_to_tableau(state, card, j):
                    moves.append(Move("foundation_to_tableau", suit, j))

    for suit in state.foundations:
        if state.foundations[suit] > 0 and can_move_to_freecell(state):
            for i in range(len(state.free_cells)):
                if state.free_cells[i] is None:
                    moves.append(Move("foundation_to_freecell", suit, None))

    print("Valid moves----------------------------")
    for i in moves:
        print(i.__repr__())
    print("---------------------------------------")
    return moves


# Checking if move is possible ---------------------------------------------------------------------------------------------------------------

def can_move_to_foundation(state, card):
    # Check if a card can be moved to the foundation
    suit, rank = card.suit, card.rank
    foundation = state.foundations.get(suit, 0)
    return (rank == 1 and foundation == 0) or (foundation == rank - 1)

def can_move_to_tableau(state, card, column):
    # Check if a card can be moved to a tableau column
    if not state.tableau[column]:
        return True
    top_card = state.tableau[column][-1]
    return (card.rank == top_card.rank - 1) and (card.colour != top_card.colour)

def can_move_to_freecell(state):
    # Check if there is an empty free cell to move the card to
    return None in state.free_cells


# Execute move --------------------------------------------------------------------------------------------------------------------------------


def move_tableau_to_foundation(state, col):
    if state.tableau[col]:  # Ensure column is not empty
        card = state.tableau[col][-1]
        if can_move_to_foundation(state, card):
            new_state = state.copy()
            new_state.tableau[col].pop()
            new_state.foundations[card.suit] = card.rank
            return new_state
    return None

# Move from tableau to freecell
def move_tableau_to_freecell(state, col):
    if state.tableau[col]:  # Ensure column is not empty
        for i in range(len(state.free_cells)):
            if state.free_cells[i] is None:  # Find an empty FreeCell
                new_state = state.copy()
                new_state.free_cells[i] = new_state.tableau[col].pop()  # Modify the copied state
                return new_state
    return None

# Move from freecell to foundation
def move_freecell_to_foundation(state, fc):
    if state.free_cells[fc] is not None:
        card = state.free_cells[fc]
        if can_move_to_foundation(state, card):
            new_state = state.copy()
            new_state.free_cells[fc] = None
            new_state.foundations[card.suit] = card.rank
            return new_state
    return None

# Move from tableau to tableau
def move_tableau_to_tableau(state, src, dest):
    if state.tableau[src]:  # Ensure source is not empty
        card = state.tableau[src][-1]
        if can_move_to_tableau(state, card, dest):
            new_state = state.copy()
            new_state.tableau[dest].append(new_state.tableau[src].pop())
            return new_state
    return None

# Move from freecell to tableau
def move_freecell_to_tableau(state, fc, col):
    if state.free_cells[fc] is not None:
        card = state.free_cells[fc]
        if can_move_to_tableau(state, card, col):
            new_state = state.copy()
            new_state.tableau[col].append(card)
            new_state.free_cells[fc] = None
            return new_state
    return None

# Move from foundation to tableau
def move_foundation_to_tableau(state, suit, col):
    if suit in state.foundations and state.foundations[suit] > 0:
        card = Card(state.foundations[suit], suit)
        if can_move_to_tableau(state, card, col):
            new_state = state.copy()
            new_state.foundations[suit] -= 1
            new_state.tableau[col].append(card)
            return new_state
    return None

# Move from foundation to freecell (rare case)
def move_foundation_to_freecell(state, suit, fc):
    if suit in state.foundations and state.foundations[suit] > 0:
        for i in range(len(state.free_cells)):
            if state.free_cells[i] is None:
                new_state = state.copy()
                new_state.free_cells[i] = Card(state.foundations[suit], suit)
                new_state.foundations[suit] -= 1
                return new_state
    return None