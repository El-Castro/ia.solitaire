from Card import Card
from Move import Move

# Possible Moves ----------------------------------------------------------------------------------------------------------------------------------------------


def get_possible_moves_Astar(state):
    """Get all possible moves from the state, avoiding back-and-forth moves."""
    moves = []
    
    last_state = state.history[-1] if state.history else None  # Last state for comparison

    # Moves from tableau to foundation (always a good move)
    for i, column in enumerate(state.tableau):
        if column:
            card = column[-1]
            if can_move_to_foundation(state, card):
                moves.append(Move("tableau_to_foundation", i, card.suit))

    # Moves from tableau to freecell (avoid reversing freecell_to_tableau)
    for i, column in enumerate(state.tableau):
        if column and can_move_to_freecell(state):
            if not (last_state and last_state.free_cells.count(None) < state.free_cells.count(None)):  
                moves.append(Move("tableau_to_freecell", i, None))

    # Moves from tableau to tableau (avoid reversing last tableau_to_tableau move)
    for i, column in enumerate(state.tableau):
        if column:
            for j, target_column in enumerate(state.tableau):
                if i != j and can_move_to_tableau(state, column[-1], j):
                    if not (last_state and last_state.tableau[j] and last_state.tableau[j][-1] == column[-1]):
                        moves.append(Move("tableau_to_tableau", i, j))

    # Moves from freecell to foundation (always a good move)
    for i, card in enumerate(state.free_cells):
        if card and can_move_to_foundation(state, card):
            moves.append(Move("freecell_to_foundation", i, card.suit))

    # Moves from freecell to tableau (avoid reversing tableau_to_freecell)
    for i, card in enumerate(state.free_cells):
        if card:
            for j, column in enumerate(state.tableau):
                if can_move_to_tableau(state, card, j):
                    if not (last_state and last_state.tableau[j] and last_state.tableau[j][-1] == card):
                        moves.append(Move("freecell_to_tableau", i, j))

    # # Moves from foundation to tableau (avoid moving back to foundation immediately)
    # for suit in state.foundations:
    #     if state.foundations[suit] > 0:
    #         for j, column in enumerate(state.tableau):
    #             card = Card(state.foundations[suit], suit)
    #             if can_move_to_tableau(state, card, j):
    #                 if not (last_state and last_state.tableau[j] and last_state.tableau[j][-1] == card):
    #                     moves.append(Move("foundation_to_tableau", suit, j))

    # print("Valid moves----------------------------")
    # for i in moves:
    #     print(i)
    # print("---------------------------------------")
    return moves

def get_possible_moves(state, AImode=False):
    """Get all possible moves from the state"""
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
        if state.foundations[suit] > 1:
            for j, column in enumerate(state.tableau):
                card = Card(state.foundations[suit], suit)
                if can_move_to_tableau(state, card, j):
                    moves.append(Move("foundation_to_tableau", suit, j))

    for suit in state.foundations:
        if state.foundations[suit] > 1 and can_move_to_freecell(state):
            moves.append(Move("foundation_to_freecell", suit, None))

    if not AImode:
        print("Valid moves----------------------------")
        for i in moves:
            print(i)
        print("---------------------------------------")
    return moves


# Automatic Moves ---------------------------------------------------------------------------------------------------------------------------------------------


def get_automatic_moves(state):

    moves = []

    next_needed = {suit: state.foundations[suit] + 1 for suit in state.foundations if state.foundations[suit] < 13}
    
    """Check if an opposite-color card of rank-1 exists in the top 3 depths of any tableau column."""
    def near_lower(card):
        if card.rank <= 2:  
            return False  # A 2 or Ace can never block anything, always move it
        for col in state.tableau:
            if col and len(col) > 1:  # Ignore empty columns and single cards
                for depth in range(min(2, len(col))):  # Check only the top 2 cards
                    top_card = col[-(depth + 1)]
                    if top_card.rank == card.rank - 1 and top_card.colour != card.colour:
                        return True
        return False

    for i, column in enumerate(state.tableau):
        if column:
            card = column[-1]
            suit, rank = card.suit, card.rank

            if suit in next_needed and rank == next_needed[suit]:  # Can move to foundation
                #if not near_lower(card):
                    moves.append(Move("tableau_to_foundation", i, suit))

        # Check Freecells for automatic moves
    for i, card in enumerate(state.free_cells):
        if card:
            suit, rank = card.suit, card.rank

            if suit in next_needed and rank == next_needed[suit]:  # Can move to foundation
                #if not near_lower(card):
                    moves.append(Move("freecell_to_foundation", i, suit))
    
    #print("Automatic Moves:", [f"{move.move_type} from {move.source}" for move in moves])
        
    return moves

def apply_automatic_moves(state):
    """Recursively applies all automatic moves to foundations until no more can be made."""
    
    while True:
        moves = get_automatic_moves(state)
        if not moves:  # Stop when no more automatic moves are possible
            break
        for move in moves:
            state.apply_move(move)  # Apply each move
    
    return state


# Individual Move Possibility ---------------------------------------------------------------------------------------------------------------------------------


def can_move_to_foundation(state, card):
    """Check if a card can be moved to the foundation"""
    suit, rank = card.suit, card.rank
    foundation = state.foundations.get(suit, 0)
    return (rank == 1 and foundation == 0) or (foundation == rank - 1)

def can_move_to_tableau(state, card, column):
    """Check if a card can be moved to a tableau column"""
    if not state.tableau[column]:
        return True
    top_card = state.tableau[column][-1]
    return (card.rank == top_card.rank - 1) and (card.colour != top_card.colour)

def can_move_to_freecell(state):
    """Check if there is an empty free cell to move the card to"""
    return None in state.free_cells


# Individual Move Executioners --------------------------------------------------------------------------------------------------------------------------------


def move_tableau_to_foundation(state, col, AImode=False):
    """
    Move a card from tableau to foundation
    Preconditions:
    - The tableau column `col` is not empty.
    - The top card of the tableau column can be moved to the foundation.
    Effects:
    - The top card is removed from the tableau column.
    - The card is added to the foundation.
    Costs:
    - Typically, the cost is 1 move.
    """
    if state.tableau[col]:  # Ensure column is not empty
        card = state.tableau[col][-1]
        if can_move_to_foundation(state, card):
            new_state = state.copy()
            new_state.tableau[col].pop()
            new_state.foundations[card.suit] = card.rank
            if not AImode: print(f"TB-F {card.rank} of {card.suit}\n")
            return new_state
    return None

def move_tableau_to_freecell(state, col, AImode=False):
    """
    Move a card from tableau to freecell
    Preconditions:
    - The tableau column `col` is not empty.
    - There is at least one empty free cell.
    Effects:
    - The top card is removed from the tableau column.
    - The card is placed in an empty free cell.
    Costs:
    - Typically, the cost is 1 move.
    """
    if state.tableau[col]:  # Ensure column is not empty
        for i in range(len(state.free_cells)):
            if state.free_cells[i] is None:  # Find an empty FreeCell
                new_state = state.copy()
                if not AImode: print(f"TB{col}-FC {new_state.tableau[col][-1].rank} of {new_state.tableau[col][-1].suit}\n")
                new_state.free_cells[i] = new_state.tableau[col].pop()  # Modify the copied state
                return new_state
    return None

def move_freecell_to_foundation(state, fc, AImode=False):
    """
    Move a card from freecell to foundation
    Preconditions:
    - The free cell `fc` is not empty.
    - The card in the free cell can be moved to the foundation.
    Effects:
    - The card is removed from the free cell.
    - The card is added to the foundation.
    Costs:
    - Typically, the cost is 1 move.
    """
    if state.free_cells[fc] is not None:
        card = state.free_cells[fc]
        if can_move_to_foundation(state, card):
            new_state = state.copy()
            new_state.free_cells[fc] = None
            new_state.foundations[card.suit] = card.rank
            if not AImode: print(f"FC-F {card.rank} of {card.suit}\n")
            return new_state
    return None

def move_tableau_to_tableau(state, src, dest, AImode=False):
    """
    Move a card from one tableau column to another
    Preconditions:
    - The source tableau column `src` is not empty.
    - The top card of the source column can be moved to the destination column `dest`.
    Effects:
    - The top card is removed from the source tableau column.
    - The card is added to the destination tableau column.
    Costs:
    - Typically, the cost is 1 move.
    """
    if state.tableau[src]:  # Ensure source is not empty
        card = state.tableau[src][-1]
        if can_move_to_tableau(state, card, dest):
            new_state = state.copy()
            new_state.tableau[dest].append(new_state.tableau[src].pop())
            if not AImode: print(f"TB{src}-TB{dest} {card.rank} of {card.suit}\n")
            return new_state
    return None

def move_freecell_to_tableau(state, fc, col, AImode=False):
    """
    Move a card from freecell to tableau
    Preconditions:
    - The free cell `fc` is not empty.
    - The card in the free cell can be moved to the tableau column `col`.
    Effects:
    - The card is removed from the free cell.
    - The card is added to the tableau column.
    Costs:
    - Typically, the cost is 1 move.
    """
    if state.free_cells[fc] is not None:
        card = state.free_cells[fc]
        if can_move_to_tableau(state, card, col):
            new_state = state.copy()
            new_state.tableau[col].append(card)
            new_state.free_cells[fc] = None
            if not AImode: print(f"FC-TB{col} {card.rank} of {card.suit}\n")
            return new_state
    return None

def move_foundation_to_tableau(state, suit, col):
    """
    Move a card from foundation to tableau
    Preconditions:
    - The foundation for the suit is not empty.
    - The card can be moved to the tableau column `col`.
    Effects:
    - The card is removed from the foundation.
    - The card is added to the tableau column.
    Costs:
    - Typically, the cost is 1 move.
    """
    if suit in state.foundations and state.foundations[suit] > 0:
        card = Card(state.foundations[suit], suit)
        if can_move_to_tableau(state, card, col):
            new_state = state.copy()
            new_state.foundations[suit] -= 1
            new_state.tableau[col].append(card)
            print(f"F-TB {card.rank} of {card.suit}\n")
            return new_state
    return None

def move_foundation_to_freecell(state, suit):
    """
    Move a card from foundation to freecell (rare case)
    Preconditions:
    - The foundation for the suit is not empty.
    - There is at least one empty free cell.
    Effects:
    - The card is removed from the foundation.
    - The card is placed in an empty free cell.
    Costs:
    - Typically, the cost is 1 move.
    """
    if suit in state.foundations and state.foundations[suit] > 0:
        for i in range(len(state.free_cells)):
            if state.free_cells[i] is None:
                new_card=Card(state.foundations[suit], suit)
                new_state = state.copy()
                new_state.free_cells[i] = new_card
                new_state.foundations[suit] -= 1
                print(f"{new_card.rank} of {new_card.suit}\n")
                return new_state
    return None
