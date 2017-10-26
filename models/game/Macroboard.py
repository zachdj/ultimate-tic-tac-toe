from .Board import Board
from .Microboard import Microboard


class Macroboard(Board):
    """  Represents the meta-board composed of a 3x3 grid of smaller tic-tac-toe boards
    """
    def __init__(self):
        Board.__init__(self)
        self.board = [[Microboard(), Microboard(), Microboard()],
                      [Microboard(), Microboard(), Microboard()],
                      [Microboard(), Microboard(), Microboard()]]

    def make_move(self, move):
        """  Overrides Board.make_move
        """
        microboard = self.board[move.metarow][move.metacol]
        if microboard.board_completed:
            raise Exception("Invalid move.  That meta-board is already completed")
        microboard.make_move(move)
        self.total_moves += 1

        self.check_board_completed(move.metarow, move.metacol)

    def check_cell(self, row, col):
        """  Overrides Board.check_cell
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise Exception("Requested meta-cell is out of bounds")
        microboard = self.board[row][col]
        return microboard.winner

    def __str__(self):
        representation = ""
        for i in list(range(0, 9)):
            metarow = i//3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j//3
                col = j % 3
                cell = self.board[metarow][metacol].check_cell(row, col)
                if cell == Board.X: representation += "x"
                elif cell == Board.O: representation += "o"
                else: representation += "_"

                if j in [2, 5]: representation += "    "  # extra space in between metacolumns

            representation += "\n" if i != 8 else ""
            if i in [2, 5]: representation += "\n"  # extra line between metarows

        return representation

