from collections import deque
import time
import tracemalloc
import FreecellMove as fcm
import heapq
from FreecellState import FreecellState



# A Star ------------------------------------------------------------------------------------------------------------------------------------------------------


def solve_game_astar(game):
    """This function attempts to solve the Freecell game using the A* search algorithm.
    It initializes the open set with the initial game state and iteratively explores
    the possible moves to find the solution. The heuristic function is used to estimate
    the cost of reaching the goal from the current state."""
    start_time = time.time()  # Start timer
    tracemalloc.start()  # Start memory tracking

    try:
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
            print(f"Open set size: {len(open_set)}")
            # Get the node in open_set with the lowest f_score
            _, current_g, current = heapq.heappop(open_set)

            # If the current state is the goal, reconstruct and return the path
            if current.is_solved():
                end_time = time.time()  # End timer
                current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
                tracemalloc.stop()  # Stop memory tracking

                print(f"Solution found in {end_time - start_time:.4f} seconds!")
                print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
                return reconstruct_path_astar(came_from, current)

            # Iterate through the possible moves from the current state
            for move in current.get_possible_moves_Astar():
                # Apply the move to get the neighbor state
                neighbor = current.copy().apply_move(move, True)
                neighbor = fcm.apply_automatic_moves(neighbor)
                tentative_g_score = current_g + 1# + len(auto_moves)

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, move)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.heuristic()
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

            # for src, dest, num_cards in fcm.get_possible_supermoves(current):
            #     neighbor = current.copy()
            #     neighbor = fcm.execute_supermove(neighbor, src, dest, num_cards)
            #     supermove = f"Supermove(source={src}, destination={dest}, number of cards={num_cards})"
            #     # Apply the move to get the neighbor state
            #     neighbor = fcm.apply_automatic_moves(neighbor)
            #     tentative_g_score = current_g + 1

            #     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
            #         came_from[neighbor] = (current, supermove)
            #         g_score[neighbor] = tentative_g_score
            #         f_score[neighbor] = tentative_g_score + neighbor.heuristic()
            #         heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

        # If the open set is empty but the goal was never reached, return None
        return None

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    finally:
        current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
        tracemalloc.stop()
        print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")


# BFS ---------------------------------------------------------------------------------------------------------------------------------------------------------


def solve_game_bfs(game):
    """
    Attempts to solve the Freecell game using breadth-first search (BFS).
    It explores the state space level by level without using heuristics.
    If a solution is found, it reconstructs and returns the path of moves.
    Otherwise, returns None.
    """
    start_time = time.time()  # Start timer
    tracemalloc.start()  # Start memory tracking

    try:
        initial_state = game.copy()
        queue = deque()
        queue.append((initial_state, 0))  # Tuple: (state, depth)
        came_from = {}  # To reconstruct the path: {child_state: (parent_state, move)}
        visited = set()
        visited.add(initial_state)

        while queue:
            current, depth = queue.popleft()

            # Debug: Print the current depth and state
            print(f"{depth}")

            # Check if we've reached the solved state.
            if current.is_solved():
                end_time = time.time()  # End timer
                current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
                tracemalloc.stop()  # Stop memory tracking

                print(f"Solution found in {end_time - start_time:.4f} seconds!")
                print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
                return reconstruct_path_bfs(came_from, current)

            # Iterate over all possible moves from the current state.
            for move in current.get_possible_moves(True):
                type_of_move = move.move_type
                if type_of_move != "foundation_to_freecell" and type_of_move != "foundation_to_tableau":
                    neighbor = current.copy().apply_move(move, True)
                    neighbor=fcm.apply_automatic_moves(neighbor)

                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = (current, move)
                        queue.append((neighbor, depth + 1))
                        # Debug: Print the move and new state

            for src, dest, num_cards in fcm.get_possible_supermoves(current):
                neighbor = current.copy()
                neighbor = fcm.execute_supermove(neighbor, src, dest, num_cards)
                supermove = f"Supermove(source={src}, destination={dest}, number of cards={num_cards})"
                neighbor = fcm.apply_automatic_moves(neighbor)

                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, supermove)
                    queue.append((neighbor, depth + 1))
                    # Debug: Print the move and new state

        # If no solution was found
        print("No solution found.")
        return None

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    finally:
        current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
        tracemalloc.stop()
        print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")


# DFS ---------------------------------------------------------------------------------------------------------------------------------------------------------
def solve_game_dfs(game):
    start_time = time.time()
    tracemalloc.start()

    initial_state = game.copy()
    stack = [(initial_state, [], 0)]  # (state, path_so_far, depth)
    visited = set()
    visited.add(initial_state)

    max_depth = 0
    visited_count = 1

    while stack:
        current, path, depth = stack.pop()

        # Print depth at every step
        print(f"Exploring depth: {depth}, visited nodes: {visited_count}")

        if depth > max_depth:
            max_depth = depth

        if current.is_solved():
            end_time = time.time()
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print(f"Solution found with DFS in {end_time - start_time:.4f} seconds!")
            print(f"States visited: {visited_count}")
            print(f"Max depth reached: {max_depth}")
            print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
            return path

        for move in current.get_possible_moves(True):
            if move.move_type in {"foundation_to_freecell", "foundation_to_tableau"}:
                continue

            next_state = current.copy().apply_move(move, True)
            next_state = fcm.apply_automatic_moves(next_state)

            if next_state not in visited:
                visited.add(next_state)
                visited_count += 1
                stack.append((next_state, path + [move], depth + 1))

    print("No solution found for DFS.")
    print(f"Total states visited: {visited_count}")
    print(f"Max depth reached: {max_depth}")
    return None

# Auxiliary functions -----------------------------------------------------------------------------------------------------------------------------------------


def reconstruct_path_bfs(came_from, current):
    # Reconstruct the path from the goal to the start
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()  # Reverse the path to get it from start to goal

    # Print the total path length
    print(f"{len(total_path)}\n")
    
    # Write the total path to a file
    with open("solution_path_bfs.txt", "w") as file:
        for move in total_path:
            file.write(f"{move}\n")

    return total_path

def reconstruct_path_astar(came_from, current):
    # Reconstruct the path from the goal to the start
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()  # Reverse the path to get it from start to goal

    # Print the total path length
    print(f"{len(total_path)}\n")
    
    # Write the total path to a file
    with open("solution_path_astar.txt", "w") as file:
        for move in total_path:
            file.write(f"{move}\n")

    return total_path