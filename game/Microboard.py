import numpy
from .BoardConstants import BoardConstants as BC
from .Exceptions import InvalidMoveException

class Microboard:
    'Represents a small (3x3) tic-tac-toe board'

    def __init__(self):
        self.board = numpy.ones((3, 3)) * BC.EMPTY
        self.total_moves = 0  # the number of moves made on this board
        self.board_completed = False
        self.winner = BC.EMPTY  # An "EMPTY" winner indicates that neither X nor O won the board

    def make_move(self, player, row, col):
        if self.board_completed:
            raise InvalidMoveException("You cannot make additional moves on a completed board")

        if player not in [BC.X, BC.O]:
            raise InvalidMoveException("A move can only be made by player X or O.  Tried to make move as player %s" % player)

        if row < 0 or row > 2 or col < 0 or col > 2:
            raise InvalidMoveException("Move location is out of bounds.  Please specify a row and column between 0 and 2")

        if self.board[row][col] != BC.EMPTY:
            raise InvalidMoveException("You cannot make a move in an occupied slot")

        self.board[row][col] = player
        self.total_moves += 1
        self.check_board_completed(row, col)

    def check_board_completed(self, row, col):
        'Checks if the current board has been won or filled up (tied)'
        rowsum = 0
        colsum = 0
        for i in [0, 1, 2]:
            rowsum += self.board[row][i]
            colsum += self.board[i][col]

        if rowsum == 3 or colsum == 3:
            self.board_completed = True
            self.winner = BC.X
        elif rowsum == 6 or colsum == 6:
            self.board_completed = True
            self.winner = BC.O
        elif self.total_moves == 9:
            self.board_completed = True

    def __str__(self):
        representation = ""
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if self.board[row][col] == BC.O:
                    representation += "O"
                elif self.board[row][col] == BC.X:
                    representation += "x"
                else:
                    representation += "_"
            if row != 2:
                representation += "\n"
        return representation

