import numpy as np
from maze import Maze
from queue import PriorityQueue

# TODO: Write code to compute a solution to the maze.
'''“The A* algorithm was adapted from a grid-based
    pathfinding implementation and rewritten to
    operate on the maze’s boolean grid representation.”'''
    


def heuristic(a, b):
    """Manhattan distance heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, maze):
    """Return valid neighboring cells"""
    x, y = pos
    neighbors = []

    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy

        if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1]:
            if maze[nx, ny]:  # floor, not wall
                neighbors.append((nx, ny))

    return neighbors


def reconstruct_path(came_from, current):
    """Reconstruct path from start to goal"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def solve_maze_astar(maze, start, goal):
    """
    A* pathfinding on a boolean maze.
    Returns a list of (x, y) positions from start to goal.
    """

    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, maze):
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return None  # No path found
