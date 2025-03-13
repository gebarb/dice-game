import getopt
import sys

from diceSim import DiceSim


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
