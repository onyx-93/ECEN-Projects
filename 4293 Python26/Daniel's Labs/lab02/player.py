from abc import ABC, abstractmethod
import random

_EMPTY = ' ' # Used to indicate empty spaces in the board

class AbstractPlayer(ABC):
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def move(self, **kwargs):
        """Return an integer representing the column where the player intends to play a piece."""


class ConsolePlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Get which column to play in from the user via text console"""
        return int(input('Enter which column to play in: '))


# TODO: Create a CPUPlayer class which selects moves without user intervention
class CPUPlayer(AbstractPlayer):
    def move(self, **kwargs):
        """Select a column to play in automatically."""
        board = kwargs.get('board')
        valid_columns = [col for col in range(board.num_cols) if board.rows[0][col] is _EMPTY]
        return random.choice(valid_columns)
    