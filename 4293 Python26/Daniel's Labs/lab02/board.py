_EMPTY = ' ' # Used to indicate empty spaces in the board

class InvalidMoveError(ValueError):
    pass

class ConnectFourBoard:

    """Represents a Connect 4 board. Handles board state and checks moves for validity."""

    def __init__(self, num_rows, num_cols): #constructor method. self: the instance being created (passed automatically)
        """Initialize a new board"""
        self.num_rows = num_rows #the number of rows in the board will be accessible anywhre in the class using self.num_rows
        self.num_cols = num_cols #the number of columns in the board will be accessible anywhre in the class using self.num_cols
        self.clear() #This will initialize the board grid with empty spaces (calls the instance method defined below).

    def clear(self): #instance method
        """Replace all pieces with empty spaces."""
        self.rows = list() #Creates an empty list where self.rows can be used by other methods in the class.
        for row in range(self.num_rows): # Loop that runs once for each row index from 0 to num_rows - 1.
            self.rows.append([_EMPTY for col in range(self.num_cols)])# For each row, appends a list of _EMPTY strings representing empty cells in that row. each row is a list with num_cols empty spaces.

    def display(self): #instance method
        """Display the current board state"""
        for row in range(self.num_rows): # Loop that runs once for each row index from 0 to num_rows - 1.
            print(f'\t|{"|".join(self.rows[row])}|') #Displays each row with '|' between each cell | | |X|O| | | |
        print('\t ' + ' '.join([str(col) for col in range(self.num_cols)]))

    def check_winner(self): #instance method
        """Check whether someone has won the game."""
        # TODO: Implement this function instead of just returning false
        for row in range(self.num_rows): # Go through each row
            for col in range(self.num_cols):# For each row, go through each column
                symbol = self.rows[row][col]# Get the symbol at the current position
                if symbol is _EMPTY:
                    continue # Skip empty cells

                # Check horizontal
                if col + 3 < self.num_cols: #
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
     
    def is_full(self): #instance method
        """Check whether the board is full."""
        # TODO: Implement this function instead of just returning false
        for row in range(self.num_rows): 
            for col in range(self.num_cols):
                if self.rows[row][col] is _EMPTY:
                    return False # If any cell is empty, the board is not full
        return True # If no empty cells were found, the board is full
                   
    def add_piece(self, col, symbol): #instance method
        """Add a piece to the specified column."""
        # TODO: Add code to check if the move is valid (and raise InvalidMoveError if not)
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

# board = ConnectFourBoard(6, 7) this is an example of how to create an object of the class ConnectFourBoard
# board.display() this is an example of how to call the display method on the object board 


