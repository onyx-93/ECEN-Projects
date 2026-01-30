_EMPTY = ' ' # Used to indicate empty spaces in the board

class InvalidMoveError(ValueError):
    pass

class ConnectFourBoard:

    """Represents a Connect 4 board. Handles board state and checks moves for validity."""

    def __init__(self, num_rows, num_cols):
        """Initialize a new board"""
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.clear()

    def clear(self):
        """Replace all pieces with empty spaces."""
        self.rows = list()
        for row in range(self.num_rows):
            self.rows.append([_EMPTY for col in range(self.num_cols)])

    def display(self):
        """Display the current board state"""
        for row in range(self.num_rows):
            print(f'\t|{"|".join(self.rows[row])}|')
        print('\t ' + ' '.join([str(col) for col in range(self.num_cols)]))

    def check_winner(self):
        """Check whether someone has won the game."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # List of tuples (vectors) for directions left, down, diagonals
        for r in range(self.num_rows):
            for c in range(self.num_cols): # Loops through matrix to read spaces and detect which one is empty
                piece = self.rows[r][c]
                if piece == _EMPTY:
                    continue

                for dr, dc in directions: # If the cell is not empty scan all four directions to check for valid win
                    r_end = r + 3 * dr
                    c_end = c + 3 * dc
                    if not (0 <= r_end < self.num_rows and 0 <= c_end < self.num_cols):
                        continue
                    if all (self.rows[r + k*dr][c + k*dc] == piece for k in range(4)): 
                        return True
                    
        return False

    def is_full(self):
        """Check whether the board is full."""
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.rows[r][c] == _EMPTY:   # Loop through the entire grid to scan for empty spaces
                    return False
                
        return True

    
    def add_piece(self, col, symbol):
        """Add a piece to the specified column."""
        if not isinstance(col, int): # If input is not an integer
            raise InvalidMoveError("Column must be an integer.")
        if col < 0 or col >= self.num_cols: # If input is integer out of bounds
            raise InvalidMoveError(f"Column must be between 0 and {self.num_cols - 1}.")
        
        if self.rows[0][col] != _EMPTY:
            raise InvalidMoveError("That column is full.")

        for row in range(self.num_rows -1, -1, -1):
            if self.rows[row][col] == _EMPTY:
                self.rows[row][col] = symbol
                return
            