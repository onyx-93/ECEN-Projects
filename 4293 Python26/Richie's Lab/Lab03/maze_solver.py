import numpy as np
from maze import Maze
import queue
from collections import deque

_FLOOR = True
_WALL = False

# TODO: Write code to compute a solution to the maze.
class MazeSolver:
    """
    Solver for a Maze object.
    Responsible for finding a path from start to goal.
    """

    def __init__(self, maze):
        """
        Store the maze and initialize solver state
        """
        self.maze = maze.maze                  # The boolean maze grid
        self.shape = maze.shape                # Dimensions of the maze
        self.start = maze.start_position       # Logical start position
        self.goal = maze.goal_position         # Logical goal position

        # Unpack start and endpoints

        sx, sy = self.start
        gx, gy = self.goal

        # Convert logical positions to grid coordinates (2*x + 1 mapping)
        self.start_cell = (2*sx + 1, 2*sy + 1)      # TODO: compute grid start
        self.goal_cell = (2*gx + 1, 2*gy + 1)       # TODO: compute grid goal

        # Track visited cells to avoid revisiting
        self.visited = set()                # TODO: initialize visited structure

        # Store parent relationships for path reconstruction
        self.parent = {}                       # child_cell -> parent_cell

    def solve(self):
        """
        Main entry point for solving the maze.
        Chooses search strategy and returns a path if found.
        """
        
        frontier = deque()
        frontier.append(self.start_cell)
        self.visited.add(self.start_cell)
       
        while frontier:
            current = frontier.popleft()
            
            # If the cell is the goal finish
            if current == self.goal_cell:
                return self.reconstruct_path()
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parent[neighbor] = current
                    frontier.append(neighbor)
        return None # No solution found

    def get_neighbors(self, cell):
        """
        Given a grid cell, return reachable neighboring cells.
        """
        neighbors = []
        row, col = cell
        # Moving directions move in four different directions
        directions = [(-1 , 0), (1 , 0), (0 , -1), (0 , 1)]
        # Move in all directions
        for dr, dc in directions:
            r = row + dr
            c = col + dc
        # Check for boundary conditions
            if (0 <= r < self.shape[0] and 0 <= c < self.shape[1] and self.maze[r][c] == _FLOOR):
                neighbors.append((r, c))
        return neighbors

    def reconstruct_path(self):
        """
        Reconstruct path from goal to start using parent links.
        """
        path = []
        current = self.goal_cell
        while current != self.start_cell:
            path.append(current)
            if current not in self.parent:
                return None
            current = self.parent[current]
        path.append(self.start_cell)
        path.reverse()
        return path

    def mark_path_on_maze(self, path):
        """
        Optional: mark the solution path on the maze for display.
        """
        for r, c in path:
            self.maze[r][c] = True
        pass

    def displayS(self, path=None):

        str_maze = np.full(self.shape, '  ', dtype=object)

        for r in range(self.shape[0]):
            for c in range(self.shape[1]):
                if self.maze[r, c]:
                    str_maze[r, c] = '▒▒' # Floor empty
                else:
                    str_maze[r, c] = '██' # Wall
        if path:
            for r, c in path:
                str_maze[r, c] = '::' # Solution path
        
        print("Start")
        for row in str_maze:
            print(''.join([c for c in row]))
        print(' '*(self.shape[0]-3), "Finish")

m = Maze(7)
solver = MazeSolver(m)

path = solver.solve()


# The code block below has been commented out since the interactive maze utilizes this maze solution, leaving this block uncommented will print a different maze solved in the terminal which is undesired.
# Else it can be uncommented

# if path:
#     print("\n\tSolution\n")
#     solver.displayS(path)
#     print("\n\tNon-Solved Maze\n")
#     m.display()
#     print()
# else:
#     print("No solution found")

# This code was built and approached using generative AI, since the maze code and the development of the same seems messy and not friendly to begginers in programming like me.
# AI proved to be a fantastic tool to understand the maze code, to then give structure, and solution to the maze created. 

