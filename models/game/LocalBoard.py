import numpy
from .Board import Board


class LocalBoard(Board):
    """  Represents a traditional 3x3 tic tac toe board
    """
    def __init__(self):
        Board.__init__(self)
        self.board = numpy.ones((3, 3)) * Board.EMPTY

    def check_cell(self, row, col):
        """  Overrides Board.check_cell
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise Exception("Requested cell is out of bounds")
        return self.board[row][col]

    def make_move(self, move):
        """  Overrides Board.make_move
        """
        if self.board[move.row][move.col] != Board.EMPTY:
            raise Exception("You cannot make a move in an occupied slot")

        self.board[move.row][move.col] = move.player
        self.total_moves += 1
        self.check_board_completed(move.row, move.col)

    def __str__(self):
        representation = ""
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if self.board[row][col] == Board.O:
                    representation += "O"
                elif self.board[row][col] == Board.X:
                    representation += "x"
                else:
                    representation += "_"
            if row != 2:
                representation += "\n"
        return representation

