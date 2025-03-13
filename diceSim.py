import cmd
from diceGame import DiceGame


class DiceSim(cmd.Cmd):
    """
        Driver class to run the shell prompt of the game.
    """
    intro = 'Welcome to the Dice Game Simulation.\nType help or ? to list commands.\n'
    prompt = '(dice-game) '

    def __init__(self, size=10):
        super(DiceSim, self).__init__()
        self.GAME = DiceGame(size)
        self.DISABLED = set(["move"])

    """ Shell Methods """

    def default(self, line):
        """
            Handles the default behavior of any unrecognized command.
        """
        print("Please enter a valid command.")

    def do_board(self, arg):
        """
            Prints the current state of the Game Board to the console.
        """
        print(f"The Game Board is:\n{self.GAME.getBoard()}")

    def do_exit(self, arg):
        """
            Close the Dice Game Simulation.
        """
        return True

    def do_move(self, arg):
        """
            Perform the move, removing the specified option(s) from the game board.
            A move may be represented by an integer, or 2 integers separated by a space.
        """
        move = self._parseMove(arg)
        if move and self.GAME.isValidMove(move):
            self.GAME.doMove(move)
            self.DISABLED.add("move")
            if self.GAME.hasWon():
                print("Congratulations, You have won the game!")
                print("Type `reset` to play again.")
            else:
                self.DISABLED.remove("roll")
        else:
            print(f"{move} is not a valid move.")
            print(f"Please select a move from:\n{self.GAME.getMoves()}")

    def do_reset(self, arg):
        """
            Resets the board and game state.
        """
        self._resetGame()
        print("The game board and state has been reset.")

    def do_roll(self, arg):
        """
            Roll two six-sided dice to determine the next target value.
        """
        roll = self.GAME.roll()
        target = roll[0] + roll[1]
        self.GAME.setTarget(target)
        moves = self.GAME.getMoves()
        self.DISABLED.add("roll")
        print(f"You have rolled:\n{roll}")
        print(f"The Target value is:\n{target}")
        if not moves or len(moves) == 0:
            print("There are no available moves. You have lost the game!")
            print("Type `reset` to play again.")
        else:
            self.DISABLED.remove("move")
            print(f"This results in the available moves:\n{moves}")
            print("Please select a move from the available moves.")

    def precmd(self, line):
        """
            Hook that runs before the supplied command, this will:
                Convert the command to lowercase.
                Ensure only valid commands are ran based on the state of the game and last command ran.
        """
        line = line.lower()
        command = line.split()[0]
        if command in self.DISABLED:
            print(f"`{command}` is disabled due to the state of the game.")
            return "invalid"
        return line

    """ Functional Methods """

    @staticmethod
    def _parseMove(arg):
        """
            Parses the integer or tuple of integers from the command-lines arguments.
        """
        if arg:
            option1, *option2 = map(int, arg.split())
            if option2:
                return (option1, option2[0])
            else:
                return option1

        return None

    def _resetGame(self):
        """
            Resets the simulator and game to the initial state.
        """
        self.DISABLED = set(["move"])
        self.GAME.reset()
