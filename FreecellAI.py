from collections import deque
import heapq



def solve_game_astar(game):
    """This function attempts to solve the Freecell game using the A* search algorithm.
    It initializes the open set with the initial game state and iteratively explores
    the possible moves to find the solution. The heuristic function is used to estimate
    the cost of reaching the goal from the current state."""

    # Initialize the open set (priority queue) with the initial game state
    open_set = []
    heapq.heappush(open_set, (game.heuristic(), 0, game))
    
    # Dictionary to keep track of the path
    came_from = {}
    
    # Dictionary to keep track of the cost of the cheapest path to a node
    g_score = {game: 0}
    
    # Dictionary to keep track of the estimated cost of the cheapest path through a node
    f_score = {game: game.heuristic()}

    while open_set:
        # Get the node in open_set with the lowest f_score
        _, current_g, current = heapq.heappop(open_set)

        # If the current state is the goal, reconstruct and return the path
        if current.is_solved():
            return reconstruct_path(came_from, current)

        # Iterate through the possible moves from the current state
        for move in current.get_possible_moves():
            type_of_move=move.move_type
            if type_of_move!="foundation_to_freecell" and type_of_move!="foundation_to_tableau":
                # Apply the move to get the neighbor state
                neighbor = current.copy().apply_move(move,True)
                tentative_g_score = current_g + 0.001

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, move)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.heuristic()
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

    # If the open set is empty but the goal was never reached, return None
    return None


def solve_game_bfs(game):
    """
    Attempts to solve the Freecell game using breadth-first search (BFS).
    It explores the state space level by level without using heuristics.
    If a solution is found, it reconstructs and returns the path of moves.
    Otherwise, returns None.
    """

    initial_state = game.copy()
    queue = deque()
    queue.append((initial_state, 0))  # Tuple: (state, depth)
    came_from = {}  # To reconstruct the path: {child_state: (parent_state, move)}
    visited = set()
    visited.add(initial_state)
    
    while queue:
        current, depth = queue.popleft()
        
        # Debug: Print the current depth and state
        print(f"Exploring depth {depth}, current state: {current}")

        # Check if we've reached the solved state.
        if current.is_solved():
            print("Solution found!")
            return reconstruct_path(came_from, current)
        
        # Iterate over all possible moves from the current state.
        for move in current.get_possible_moves():
            type_of_move = move.move_type
            if type_of_move != "foundation_to_freecell" and type_of_move != "foundation_to_tableau":
                neighbor = current.copy()
                neighbor.apply_move(move,True)
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, move)
                    queue.append((neighbor, depth + 1))
                    # Debug: Print the move and new state
                    print(f"Move applied: {move}, new state: {neighbor}")
    
    # If no solution was found
    print("No solution found.")
    return None


def solve_game_dfs(game):

    print("Unnavailable: DFS under construction.")
    return None


# Auxiliary functions -----------------------------------------------------------------------------------------------------------------------------


def reconstruct_path(came_from, current):
    # Reconstruct the path from the goal to the start
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()  # Reverse the path to get it from start to goal

    # Print the total path length
    print(f"{len(total_path)}\n")
    
    # Write the total path to a file
    with open("solution_path.txt", "w") as file:
        for move in total_path:
            file.write(f"{move}\n")

    return total_path
