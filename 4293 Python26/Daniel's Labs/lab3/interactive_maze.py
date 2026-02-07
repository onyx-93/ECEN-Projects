import matplotlib.pyplot as plt
import numpy as np
from maze import Maze
from maze_solver import a_star, logical_to_grid

def interactive_maze():
    maze = Maze(16) # You can change the size here (e.g., Maze(8) for a larger maze)
    player_pos = maze.start_position
    goal_pos = maze.goal_position

    #get solution path for hint system
    solution_path = a_star(maze)
    if solution_path:
        solution_grid = solution_path 
    else:
        solution_grid = []

    # Convert to grid coordinates for drawing
    player_grid = logical_to_grid(player_pos)
    goal_grid = logical_to_grid(goal_pos)
    
    # FIX 2: Track game state to stop movement after winning
    game_over = False
    show_solution = False

    fig, ax = plt.subplots(figsize=(7,7))
    plt.title("Maze Game – WASD to move")

    def redraw():
        ax.clear()
        # Walls = 0 (black), floors = 1 (white)
        ax.imshow(np.where(maze.maze, 1, 0), cmap="gray", origin="upper")
        
        # Draw solution if requested AND it exists
        if show_solution and solution_grid:
            ys = [p[0] for p in solution_grid]
            xs = [p[1] for p in solution_grid]
            ax.plot(xs, ys, color="blue", linewidth=3, alpha=0.7)

        # Player & goal
        ax.scatter(player_grid[1], player_grid[0], c="red", s=200, marker="o", label="You")
        ax.scatter(goal_grid[1], goal_grid[0], c="lime", s=200, marker="*", label="Goal")

        ax.set_xticks([]); ax.set_yticks([])
        
        # Update UI based on state
        if game_over:
             ax.text(0.5, 0.5, "YOU WIN!\nDo you want to play again?\n YES (Y) / NO (N)",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=20, color="lime", bbox=dict(facecolor='black', alpha=0.8))
        else:
            ax.text(0.5, -0.08, "U: up  D: down  L: left  R: right   H: toggle hint   Q: quit",
                    transform=ax.transAxes, ha="center", fontsize=10)

        plt.draw()

    def on_key(event):
        # FIX 3: Include game_over in nonlocal scope
        nonlocal player_pos, player_grid, show_solution, game_over

        
        if event.key == 'y':
            plt.close(fig) # Close current figure before starting a new game
            interactive_maze() # Restart the game
            return
        
        elif event.key == 'n':
            plt.close(fig)
            return

        # Disable interaction if game is over
        if game_over:
            return

        if event.key == 'h':
            show_solution = not show_solution
            redraw()
            return

        # FIX 4: Renamed dx/dy to d_row/d_col for clarity (Row is Y-axis!)
        d_row, d_col = 0, 0
        if event.key ==   'u': d_row = -1  # Up (Row decreases)
        elif event.key == 'd': d_row = 1 # Down (Row increases)
        elif event.key == 'l': d_col = -1 # Left (Col decreases)
        elif event.key == 'r': d_col = 1 # Right (Col increases)
        else:
            return

        new_logical = (player_pos[0] + d_row, player_pos[1] + d_col)
        new_grid = logical_to_grid(new_logical)

        # Boundary and Wall Check
        if (0 <= new_grid[0] < maze.maze.shape[0] and
            0 <= new_grid[1] < maze.maze.shape[1] and
            maze.maze[new_grid[0], new_grid[1]]): # Assumes 1/True is floor

            player_pos = new_logical
            player_grid = new_grid

            if player_pos == goal_pos:
                game_over = True
            
            redraw()

    fig.canvas.mpl_connect('key_press_event', on_key)
    redraw()
    plt.show()

if __name__ == "__main__":
    interactive_maze()