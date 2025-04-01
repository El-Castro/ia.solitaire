from Card import Card
from Move import Move
import FreecellMove as fcm
import random
import os
import json

class FreecellState:
    def __init__(self, tableau, free_cells=None, foundations=None,minutes = None, seconds = None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: 0 for suit in ['hearts', 'diamonds', 'clubs', 'spades']}
        self.history = []
        self.minutes = minutes
        self.seconds = seconds

    def copy(self):
        """Creates a deep copy of the current FreecellState instance."""
        return FreecellState([col[:] for col in self.tableau], self.free_cells[:], self.foundations.copy())
    
    def is_solved(self):
        """Checks if the current FreecellState is in a solved state."""
        return all(self.foundations[suit] == 13 for suit in self.foundations)
    
    def undo(self):
        """Reverts the FreecellState to the previous state if there is any history."""
        if self.history:
            previous_state = self.history.pop()
            self.tableau = previous_state.tableau
            self.free_cells = previous_state.free_cells
            self.foundations = previous_state.foundations
        return self


# Saves & Presets -----------------------------------------------------------------------------------------------------------------------------


    def save_to_file(self, filename):
        """Saves the current state of the game to a file."""
        state = {
            'tableau': [[card.to_dict() for card in col] for col in self.tableau],
            'free_cells': [card.to_dict() if card else None for card in self.free_cells],
            'foundations': self.foundations,
            'time': {"minutes": self.minutes, "seconds": self.seconds}
        }
        with open(os.path.join('saves', filename), 'w') as f:
            json.dump(state, f)

    @staticmethod
    def load_from_file(filename):
        """Loads a game state from a file."""
        with open(os.path.join('saves', filename), 'r') as f:
            state = json.load(f)
        tableau = [[Card.from_dict(card) for card in col] for col in state['tableau']]
        free_cells = [Card.from_dict(card) if card else None for card in state['free_cells']]
        foundations = state['foundations']
        return FreecellState(tableau, free_cells, foundations)
    
    def save_state(self):
        """Saves the current state to the history for undo functionality."""
        self.history.append(self.copy())

    @staticmethod
    def create_random_state():
        """Creates a random initial game state."""
        # Create a deck of cards
        deck = [Card(rank, suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades'] for rank in range(1, 14)]
        random.shuffle(deck)
        
        # Distribute cards to tableau columns
        tableau = [[] for _ in range(8)]
        for i, card in enumerate(deck):
            tableau[i % 8].append(card)
        
        return FreecellState(tableau)

    @staticmethod
    def load_presets(filename):
        """Loads preset game states from a file."""
        with open(os.path.join('saves', filename), 'r') as f:
            presets = json.load(f)
        return presets
    
    @staticmethod
    def get_presets_name(presets):
        """Retrieves the names of the preset game states."""
        return [preset["name"] for preset in presets]
    
    @staticmethod
    def create_from_preset(preset):
        """Creates a game state from a preset."""
        tableau = [[Card.from_dict(card) for card in col] for col in preset['tableau']]
        free_cells = [Card.from_dict(card) if card else None for card in preset['free_cells']]
        foundations = preset['foundations']
        return FreecellState(tableau, free_cells, foundations)


# Move Executioner -----------------------------------------------------------------------------------------------------------------------------


    def apply_move(self, move):
        """Applies a given move to the current FreecellState, creating the new state."""
        print("Apply move: " + move.__repr__())
        move_type = move.move_type
        new_state = None
        if move_type == "tableau_to_foundation":
            new_state = fcm.move_tableau_to_foundation(self, move.source)
        elif move_type == "tableau_to_freecell":
            new_state = fcm.move_tableau_to_freecell(self, move.source)
        elif move_type == "freecell_to_foundation":
            new_state = fcm.move_freecell_to_foundation(self, move.source)
        elif move_type == "tableau_to_tableau":
            new_state = fcm.move_tableau_to_tableau(self, move.source, move.destination)
        elif move_type == "freecell_to_tableau":
            new_state = fcm.move_freecell_to_tableau(self, move.source, move.destination)
        elif move_type == "foundation_to_tableau":
            new_state = fcm.move_foundation_to_tableau(self, move.source, move.destination)
        elif move_type == "foundation_to_freecell":
            new_state = fcm.move_foundation_to_freecell(self, move.source)
        
        if new_state:
            self.save_state()  # Save current state before applying the move
            self.tableau = new_state.tableau
            self.free_cells = new_state.free_cells
            self.foundations = new_state.foundations
        return self

    def get_possible_moves(self):
        """Calls get_possible_moves from FreecellMove."""
        return fcm.get_possible_moves(self)


# Heuristic -----------------------------------------------------------------------------------------------------------------------------


    def heuristic(self):
        """Calculates a heuristic value for the current FreecellState."""
        foundation_score = sum(13 - self.foundations[suit] for suit in self.foundations)
        blocking_cards = sum(len(col) - 1 for col in self.tableau if col)
        free_cells = sum(1 for cell in self.free_cells if cell)
        
        print(0.003 * foundation_score + 0.002 * blocking_cards + 0.004 * free_cells)

        # Adjust weights based on experimentation
        return 0.003 * foundation_score + 0.002 * blocking_cards + 0.004 * free_cells


    # Efficiency improvement attempt (in progress)
    # def heuristic(self):
    #     foundation_score = sum(13 - self.foundations[suit] for suit in self.foundations)
        
    #     # Efficient tracking of the next needed card for each suit
    #     next_needed = {suit: self.foundations[suit] + 1 for suit in self.foundations}

    #     for card in self.free_cells:
    #         if card:
    #             suit, rank = card.suit, card.rank
    #             if suit in next_needed and rank == next_needed[suit]:
    #                 del next_needed[suit]  # Remove immediately (already accessible)

    #     blocked_next_cards = 0

    #     for col in self.tableau:
    #         for depth, card in enumerate(col):  # Iterate from top to bottom
    #             suit, rank = card.suit, card.rank
    #             if suit in next_needed and rank == next_needed[suit]:  # It's a needed card
    #                 blocked_next_cards += depth  # Penalize based on how deep it's buried
    #                 del next_needed[suit]  # Remove suit from tracking
    #                 if not next_needed:  # Stop once all 4 suits are found
    #                     break
    #         if not next_needed:  
    #             break  # No need to keep searching

    #     free_columns = sum(1 for col in self.tableau if not col)
    #     free_cells = sum(1 for cell in self.free_cells if cell is None)

    #     return 3 * foundation_score + 2 * blocked_next_cards - 3 * free_cells - 4 * free_columns


# Dunder Methods -----------------------------------------------------------------------------------------------------------------------------


    def __hash__(self):
        """Provides a unique hash value for the FreecellState instance."""
        return hash((tuple(tuple(col) for col in self.tableau), 
                    tuple(self.free_cells), 
                    tuple(sorted(self.foundations.items()))))

    def __eq__(self, other):
        """Check if two FreecellState instances are equal."""
        return (self.tableau == other.tableau and
                self.free_cells == other.free_cells and
                self.foundations == other.foundations)

    def __lt__(self, other):
        """Compare two FreecellState objects based on their heuristic values."""
        return self.heuristic() < other.heuristic()
