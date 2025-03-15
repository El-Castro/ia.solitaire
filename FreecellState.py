from Card import Card
from Move import Move
import FreecellMove as fcm
import random
import copy
import heapq
import os
import json

class FreeCellState:
    def __init__(self, tableau, free_cells=None, foundations=None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: 0 for suit in ['hearts', 'diamonds', 'clubs', 'spades']}
        self.history = []

    def copy(self):
        return FreeCellState([col[:] for col in self.tableau], self.free_cells[:], self.foundations.copy())
    
    def is_solved(self):
        # Check if all foundations are complete
        return all(len(self.foundations[suit]) == 13 for suit in self.foundations)

    def save_to_file(self, filename):
        state = {
            'tableau': [[card.to_dict() for card in col] for col in self.tableau],
            'free_cells': [card.to_dict() if card else None for card in self.free_cells],
            'foundations': self.foundations
        }
        with open(os.path.join('saves', filename), 'w') as f:
            json.dump(state, f)

    @staticmethod
    def load_from_file(filename):
        with open(os.path.join('saves', filename), 'r') as f:
            state = json.load(f)
        tableau = [[Card.from_dict(card) for card in col] for col in state['tableau']]
        free_cells = [Card.from_dict(card) if card else None for card in state['free_cells']]
        foundations = state['foundations']
        return FreeCellState(tableau, free_cells, foundations)

    @staticmethod
    def create_random_state():
        # Create a deck of cards
        deck = [Card(rank, suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades'] for rank in range(1, 14)]
        random.shuffle(deck)
        
        # Distribute cards to tableau columns
        tableau = [[] for _ in range(8)]
        for i, card in enumerate(deck):
            tableau[i % 8].append(card)
        
        return FreeCellState(tableau)

    @staticmethod
    def load_presets(filename):
        with open(filename, 'r') as f:
            presets = json.load(f)
        return presets

    @staticmethod
    def create_from_preset(preset):
        tableau = [[Card.from_dict(card) for card in col] for col in preset['tableau']]
        free_cells = [Card.from_dict(card) if card else None for card in preset['free_cells']]
        foundations = preset['foundations']
        return FreeCellState(tableau, free_cells, foundations)

    def save_state(self):
        self.history.append(self.copy())

    def undo(self):
        if self.history:
            previous_state = self.history.pop()
            self.tableau = previous_state.tableau
            self.free_cells = previous_state.free_cells
            self.foundations = previous_state.foundations

    def apply_move(self, move):
        print("Apply move")
        move_type = move.move_type
        if move_type == "tableau_to_foundation":
            return fcm.move_tableau_to_foundation(self, move.source)
        elif move_type == "tableau_to_freecell":
            return fcm.move_tableau_to_freecell(self, move.source)
        elif move_type == "freecell_to_foundation":
            return fcm.move_freecell_to_foundation(self, move.source)
        elif move_type == "tableau_to_tableau":
            return fcm.move_tableau_to_tableau(self, move.source, move.destination)
        elif move_type == "freecell_to_tableau":
            return fcm.move_freecell_to_tableau(self, move.source, move.destination)
        elif move_type == "foundation_to_tableau":
            return fcm.move_foundation_to_tableau(self, move.source, move.destination)
        elif move_type == "foundation_to_freecell":
            return fcm.move_foundation_to_freecell(self, move.source, move.destination)
        return self

    def get_possible_moves(self):
        return fcm.get_possible_moves(self)

    def apply_moves(self, moves):
        for move in moves:
            self.apply_move(move)
        return self
