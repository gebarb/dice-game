import cmd
import getopt
import random
import sys


class DiceGame:
    """
        Class to represent the game board and functionality.
    """

    def __init__(self, size: int):
        self.SIZE = size
        self.initializeGame()

    def getMoves(self) -> list[int | tuple[int, int]]:
        """
            Returns a list of valid options to remove from the board.
            A remaining option can be removed on this turn if it has the same value as the sum of the roll,
            or if it can be added to another remaining option to equal the sum of the roll.
        """
        moves = []
        if self.BOARD.get(self.TARGET, False) is True:
            moves.append(self.TARGET)

        self.setMoves(moves)

        return self.MOVES

    def getTarget(self):
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
        self.MOVES = None


class DiceSim(cmd.Cmd):
    """
        Driver class to run the shell prompt of the game.
    """
    # TODO: use `precommand` to enable/disable commands based on the state of the game

    intro = 'Welcome to the Dice Game Simulation.\nType help or ? to list commands.\n'
    prompt = '(dice-game) '

    def __init__(self, size=10):
        super(DiceSim, self).__init__()
        self.GAME = DiceGame(size)

    """ Shell Methods """

    def do_roll(self, arg):
        """
            Roll two six-sided dice to determine the next target value.
        """
        roll = self.GAME.roll()
        target = roll[0] + roll[1]
        self.GAME.setTarget(target)
        moves = self.GAME.getMoves()
        print(f"You have rolled:\n{roll}")
        print(f"The Target value is:\n{target}")
        if not moves or len(moves) == 0:
            print("There are no available moves. You have lost the game!")
            self.GAME.reset()
        print(f"This results in the available moves:\n{moves}")
        print("Please select a move from the available moves.")

    def do_move(self, arg):
        """
            Perform the move, removing the specified option(s) from the game board.
            A move may be represented by an integer, or 2 integers separated by a space.
        """
        move = self._parseMove(arg)
        if move and self.GAME.isValidMove(move):
            self.GAME.doMove(move)
        else:
            print(f"{move} is not a valid move.")
            print(f"Please select a move from:\n{self.GAME.getMoves()}")

    def do_exit(self, arg):
        """
            Close the Dice Game Simulation.
        """
        return True

    """ Functional Methods """

    @staticmethod
    def _parseMove(arg):
        """
            Parses the integer or tuple of integers from the command-lines arguments.
        """
        if arg:
            option1, *option2 = map(int, arg.split())
            if option2:
                return (option1, option2)
            else:
                return option1

        return None


def main(argv):
    size = 10
    try:
        opts, args = getopt.getopt(argv, "s:", ["size="])
        for opt, arg in opts:
            if opt in ('-s', '--size'):
                size = arg

    except getopt.GetoptError as e:
        sys.exit(2)

    DiceSim(size=size).cmdloop()


if __name__ == '__main__':
    main(sys.argv[1:])
