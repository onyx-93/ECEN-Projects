from board import ConnectFourBoard, InvalidMoveError
from player import ConsolePlayer, CPUPlayer


class ConnectFourGame:
    """Represents a Connect 4 game. Manages board and players."""

    def __init__(self, rows=6, cols=7, p1_type=ConsolePlayer, p2_type=ConsolePlayer, cpu_type=CPUPlayer, vs_cpu=False):
        """Initialize a new game"""

        # Set up board
        self.board = ConnectFourBoard(rows, cols)

        # Set up Players
        p1_symbol = self.get_player_symbol("Player 1")
        p2_symbol = self.get_player_symbol("Player 2")
      
        while p2_symbol == p1_symbol:
            print("Player 2 can't have the same symbol as Player 1!")
            p2_symbol = self.get_player_symbol("Player 2")
         
        # Player 1 is always human (ConsolePlayer by default)  "updated" 
        self.player_1 = p1_type(name='Player 1', symbol=p1_symbol)
        
        # Player 2 is either human or CPU depending on vs_cpu flag "updated"
        if vs_cpu:
            self.player_2 = cpu_type(name='CPU', symbol=p2_symbol)
        else:
            self.player_2 = p2_type(name='Player 2', symbol=p2_symbol)

        self.turn = 0

    def start(self):
        """Begin playing a new game.

        Players take turns until either someone wins or the board is full."""

        # Clear the board
        self.board.clear()

        # Main game loop
        while not self.board.is_full():
            # Figure out whose turn it is
            match self.turn % 2:
                case 0:
                    current_player = self.player_1
                case 1:
                    current_player = self.player_2
            print(f"{current_player.name}'s turn.")

            # Display the board
            self.board.display()

            # Get the next player's move
            move_is_invalid = True
            while move_is_invalid: # Keep trying until we get a valid move
                col = current_player.move(board=self.board) # # Important: pass the board so CPUPlayer can see it "updated"
                try:
                    self.board.add_piece(col, current_player.symbol)
                    move_is_invalid = False # If we make it to this line, move was valid
                except InvalidMoveError as err:
                    print(err) # Otherwise display why the move was not valid

            # Increment the turn count
            self.turn += 1

            # Check for winners
            if self.board.check_winner():
                print(f'{current_player.name} wins!')
                self.board.display()  # Show final board state "updated"
                break # Get out of the while loop without triggering the else clause
        else:
            # If we reach this line, the board is full
            print('No winner!')
            self.board.display()  # Show final board state "updated"

    def get_player_symbol(self, player_name):
        """Request a valid symbol to use for a player."""
        symbol_is_invalid = True
        while symbol_is_invalid:
            symbol = input(f'Enter a character to use as a symbol for {player_name}: ')
            symbol = symbol.strip() # Remove leading and trailing whitespace
            symbol = symbol[0] # Only keep the first character, ignore everything else
            if not symbol:
                print('Symbol must not be a whitespace character!')
            else:
                # Get positive confirmation from the player
                confirmation = input(f'Use "{symbol}" for {player_name}? (y/N): ')
                symbol_is_invalid = not confirmation.lower().startswith('y')
        return symbol


if __name__ == "__main__":
    # Play a new connect 4 game
    print("Welcome to Connect Four!")
    print("You can choose to play against another human or against the computer.")
    print("Choose your opponent!")
    
    
    while True:
        choice = input("Enter 1 for human vs human, or 2 for human vs computer: ").strip()

        try:
            choice_num = int(choice)          # Try to convert to integer
            if choice_num in (1, 2):
                break                         # Valid input → exit the loop
            else:
                print("Please enter either 1 or 2.")
        except ValueError:
            # Happens when input can't be converted to int (letters, empty, etc.)
            print("Invalid input. Please enter 1 or 2.\n")

    if choice == "2":
        # Human vs CPU
        game = ConnectFourGame(vs_cpu=True)
    else:
        # Default: Human vs Human
        game = ConnectFourGame()
    
while True:
        game.start()
        
        while True:
            answer = input('Play again? (y/n): ').strip().lower()
            if answer in ('y', 'yes', ''):
                break  # continue outer loop → play again
            if answer in ('n', 'no'):
                print("Thanks for playing!")
                exit()   # or just break outer loop and let program end
            print('Please answer y or n.\n')
            