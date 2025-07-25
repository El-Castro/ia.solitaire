from collections import deque
import time
import tracemalloc
import FreecellMove as fcm
import heapq
from FreecellState import FreecellState



# A Star ------------------------------------------------------------------------------------------------------------------------------------------------------


def solve_game_astar(game):
    """Solve the Freecell game using the A* search algorithm.
    The algorithm uses a priority queue (open set) to explore game states,
    guided by a heuristic function that estimates the cost to reach the goal.
    It iteratively evaluates possible moves until a solution is found or all
    states are explored."""
    start_time = time.time()  # Start timer
    tracemalloc.start()  # Start memory tracking
    isDone=False

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
                isDone=True
                end_time = time.time()  # End timer
                current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
                tracemalloc.stop()  # Stop memory tracking

                print(f"Solution found in {end_time - start_time:.4f} seconds!")
                print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")

                with open("statistics_astar.txt", "w") as file:
                    file.write(f"Number of states explored: {len(g_score)}\n")
                    file.write(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB\n")
                    file.write(f"Time taken: {end_time - start_time:.4f} seconds\n")

                return reconstruct_path_astar(came_from, current)

            # Iterate through the possible moves from the current state
            for move in current.get_possible_moves_Astar():
                # Apply the move to get the neighbor state
                neighbor = current.copy().apply_move(move, True)
                neighbor = fcm.apply_automatic_moves(neighbor)
                tentative_g_score = current_g + 1

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, move)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.heuristic()
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

            for src, dest, num_cards in fcm.get_possible_supermoves(current):
                neighbor = current.copy()
                neighbor = fcm.execute_supermove(neighbor, src, dest, num_cards, True)
                supermove = f"Supermove(source={src}, destination={dest}, number of cards={num_cards})"
                # Apply the move to get the neighbor state
                neighbor = fcm.apply_automatic_moves(neighbor)
                tentative_g_score = current_g + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, supermove)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.heuristic()
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

        #If the open set is empty but the goal was never reached
        return None

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    finally:
        if not isDone:
            current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
            tracemalloc.stop()
            print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")


# BFS ---------------------------------------------------------------------------------------------------------------------------------------------------------


def solve_game_bfs(game):
    """
    Solves the Freecell game using breadth-first search (BFS).
    This algorithm explores the state space level by level, ensuring that the
    shallowest solution is found first. It does not use heuristics to guide the search.
    If a solution is found, it reconstructs and returns the sequence of moves.
    If no solution exists, it returns None.
    """
    start_time = time.time()  # Start timer
    tracemalloc.start()  # Start memory tracking
    isDone=False

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
            print(f"{len(visited)}")

            # Check if we've reached the solved state.
            if current.is_solved():
                isDone=True
                end_time = time.time()  # End timer
                current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
                tracemalloc.stop()  # Stop memory tracking

                print(f"Solution found in {end_time - start_time:.4f} seconds!")
                print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
                with open("statistics_bfs.txt", "w") as file:
                    file.write(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB\n")
                    file.write(f"Time taken: {end_time - start_time:.4f} seconds\n")
                    file.write(f"Depth of solution: {depth}\n")
                    file.write(f"Number of states explored: {len(visited)}\n")
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
                neighbor = fcm.execute_supermove(neighbor, src, dest, num_cards, True)
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
        if not isDone:
            current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage
            tracemalloc.stop()
            print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")


# DFS ---------------------------------------------------------------------------------------------------------------------------------------------------------


def solve_game_dfs(game, max_depth=45):
    """
    Solves the Freecell game using depth-first search (DFS) with a specified depth limit.
    The algorithm explores possible moves in a depth-first manner, backtracking when necessary.
    If a solution is found within the depth limit, it reconstructs and returns the sequence of moves.
    If no solution is found it returns None.
    """
    max_depth_reached = 0
    start_time = time.time()
    tracemalloc.start()
    isDone=False

    try:
        initial_state = game.copy()
        stack = [(initial_state, 0)]  # (state, depth)
        came_from = {}
        visited = set()
        visited.add(initial_state)

        while stack:
            current, depth = stack.pop()
            max_depth_reached = max(max_depth_reached, depth)
            print(f"Depth {depth}")
            print(f"{len(visited)}")

            if current.is_solved():
                isDone=True
                end_time = time.time()
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                print(f"Solution found in {end_time - start_time:.4f} seconds!")
                print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
                with open("statistics_dfs.txt", "w") as file:
                    file.write(f"Max depth reached: {max_depth_reached}\n")
                    file.write(f"States explored: {len(visited)}\n")
                    file.write(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB\n")
                    file.write(f"Time taken: {end_time - start_time:.4f} seconds\n")
                return reconstruct_path_dfs(came_from, current)

            if depth >= max_depth:
                continue  # Skip expanding this node

            for move in current.get_possible_moves(True):
                type_of_move = move.move_type
                if type_of_move not in ("foundation_to_freecell", "foundation_to_tableau"):
                    neighbor = current.copy().apply_move(move, True)
                    neighbor = fcm.apply_automatic_moves(neighbor)

                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = (current, move)
                        stack.append((neighbor, depth + 1))

            for src, dest, num_cards in fcm.get_possible_supermoves(current):
                neighbor = current.copy()
                neighbor = fcm.execute_supermove(neighbor, src, dest, num_cards, True)
                supermove = f"Supermove(source={src}, destination={dest}, number of cards={num_cards})"
                neighbor = fcm.apply_automatic_moves(neighbor)

                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, supermove)
                    stack.append((neighbor, depth + 1))

        print("No solution found.")
        return None

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    finally:
        if not isDone:
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"Peak memory usage: {peak_mem / 1024 / 1024:.4f} MB")
            print(f"Maximum depth reached: {max_depth_reached}")


# Auxiliary functions -----------------------------------------------------------------------------------------------------------------------------------------


def reconstruct_path_bfs(came_from, current):
    """
    Reconstructs the path from the goal to the start using the BFS algorithm's `came_from` mapping.
    """
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
    """
    Reconstructs the path from the goal to the start using the A* algorithm's `came_from` mapping.
    """
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

def reconstruct_path_dfs(came_from, current):
    """
    Reconstructs the path from the goal to the start using the DFS algorithm's `came_from` mapping.
    """
    total_path = []
    while current in came_from:
        current, move = came_from[current]
        total_path.append(move)
    total_path.reverse()  # Reverse the path to get it from start to goal

    # Print the total path length
    print(f"{len(total_path)}\n")
    
    # Write the total path to a file
    with open("solution_path_dfs.txt", "w") as file:
        for move in total_path:
            file.write(f"{move}\n")

    return total_path


# Functions for A* weight testing --------------------------------------------------------------------------------------------------------------------------------------------------------

 
import itertools
import csv
import os
from concurrent.futures import ProcessPoolExecutor, TimeoutError
 

# Helper: float range generator.
def frange(start, stop, step):
    x = start
    while x <= stop + 1e-9:
        yield round(x, 2)
        x += step


def run_astar_with_weights(game, foundation_weight, fc_weight, fcol_weight, blocked_weight, modifier):
    game.set_heuristic_weights(foundation_weight, fc_weight, fcol_weight, blocked_weight, modifier)
    start_time = time.time()
    path = solve_game_astar(game)
    elapsed = time.time() - start_time
    cost = len(path) if path is not None else float('inf')
    return (foundation_weight, fc_weight, fcol_weight, blocked_weight, modifier, cost, elapsed)
 

def grid_search(game, weight_ranges, timeout, results_file="heuristic_test_results.csv"):
    """
    Searches over combinations of heuristic weights.
    weight_ranges is a dict with keys:
    'foundation', 'fc', 'fcol', 'blocked', 'modifier'
    each as a tuple: (start, stop, step)
    timeout: maximum time (in seconds) allowed per combination.
    """
    best = None
    best_combos = []
    all_combos = list(itertools.product(
        frange(*weight_ranges['foundation']),
        frange(*weight_ranges['fc']),
        frange(*weight_ranges['fcol']),
        frange(*weight_ranges['blocked']),
        frange(*weight_ranges['modifier'])
    ))
    results = []
    timeouts = 0

    file_exists = os.path.exists(results_file)

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(run_astar_with_weights, game.copy(), *combo): combo for combo in all_combos}

        with open(results_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header if it's the first time
            if not file_exists:
                writer.writerow(['foundation', 'fc', 'fcol', 'blocked', 'modifier', 'cost', 'elapsed'])

        for future in futures:
            try:
                result = future.result(timeout=timeout)
                if result:
                    results.append(result)
                    #print("Tested combo:", result)
                    cost = result[5]
                    combo = result[:5]
                    print("Combo:", combo, "Cost:", cost, "Elapsed:", result[6])
                    # Write the combo and the cost + elapsed time to CSV
                    try:
                        with open("heuristic_test_results.csv", mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(combo + (cost, result[6]))  # Add cost and elapsed time to the row
                    except Exception as e:
                        print("Error writing to CSV:", e)
    
                    if best is None or cost < best:
                        best = cost
                        best_combos = [combo]
                    elif cost == best:
                        best_combos.append(combo)
                        
            except TimeoutError:
                print("Timeout for combination", futures[future])
                timeouts += 1
            except Exception as e:
                print("Error for combination", futures[future], ":", e)

    return best_combos, best, results