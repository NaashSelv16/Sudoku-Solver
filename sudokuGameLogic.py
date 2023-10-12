from sudokuBoard import SudokuBoard

class SudokuGame(object):
    """
    """
    def __init__(self, board_file):
        
        self.board_file = board_file
        Board = SudokuBoard(board_file)
        self.start_puzzle = Board.board

    def start(self):
        """
        """
        # Final Solved Flag
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        """
        """
        for row in range(9):
            if not self.__check_row(row):
                return False
        
        for column in range(9):
            if not self.__check_column(column):
                return False
        
        for row in range(3):
            for col in range(3):
                if not self.__check_square(row, col):
                    return False

        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )