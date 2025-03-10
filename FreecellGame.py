import tkinter as tk
from tkinter import Canvas
import random
import copy
import heapq

class FreeCellState:
    def __init__(self, tableau, free_cells=None, foundations=None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: [] for suit in ['hearts', 'diamonds', 'clubs', 'spades']}

    def copy(self):
        return FreeCellState([col[:] for col in self.tableau], self.free_cells[:], self.foundations.copy())
    
    def is_solved(self):
        # Check if all foundations are complete
        return all(len(self.foundations[suit]) == 13 for suit in self.foundations)

    def get_possible_moves(self):
        # Get all possible moves from the current state
        moves = []
        for i, column in enumerate(self.tableau):
            if column and self.can_move_to_foundation(column[-1]):
                moves.append(("tableau_to_foundation", i))
        for i, column in enumerate(self.tableau):
            if column and None in self.free_cells:
                moves.append(("tableau_to_freecell", i))
        for i, card in enumerate(self.free_cells):
            if card and self.can_move_to_foundation(card):
                moves.append(("freecell_to_foundation", i))
        for i, column in enumerate(self.tableau):
            if column:
                for j, target_column in enumerate(self.tableau):
                    if i != j and self.can_move_to_tableau(column[-1], target_column):
                        moves.append(("tableau_to_tableau", i, j))
        for i, card in enumerate(self.free_cells):
            if card:
                for j, column in enumerate(self.tableau):
                    if self.can_move_to_tableau(card, column):
                        moves.append(("freecell_to_tableau", i, j))
        return moves

    def can_move_to_foundation(self, card):
        # Check if a card can be moved to the foundation
        suit, rank = card
        foundation = self.foundations[suit]
        return (rank == 1 and not foundation) or (foundation and foundation[-1][1] == rank - 1)

    def can_move_to_tableau(self, card, column):
        # Check if a card can be moved to a tableau column
        if not column:
            return True
        top_card = column[-1]
        return (card[1] == top_card[1] - 1) and (card[0] != top_card[0])

    def apply_move(self, move):
        # Apply a move to the game state and return the new state
        new_state = copy.deepcopy(self)
        move_type, *indices = move
        if move_type == "tableau_to_foundation":
            card = new_state.tableau[indices[0]].pop()
            new_state.foundations[card[0]].append(card)
        elif move_type == "tableau_to_tableau":
            from_column, to_column = indices
            card = new_state.tableau[from_column].pop()
            new_state.tableau[to_column].append(card)
        elif move_type == "tableau_to_freecell":
            card = new_state.tableau[indices[0]].pop()
            free_index = new_state.free_cells.index(None)
            new_state.free_cells[free_index] = card
        elif move_type == "freecell_to_foundation":
            card = new_state.free_cells[indices[0]]
            new_state.free_cells[indices[0]] = None
            new_s[card[0]].append(card)
        elif move_type == "freecell_to_tableau":
            free_index, to_column = indices
            card = new_state.free_cells[free_index]
            new_state.free_cells[free_index] = None
            new_state.tableau[to_column].append(card)
        return new_state

    def heuristic(self):
        # Heuristic function for A* search
        return sum(13 - len(self.foundations[suit]) for suit in self.foundations)

def a_star_search(initial_state):
    # A* search algorithm to solve the FreeCell game
    open_list = []
    heapq.heappush(open_list, (initial_state.heuristic(), initial_state))
    visited = set()
    while open_list:
        _, current_state = heapq.heappop(open_list)
        if current_state.is_solved():
            return current_state
        visited.add(str(current_state.tableau))
        for move in current_state.get_possible_moves():
            new_state = current_state.apply_move(move)
            if str(new_state.tableau) not in visited:
                heapq.heappush(open_list, (new_state.heuristic(), new_state))
    return None

# Move from tableau to foundation
def move_tableau_to_foundation(state, col):
    if state.tableau[col]:  # Ensure column is not empty
        card = state.tableau[col][-1]
        suit, rank = card
        if suit in state.foundations and state.foundations[suit] == rank - 1 or (rank == 1 and suit not in state.foundations):
            new_state = state.copy()
            new_state.tableau[col].pop()
            new_state.foundation[suit] = rank
            return new_state
    return None

# Move from tableau to freecell
def move_tableau_to_freecell(state, col):
    if state.tableau[col]:  # Ensure column is not empty
        for i in range(len(state.freecells)):
            if state.freecells[i] is None:
                new_state = state.copy()
                new_state.freecells[i] = state.tableau[col].pop()
                return new_state
    return None

# Move from freecell to foundation
def move_freecell_to_foundation(state, fc):
    if state.freecells[fc] is not None:
        card = state.freecells[fc]
        suit, rank = card
        if suit in state.foundations and state.foundations[suit] == rank - 1 or (rank == 1 and suit not in state.foundations):
            new_state = state.copy()
            new_state.freecells[fc] = None
            new_state.foundation[suit] = rank
            return new_state
    return None

# Move from tableau to tableau
def move_tableau_to_tableau(state, src, dest):
    if state.tableau[src]:  # Ensure source is not empty
        card = state.tableau[src][-1]
        if not state.tableau[dest] or (state.tableau[dest][-1][1] == card[1] + 1 and state.tableau[dest][-1][0] != card[0]):
            new_state = state.copy()
            new_state.tableau[dest].append(new_state.tableau[src].pop())
            return new_state
    return None

# Move from freecell to tableau
def move_freecell_to_tableau(state, fc, col):
    if state.freecells[fc] is not None:
        card = state.freecells[fc]
        if not state.tableau[col] or (state.tableau[col][-1][1] == card[1] + 1 and state.tableau[col][-1][0] != card[0]):
            new_state = state.copy()
            new_state.tableau[col].append(card)
            new_state.freecells[fc] = None
            return new_state
    return None

# Move from foundation to tableau
def move_foundation_to_tableau(state, suit, col):
    if suit in state.foundations and state.foundations[suit] > 0:
        card = (suit, state.foundations[suit])
        if not state.tableau[col] or (state.tableau[col][-1][1] == card[1] + 1 and state.tableau[col][-1][0] != card[0]):
            new_state = state.copy()
            new_state.foundation[suit] -= 1
            new_state.tableau[col].append(card)
            return new_state
    return None

# Move from foundation to freecell (rare case)
def move_foundation_to_freecell(state, suit, fc):
    if suit in state.foundations and state.foundations[suit] > 0 and state.freecells[fc] is None:
        new_state = state.copy()
        new_state.freecells[fc] = (suit, state.foundations[suit])
        new_state.foundation[suit] -= 1
        return new_state
    return None