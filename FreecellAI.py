from FreecellState import FreecellState
from Move import Move
import heapq

def heuristic(state):
    # Heuristic function to estimate the cost to the goal
    foundation_score = sum(13 - state.foundations[suit] for suit in state.foundations)
    blocking_cards = sum(len(col) - 1 for col in state.tableau if col)
    free_cells = sum(1 for cell in state.free_cells if cell)
    return foundation_score + blocking_cards + free_cells

def solve_game(game):
    open_set = []
    game.set_heuristic(heuristic)
    heapq.heappush(open_set, (0 + heuristic(game), 0, game))
    came_from = {}
    g_score = {game: 0}
    f_score = {game: heuristic(game)}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current.is_solved():
            return reconstruct_path(came_from, current)

        for move in current.get_possible_moves():
            neighbor = current.copy().apply_move(move)
            neighbor.set_heuristic(heuristic)
            tentative_g_score = current_g + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

    return None

def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()
    return total_path

