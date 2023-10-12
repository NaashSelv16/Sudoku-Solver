class SudokuError(Exception):
    """
    """
    def __init__(self, error):
        self.error = error
        raise self.error
    
# The Class for only the Sudoku Board
class SudokuBoard(object):
    """
    """
    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    # Create Private Method
    def __create_board(self, board_file):
        # A 2D Matrix or a list of list or defaultdict(list)
        # would be created
        board = []

        # Step 1 : Iterate over each row
        for row in board_file:
            row = row.strip()

            # Step 2 : Go through each column
            if len(row) != 9:
                board = []
                raise SudokuError("Must have exactly 9 rows.")
            
            # Add a list to each rows.
            board.append([])

            # Iterate over each character
            for c in row:
                # Raise error if character is not an integer
                if not c.isdigit():
                    raise SudokuError("Only digits from 0-9 are allowed to be characters.")
                board[-1].append(int(c))
        # Check for 9 lines (Assert over it), raise error if not true
        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")

        # Return the fully constructed board
        return board

    def return_board(self):
        return self.board

    
