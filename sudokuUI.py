from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT, Label
import copy
from gameAI import Game_Solver
from sudokuGenerator import generate

MARGIN = 80
SIDE = 120
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
LEVEL = "Easy"

class SudokuUI(Frame):
    """
    """
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)

        self.row = 0
        self.col = 0
        self.level = None

        self.__initUI()

    def __initUI(self):
        """
        """
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, bg = "white" , width = WIDTH, height = HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(self,
                              text="Clear answers",
                              height = HEIGHT // 15,
                              font = ("Monaco", HEIGHT // 62),
                              command=self.__clear_answers)

        solver_button = Button(self, 
                            text = "Solve Puzzle",
                            height = HEIGHT // 15,
                            font = ("Monaco", HEIGHT // 62),
                            command=self.__solve_puzzle
                            )

        New_Label = Label(self, text = "New Puzzle : ", font = ("Monaco, 20"))

        easy_button = Button(self, text = "Easy", font = ("Monaco", 20), command = self.__easy_clicked)
        medium_button = Button(self, text = "Medium", font = ("Monaco", 20), command = self.__medium_clicked)
        hard_button = Button(self, text = "Hard", font = ("Monaco", 20), command = self.__hard_clicked)
        insane_button = Button(self, text = "Insane", font = ("Monaco", 20), command = self.__insane_clicked)

                            
        clear_button.pack(side = LEFT)
        solver_button.pack(side = LEFT)
        
        insane_button.pack(side = RIGHT)
        hard_button.pack(side = RIGHT)
        medium_button.pack(side = RIGHT)
        easy_button.pack(side = RIGHT)
        New_Label.pack(side = RIGHT)


        self.__draw_grid()
        self.__draw_puzzle()

        # self.cell_click and self.key_pressed is a callback function , much like JS
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def fresh_start(self):
        """
        """
        self.__clear_answers()
        fresh_board = generate(self.level)
        self.game.start_puzzle = copy.deepcopy(fresh_board)
        self.game.puzzle = fresh_board
        self.__draw_puzzle()

    def __easy_clicked(self):
        """
        """
        self.level = "Easy"
        self.fresh_start()

    def __medium_clicked(self):
        """
        """
        self.level = "Medium"
        self.fresh_start()

    
    def __hard_clicked(self):
        """
        """
        self.level = "Hard"
        self.fresh_start()

    
    def __insane_clicked(self):
        """
        """
        self.level = "Insane"
        self.fresh_start()



    def __draw_grid(self):
        """
        """

        for i in range(10):
            if i % 3 == 0:
                color = "blue"
            else:
                color = "grey"
            

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = WIDTH - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            y0 = MARGIN + i * SIDE
            x0 = MARGIN
            y1 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        """
        """

        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2

                    original = self.game.start_puzzle[i][j]
                    
                    if answer == original:
                        color = "red"
                    else:
                        color = "dark green"

                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill = color, font = ("Monaco", 25))
    
    def __clear_answers(self):
        """
        """

        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("winner")
        self.__draw_puzzle()

    def __cell_clicked(self, event):
        """
        """
        if self.game.game_over:
            return

        # Event class gives us current x and current ys
        x = event.x
        y = event.y

        if(MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

        # Get row and column from x , y coordinates
        row = (y - MARGIN) // SIDE
        col = (x - MARGIN) // SIDE

        # if cell was selected already - deselect it
        if (row, col) == (self.row, self.col):
            self.row, self.col = -1, -1
        elif self.game.puzzle[row][col] == 0:
            self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        """
        """
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __key_pressed(self, event):
        """
        """
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col = -1
            self.row = -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __draw_victory(self):
        """
        """
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32)
        )

    def __solve_puzzle(self):
        """
        """
        self.__clear_answers()
        solver = Game_Solver(self.game.puzzle)
        solver.print_board(self.game.puzzle)
        solver.solve(self.game.puzzle)
        print("___________________")
        solver.print_board(self.game.puzzle)
        self.__draw_puzzle()

    def return_level(self):

        return self.level