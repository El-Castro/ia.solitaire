import heapq

def solve_game(game):
    """This function attempts to solve the Freecell game using the A* search algorithm.
    It initializes the open set with the initial game state and iteratively explores
    the possible moves to find the solution. The heuristic function is used to estimate
    the cost of reaching the goal from the current state."""

    # Initialize the open set (priority queue) with the initial game state
    open_set = []
    heapq.heappush(open_set, (0 + game.heuristic(), 0, game))
    
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
            # Apply the move to get the neighbor state
            neighbor = current.copy().apply_move(move)
            neighbor.heuristic()
            tentative_g_score = current_g + 1

            # If this path to neighbor is better than any previous one, record it
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + neighbor.heuristic()
                heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

    # If the open set is empty but the goal was never reached, return None
    return None

def reconstruct_path(came_from, current):
    # Reconstruct the path from the goal to the start
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()  # Reverse the path to get it from start to goal
    return total_path

#dfs 
def dfs_solve(game):
    """Solves FreeCell using Depth-First Search (DFS)."""
    
    stack = [(game, [])]  # Stack stores (current game state, path of moves)
    visited = set()  # Set to track visited states

    while stack:
        current, path = stack.pop()  # Get the last added state (LIFO behavior)

        if current.is_solved():
            return path  # Return the sequence of moves leading to the solution

        # Avoid revisiting already explored game states
        if current in visited:  # Directly checking if state exists in set
            continue
        visited.add(current)  # Mark state as visited

        # Get all possible moves from the current state
        for move in current.get_possible_moves():
            new_game = current.copy().apply_move(move)  # Apply the move
            stack.append((new_game, path + [move]))  # Store new state with updated move history

    return None  # No solution found

"""
def dfs_solve(game):    
    # Base case: if the game is solved, return the move history
    if game.is_solved():
        return game.history  # Return the sequence of game states

    # Iterate through all possible moves
    for move in game.get_possible_moves():
        game.save_state()  # Save current state before applying the move
        game.apply_move(move)  # Apply the move

        result = dfs_solve(game)  # Recursive call

        if result:  # If a solution is found, return it
            return result
        
        game.undo()  # Backtrack if move didn't lead to a solution

    return None  # No solution found

"""



