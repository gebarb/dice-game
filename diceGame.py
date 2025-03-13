import random


class DiceGame:
    """
        Class to represent the game board and functionality.
    """

    def __init__(self, size: int):
        self.SIZE = size
        self.initializeGame()

    def getBoard(self) -> dict:
        """
            Returns a dictionary representing each option on the Board and its current state.
        """
        return self.BOARD

    def getMoves(self) -> list[int | tuple[int, int]]:
        """
            Returns a list of valid options to remove from the board.
            A remaining option can be removed on this turn if it has the same value as the sum of the roll,
            or if it can be added to another remaining option to equal the sum of the roll.
        """
        moves = []
        if self.TARGET:
            if self.BOARD.get(self.TARGET, False) is True:
                moves.append(self.TARGET)

            for option, i in self.BOARD.items():
                if i is False:
                    continue
                for complement, j in self.BOARD.items():
                    if option == complement or j is False:
                        continue
                    if option + complement == self.TARGET:
                        moves.append((option, complement))

        self.setMoves(moves)

        return self.MOVES

    def getTarget(self) -> int:
        """
            Returns the current Target value. If an active roll is not in play, then this will be None.
        """
        return self.TARGET

    def hasWon(self) -> bool:
        """
            Returns a boolean showing if the player has won the game.
            To win the game, all options in the board must be removed.
        """
        return all(b is False for b in self.BOARD.values())

    def initializeGame(self):
        """
            Initializes the Board and state of the game.
        """
        self.BOARD = {i: True for i in range(1, self.SIZE)}
        self.MOVES = None
        self.TARGET = None

    def isValidMove(self, move: int | tuple[int, int]) -> bool:
        """
            Returns a boolean showing if the requested Move is valid for the current state of the Board.
        """
        return move in self.MOVES

    def reset(self):
        """
            Resets the Board and state of the game.
        """
        self.initializeGame()

    @staticmethod
    def roll() -> tuple[int, int]:
        """
            Returns a tuple representing the results of rolling two six-sided dice
        """
        return (random.randint(1, 6), random.randint(1, 6))

    def setMoves(self, moves: list[int | tuple[int, int]]):
        """
            Set the current list of Potential Moves to the specified moves.
        """
        self.MOVES = moves

    def setTarget(self, target: int):
        """
            Set the current Target value to the specified integer.
        """
        self.TARGET = target

    def doMove(self, option: int):
        """
            Perform the requested move by removing the specified options from the Board.
        """
        if isinstance(option, tuple):
            self.BOARD[option[0]] = False
            self.BOARD[option[1]] = False
        else:
            self.BOARD[option] = False
        self.TARGET = None
        self.MOVES = None
