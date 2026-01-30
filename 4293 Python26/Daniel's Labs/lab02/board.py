_EMPTY = ' ' # Used to indicate empty spaces in the board

class InvalidMoveError(ValueError):
    pass

class ConnectFourBoard:

    """Represents a Connect 4 board. Handles board state and checks moves for validity."""

    def __init__(self, num_rows, num_cols): #constructor method. self: the instance being created (passed automatically)
        """Initialize a new board"""
        self.num_rows = num_rows #the number of rows in the board will be accessible anywhre in the class using self.num_rows
        self.num_cols = num_cols #the number of columns in the board will be accessible anywhre in the class using self.num_cols
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
        for row in range(self.num_rows): # Go through each row
            for col in range(self.num_cols):# For each row, go through each column
                symbol = self.rows[row][col]# Get the symbol at the current position
                if symbol is _EMPTY:
                    continue # Skip empty cells

                # Check horizontal
                if col + 3 < self.num_cols:
                    if (self.rows[row][col + 1] == symbol and
                        self.rows[row][col + 2] == symbol and
                        self.rows[row][col + 3] == symbol):
                        return True

                # Check vertical
                if row + 3 < self.num_rows:
                    if (self.rows[row + 1][col] == symbol and
                        self.rows[row + 2][col] == symbol and
                        self.rows[row + 3][col] == symbol):
                        return True

                # Check diagonal down-right
                if row + 3 < self.num_rows and col + 3 < self.num_cols:
                    if (self.rows[row + 1][col + 1] == symbol and
                        self.rows[row + 2][col + 2] == symbol and
                        self.rows[row + 3][col + 3] == symbol):
                        return True

                # Check diagonal up-right
                if row - 3 >= 0 and col + 3 < self.num_cols:
                    if (self.rows[row - 1][col + 1] == symbol and
                        self.rows[row - 2][col + 2] == symbol and
                        self.rows[row - 3][col + 3] == symbol):
                        return True 
        return False
     
    def is_full(self):
        """Check whether the board is full."""
        for row in range(self.num_rows): 
            for col in range(self.num_cols):
                if self.rows[row][col] is _EMPTY:
                    return False # If any cell is empty, the board is not full
        return True # If no empty cells were found, the board is full
                   
    def add_piece(self, col, symbol):
        """Add a piece to the specified column."""
        if col < 0 or col >= self.num_cols:
            raise InvalidMoveError(f'Column {col} is out of bounds.')
        if self.rows[0][col] is not _EMPTY:
            raise InvalidMoveError(f'Column {col} is full.')
        if symbol is _EMPTY:
            raise InvalidMoveError('Cannot add an empty piece to the board.')
        
           
        # Find the first empty row in col and replace it with symbol
        for row in reversed(range(self.num_rows)):
            if self.rows[row][col] is _EMPTY:
                self.rows[row][col] = symbol
                break

