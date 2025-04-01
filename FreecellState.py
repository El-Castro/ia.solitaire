import copy
from Card import Card
from Move import Move
import FreecellMove as fcm
import random
import os
import json

class FreecellState:
    def __init__(self, tableau, free_cells=None, foundations=None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: 0 for suit in ['hearts', 'diamonds', 'clubs', 'spades']}
        self.history = []

    def copy(self):
        """Creates a deep copy of the current FreecellState instance."""
        return FreecellState(copy.deepcopy(self.tableau), self.free_cells[:], self.foundations.copy())
    
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
        self.heuristic()
        return self


# Saves & Presets -----------------------------------------------------------------------------------------------------------------------------


    def save_to_file(self, filename):
        """Saves the current state of the game to a file."""
        state = {
            'tableau': [[card.to_dict() for card in col] for col in self.tableau],
            'free_cells': [card.to_dict() if card else None for card in self.free_cells],
            'foundations': self.foundations
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
        #print("Apply move: " + move.__repr__())
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

    def get_possible_moves_AI(self):
        """Calls get_possible_moves_AI from FreecellMove."""
        return fcm.get_possible_moves_AI(self)

# Heuristic -----------------------------------------------------------------------------------------------------------------------------

    """Calculates a heuristic value for the current FreecellState."""
    def heuristic(self):
        
        f_weight = 1
        blocking_weight = 0.66
        fc_weight = 1.33

        foundation_score = sum(13 - self.foundations[suit] for suit in self.foundations)
        blocking_cards = sum(len(col) - 1 for col in self.tableau if col)
        blocked_free_cells = sum(1 for cell in self.free_cells if cell)
        #free_columns = sum(1 for col in self.tableau if not col)
        
        # Adjust weights based on experimentation
        score = f_weight * foundation_score + blocking_weight * blocking_cards + fc_weight * blocked_free_cells #- 3 * free_columns
        print(f"Foundation: {f_weight * foundation_score}, Blocked: {blocking_weight * blocking_cards}, Free Cells: {fc_weight * blocked_free_cells}  ")# Free Columns: {-2 * free_columns}
        print(f"Total: {score}\n")
        
        return score


    #Efficiency improvement attempt (in progress)
    def heuristic(self):
        foundation_weight = 1
        fc_weight = 0.25
        fcol_weight = -0.4
        blocked_weight = 0.5

        foundation_score = sum(13 - self.foundations[suit] for suit in self.foundations)
        blocked_free_cells = 0
        free_columns = 0
        blocked_next_cards = 0
        
        # Efficient tracking of the next needed card for each suit
        next_needed = {suit: self.foundations[suit] + 1 for suit in self.foundations if self.foundations[suit] < 13}
        found_suits = set()

        for card in self.free_cells:
            if card:
                blocked_free_cells += 1
                suit, rank = card.suit, card.rank
                if suit in next_needed and rank == next_needed[suit]:
                    found_suits.add(suit)

        for col in self.tableau:
            if not col:  # Count all open columns
                free_columns += 1
                continue
            if len(found_suits) == len(next_needed): continue # If column not empty but all suits are found, skip
            for depth, card in enumerate(col):  # If there are cards to find, investigate the column
                suit, rank = card.suit, card.rank
                if suit in found_suits: continue    # Skip card if suit is already found
                if suit in next_needed and rank == next_needed[suit]:  # It's a needed card
                    blocked_next_cards += (len(col) - depth) # Penalize based on how deep it's buried
                    found_suits.add(suit)  # Add suit to found suits
                    if len(found_suits) == len(next_needed): break # Stop if all needed suits were found
                

        score = foundation_weight * foundation_score + blocked_weight * blocked_next_cards + fc_weight * blocked_free_cells - fcol_weight * free_columns

        print(f"Foundation: {foundation_weight * foundation_score}, Blocked: {blocked_weight * blocked_next_cards}, Free Cells: {fc_weight * blocked_free_cells}, Free Columns: {fcol_weight * free_columns}, Total: {score}\n")
        return score


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
