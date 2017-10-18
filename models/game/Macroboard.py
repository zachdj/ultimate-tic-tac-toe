import numpy
from .BoardConstants import BoardConstants as BC
from .Microboard import Microboard
from exceptions import InvalidMacroboardMoveException


class Macroboard:
    'Represents the "big" tic tac toe board composed of nine Microboards'
    def __init__(self):
        self.board = [[Microboard(), Microboard(), Microboard()],
                      [Microboard(), Microboard(), Microboard()],
                      [Microboard(), Microboard(), Microboard()]]
        self.total_moves = 0
        self.board_completed = False
        self.winner = BC.EMPTY

    def make_move(self, player, metarow, metacol, row, col):
        'Makes a move on this board using the current player.  Player should be BoardConstants.X or BoardConstants.O'

        if row < 0 or row > 2 or col < 0 or col > 2:
            raise InvalidMacroboardMoveException("Move location is out of bounds.  Please specify a metarow and metacolumn between 0 and 2")

        microboard = self.board[metarow][metacol]
        microboard.make_move(player, row, col)
        self.total_moves += 1

        self.check_board_completed(metarow, metacol)

    def check_board_completed(self, metarow, metacol):
        'Checks if the current board has been won or tied'
        rowsum = 0
        colsum = 0
        main_diag_sum = 0  # sum of diagonal from top-left to bottom-right
        alt_diag_sum = 0  # sum of diagonal from top-right to bottom-left
        for i in [0, 1, 2]:
            # "winner" will be BC.EMPTY if the microboard has not been won or if the board was a tie
            rowsum += self.board[metarow][i].winner
            colsum += self.board[i][metacol].winner
            main_diag_sum += self.board[i][i].winner
            alt_diag_sum += self.board[i][2 - i].winner

        if rowsum == BC.X_WIN_COND or colsum == BC.X_WIN_COND or main_diag_sum == BC.X_WIN_COND or alt_diag_sum == BC.X_WIN_COND:
            self.board_completed = True
            self.winner = BC.X
        elif rowsum == BC.O_WIN_COND or colsum == BC.O_WIN_COND or main_diag_sum == BC.O_WIN_COND or alt_diag_sum == BC.O_WIN_COND:
            self.board_completed = True
            self.winner = BC.O

        # check for tie
        completed_boards = 0
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if self.board[row][col].board_completed: completed_boards += 1

        if completed_boards == 9:
            self.board_completed = True

    def __str__(self):
        representation = ""
        for i in numpy.arange(0, 9):
            metarow = i//3
            row = i % 3
            for j in numpy.arange(0, 9):
                metacol = j//3
                col = j % 3
                cell = self.board[metarow][metacol].cell(row, col)
                if cell == BC.X: representation += "x"
                elif cell == BC.O: representation += "o"
                else: representation += "_"

                if j in [2, 5]: representation += "    "  # extra space in between metacolumns

            representation += "\n" if i != 8 else ""
            if i in [2, 5]: representation += "\n"  # extra line between metarows

        return representation

