import numpy as np
from maze import Maze
from queue import PriorityQueue

def logical_to_grid(pos):
    """Convert logical maze coordinates to grid coordinates"""
    x, y = pos
    return (2*x + 1, 2*y + 1)


def a_star(maze):
    start = logical_to_grid(maze.start_position)
    goal  = logical_to_grid(maze.goal_position)

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

        for neighbor in get_neighbors(current, maze.maze):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return None


def heuristic(a, b):
    # a and b are (row, col)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

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
