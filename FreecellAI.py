from FreecellState import FreecellState
from Move import Move

def solve_game(game):
    def dfs(state, visited):
        if state.is_solved():
            return True
        state_key = state_to_key(state)
        if state_key in visited:
            return False
        visited.add(state_key)
        possible_moves = state.get_possible_moves()
        for move in sorted(possible_moves, key=move_heuristic):
            new_state = state.copy().apply_move(move)
            if new_state and dfs(new_state, visited):
                return True
        return False

    def state_to_key(state):
        # Create a unique key for the state to track visited states
        return (tuple(tuple(col) for col in state.tableau),
                tuple(state.free_cells),
                tuple(state.foundations.items()))

    def move_heuristic(move):
        # Heuristic to prioritize moves that advance cards to the foundation
        if move.move_type in ["tableau_to_foundation", "freecell_to_foundation"]:
            return 0
        return 1

    visited = set()
    if dfs(game, visited):
        print("Game solved!")
        return True
    print("No solution found.")
    return False
