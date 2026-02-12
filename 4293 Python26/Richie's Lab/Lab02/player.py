from abc import ABC, abstractmethod
import random

class AbstractPlayer(ABC):
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def move(self, **kwargs):
        """Return an integer representing the column where the player intends to play a piece."""


class ConsolePlayer(AbstractPlayer): # For the input to check if the move is valid I went ahead and used generative AI to make the error catch more robust
    def move(self, **kwargs):        # the initial solutions did not convince me so I chosed for a input taking function that checks the input before is used
        """Get which column to play in from the user via text console""" # The following function chechs if the move is in a valid column and if it is an integer, if these two are satisfied the function will continue otherwise it will crash
        board = kwargs.get("board", None)
        max_col = (board.num_cols - 1) if board is not None else 6

        while True:
            raw = input(f"Enter which column to position your key (0-{max_col}): ").strip()

            try:
                col = int(raw)
            except ValueError:
                print("\tInvalid input: enter an integer. \n") 
                continue

            if not (0 <= col <= max_col):
                print(f"Invalid column: enter a number from 0 to {max_col}.")
                continue

            return col



class CPUPlayer(AbstractPlayer):
    def move(self, **kwargs):
        board = kwargs.get("board")
        max_col = (board.num_cols - 1) if board else 6
        col = random.randint(0, max_col)
        print(f"{self.name} chooses colum {col}")
        return col

# Link to chat conversation: https://www.perplexity.ai/search/i-want-to-implement-the-add-pi-WCcmPdoOTIa.XcKeOJirqQ#0