# interactiv_maze
import matplotlib.pyplot as plt
import numpy as np
from maze import Maze
from maze_solver import solve_maze_astar

def draw_maze(ax, maze):
    # Walls = 0 (black), floors = 1 (white)
    img = np.where(maze.maze, 1, 0)
    ax.imshow(img, cmap="gray")

def draw_solution(ax, path):
    if path is None:
        return

    ys = [p[0] for p in path]
    xs = [p[1] for p in path]

    ax.plot(xs, ys, color="blue", linewidth=2, label="Solution")

def draw_player_and_goal(ax, player_pos, goal_pos):
    ax.scatter(player_pos[1], player_pos[0], c="red", s=100, label="Player")
    ax.scatter(goal_pos[1], goal_pos[0], c="green", s=100, label="Goal")

def interactive_maze():
    maze = Maze(16)

    player_pos = maze.start_position
    goal_pos = maze.goal_position

    solution_path = solve_maze_astar(
        maze.maze,
        player_pos,
        goal_pos
    )

    show_solution = False

    fig, ax = plt.subplots()
    plt.title("Maze Game")

    def redraw():
        ax.clear()
        draw_maze(ax, maze)
        draw_player_and_goal(ax, player_pos, goal_pos)

        if show_solution:
            draw_solution(ax, solution_path)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.text(
            0, -1,
            "W/A/X/D: Move   H: Toggle solution   Q: Quit",
            fontsize=10
        )

        plt.draw()

    def on_key(event):
        nonlocal player_pos, show_solution

        x, y = player_pos
        new_pos = player_pos

        if event.key == 'w':
            new_pos = (x - 1, y)
        elif event.key == 'x':
            new_pos = (x + 1, y)
        elif event.key == 'a':
            new_pos = (x, y - 1)
        elif event.key == 'd':
            new_pos = (x, y + 1)
        elif event.key == 'h':
            show_solution = not show_solution
        elif event.key == 'q':
            plt.close()
            return

        # Validate move
        if (0 <= new_pos[0] < maze.maze.shape[0] and
            0 <= new_pos[1] < maze.maze.shape[1] and
            maze.maze[new_pos]):
            player_pos = new_pos

        # Success check
        if player_pos == goal_pos:
            ax.clear()
            draw_maze(ax, maze)
            draw_solution(ax, solution_path)
            draw_player_and_goal(ax, player_pos, goal_pos)
            ax.text(
                maze.maze.shape[1]//2,
                maze.maze.shape[0]//2,
                "🎉 YOU WIN! 🎉\nPress Q to quit",
                ha="center",
                va="center",
                fontsize=14,
                color="green"
            )
            plt.draw()
            return

        redraw()

    fig.canvas.mpl_connect('key_press_event', on_key)

    redraw()
    plt.show()


# TODO: Write code to make the maze interactive.

# TODO: Visualize the maze using matplotlib.

if __name__ == "__main__":
    interactive_maze()


# maze_solver ################
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





   while True:
            if event.key == 'y':
                # Restart the game
                interactive_maze()
                return
            elif event.key == 'n':
                plt.close(fig)
                return
