import numpy as np
from maze import Maze
from queue import PriorityQueue

def logical_to_grid(pos):
    """
    Translates logical cell coordinates (row, col) to the actual 
    coordinate system used by the maze's underlying NumPy array.
    
    In this maze generation, logical cells are separated by walls, 
    so logical cell (0,0) maps to grid index (1,1).
    """
    x, y = pos
    return (2*x + 1, 2*y + 1)


def a_star(maze):
    """
    Finds the shortest path from start to goal using the A* Search Algorithm.
    
    This function uses a PriorityQueue to explore the most promising paths first,
    balancing the cost to reach a cell (g_score) with the estimated distance 
    to the goal (heuristic).
    """
    # Initialize start and end points in grid coordinates
    start = logical_to_grid(maze.start_position)
    goal  = logical_to_grid(maze.goal_position)

    # PriorityQueue stores tuples: (priority_score, coordinate)
    open_set = PriorityQueue()
    open_set.put((0, start))

    # Tracks the most efficient 'parent' of each cell to reconstruct the path later
    came_from = {}

    # g_score: The actual cost from the start to the current cell
    g_score = {start: 0}
    
    # f_score: The predicted total cost (g_score + heuristic)
    # This is the "priority" used by the PriorityQueue
    f_score = {start: heuristic(start, goal)}

    # A set to keep track of what's in the PriorityQueue for O(1) lookups
    open_set_hash = {start}

    while not open_set.empty():
        # Get the node with the lowest f_score
        current = open_set.get()[1]
        open_set_hash.remove(current)

        # Goal reached! Trace back the path
        if current == goal:
            return reconstruct_path(came_from, current)

        # Check all 4 directions (Up, Down, Left, Right)
        for neighbor in get_neighbors(current, maze.maze):
            # Assume a weight of 1 for every step in the maze
            tentative_g = g_score[current] + 1

            # If this path to neighbor is better than any previous one, record it
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return None # Return None if no path exists


def heuristic(a, b):
    """
    Calculates the 'Manhattan Distance' between two points.
    
    Since the player can only move in cardinal directions (no diagonals),
    this is the most accurate admissible heuristic for A*.
    """
    # a and b are (row, col) tuples
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    """
    Backtracks from the goal to the start using the parent links 
    stored in the 'came_from' dictionary.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse() # Reverse to get path from Start -> Goal
    return path

def get_neighbors(pos, maze):
    """
    Identifies walkable adjacent cells.
    
    Checks boundaries and ensures the cell is a 'floor' (True/1) 
    rather than a 'wall' (False/0).
    """
    x, y = pos
    neighbors = []

    # Adjacent movements: Down, Up, Right, Left
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy

        # Ensure we are inside the array boundaries
        if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1]:
            # IMPORTANT: maze[nx, ny] must be True to be walkable
            if maze[nx, ny]:  
                neighbors.append((nx, ny))

    return neighbors
