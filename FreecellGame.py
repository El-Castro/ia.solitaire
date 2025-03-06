import copy
import heapq

class FreeCell:
    def __init__(self, tableau, free_cells=None, foundations=None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: [] for suit in ['hearts', 'diamonds', 'clubs', 'spades']}

    def is_solved(self):
        return all(len(self.foundations[suit]) == 13 for suit in self.foundations)
    
    def get_possible_moves(self):
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
        return moves
    
    def can_move_to_foundation(self, card):
        suit, rank = card
        foundation = self.foundations[suit]
        return (rank == 1 and not foundation) or (foundation and foundation[-1] == rank - 1)
    
    def apply_move(self, move):
        new_state = copy.deepcopy(self)
        move_type, index = move
        if move_type == "tableau_to_foundation":
            card = new_state.tableau[index].pop()
            new_state.foundations[card[0]].append(card)
        elif move_type == "tableau_to_freecell":
            card = new_state.tableau[index].pop()
            free_index = new_state.free_cells.index(None)
            new_state.free_cells[free_index] = card
        elif move_type == "freecell_to_foundation":
            card = new_state.free_cells[index]
            new_state.free_cells[index] = None
            new_state.foundations[card[0]].append(card)
        return new_state
    
    def heuristic(self):
        return sum(13 - len(self.foundations[suit]) for suit in self.foundations)

def a_star_search(initial_state):
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
