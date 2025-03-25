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
    print(f"{len(total_path)}\n")
    return total_path

