import matplotlib.pyplot as plt
import numpy as np
from maze import Maze
from maze_solver import MazeSolver

# Logical operators for walls and floor
_FLOOR = True
_WALL = False 

# Disable s key, my god that sh*t is annoying
plt.rcParams['keymap.save'].remove('s')

def main():
    
    m = Maze(5)
    grid = m.maze # Boolean array

    solver = MazeSolver(m)
    solution_path = solver.solve()

    # Initialize x, and y coordinates
    # Unpack tuple fromthe maze class object
    sx, sy = m.start_position
    gx, gy = m.goal_position

    start_cell = (2*sx + 1, 2*sy + 1)
    goal_cell = (2*gx + 1, 2*gy + 1)

    fig, ax = plt.subplots()
    controls_layout = ax.text(
        0.01, 0.01,
        "Movement:  arrows / WASD  |  H: Hint  |  R: Restart  |  Q/Esc: Quit",
        transform=ax.transAxes,
        ha="left", va="bottom",
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", alpha=0.5, edgecolor="none")
    )
    win_message = ax.text(
        0.5, 0.5,
        "YOU WON!\n[R]estart or [Q]uit",
        transform=ax.transAxes,
        ha="center", va="center",
        fontsize=25,
        color="black",
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="gray")
    )
    win_message.set_visible(False)
    ax.imshow(grid, cmap='gray_r', interpolation="nearest")
    # imshow() uses (x=column, y=row), so when plotting we must inver order
    start_r, start_c = start_cell
    goal_r, goal_c = goal_cell

    ax.scatter(start_c, start_r, c='red', s=50, label="Start")
    ax.scatter(goal_c, goal_r, c='green', s=50, label="Goal")

    # Start coordinates

    player_r, player_c = start_cell
    goal_r, goal_c = goal_cell

    if solution_path is not None:
        path_rows = [r for (r, c) in solution_path]
        path_cols = [c for (r, c) in solution_path]
        hint_line_list = ax.plot(
            path_cols, path_rows,
            color="beige",
            linewidth=1.5,
            alpha=0.6,
            label="Hint path"
    )
        hint_line = hint_line_list[0]
    else:
        hint_line = None

    if hint_line is not None:
        hint_line.set_visible(False)



    player = ax.scatter(start_c, start_r, c='white', s=60, label="Player")

    ax.set_title("Terracota Maze", fontsize=20)
    ax.axis("off")
    pos = ax.get_position()
    ax.set_position([pos.x0, pos.y0, pos.width * 0.85, pos.height])
    ax.legend(loc="center left",
              bbox_to_anchor=(1.02, 0.5),
              borderaxespad=0.
              )
    # Take input:

    game_over = False
    hint_visible = False

    def on_input_key(event):
        nonlocal player_r, player_c, game_over, hint_visible

        key = event.key
        dr, dc = 0, 0

        if key == "h":
            if hint_line is not None:
              hint_visible = not hint_visible
              hint_line.set_visible(hint_visible)
              event.canvas.draw_idle()
            return


        if game_over:
            if key in ("q", "escape"):
                plt.close(event.canvas.figure)
            elif key in ("r",):
                restart_game()
            return


        if key in ("w", "up"):
            dr, dc = -1, 0
        elif key in("s", "down"):
            dr, dc = 1, 0
        elif key in ("a", "left"):
            dr, dc = 0, -1
        elif key in ("d", "right"):
            dr, dc = 0, 1
        else:
            return
        
        # Update position

        new_r = player_r + dr
        new_c = player_c + dc

        # Boundary conditons
        if not (0 <= new_r < grid.shape[0] and 0 <= new_c < grid.shape[1]):
            return
        
        if not grid[new_r, new_c] == _FLOOR:
            return
        
        player_r, player_c = new_r, new_c
        player.set_offsets([[player_c, player_r]])
        event.canvas.draw_idle()
    
        # Winning condition
        if (player_r, player_c) == (goal_r, goal_c):
            game_over = True
            win_message.set_visible(True)
            event.canvas.draw_idle()

    # Restart game
    def restart_game():
        plt.close(fig)
        main()

    fig.canvas.mpl_connect('key_press_event', on_input_key)
    plt.show()



if __name__ == "__main__":
    # Any code in this block will be run when this file is executed directly
    print("You must have run `python interactive_maze.py`")
    main()