import argparse
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from sudokuGameLogic import SudokuGame
from sudokuUI import SudokuUI, WIDTH, HEIGHT, MARGIN, SIDE, LEVEL, generate
from os import listdir
from os.path import isfile, join

# Global Variables
mypath = "boards/"
BOARDS = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            choices=BOARDS,
                            required=True)

    args = vars(arg_parser.parse_args())
    return args['board']


def start_game(board_name):
    """
    """
    # board_name = parse_arguments()
    with open('boards/' + '%s' % board_name, 'r') as boards_file:

        root = Tk()
        game = SudokuGame(boards_file)
        game.start()

        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()

if __name__ == '__main__':
    generate(LEVEL)
    start_game('temp.sudoku')
