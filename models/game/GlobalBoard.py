from .Board import Board
from .LocalBoard import LocalBoard
from .Move import Move


class GlobalBoard(Board):
    """  Represents the meta-board composed of a 3x3 grid of smaller tic-tac-toe boards
    """
    def __init__(self):
        Board.__init__(self)
        self.board = [[LocalBoard(), LocalBoard(), LocalBoard()],
                      [LocalBoard(), LocalBoard(), LocalBoard()],
                      [LocalBoard(), LocalBoard(), LocalBoard()]]

    def make_move(self, move):
        """  Overrides Board.make_move
        """
        local_board = self.board[move.metarow][move.metacol]
        if local_board.board_completed:
            raise Exception("Invalid move.  That meta-board is already completed")

        local_board.make_move(move)
        self.total_moves += 1

        self.check_board_completed(move.metarow, move.metacol)

    def check_cell(self, row, col):
        """  Overrides Board.check_cell
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            raise Exception("Requested meta-cell is out of bounds")
        local_board = self.board[row][col]
        if local_board.cats_game:
            return Board.CAT
        else:
            return local_board.winner

    def get_valid_moves(self, last_move):
        """
        Returns an array of valid moves following the specified last move
        :param last_move: the last move to be played on this board
        :return: array of Move objects that are valid to follow the last move
        """
        valid_moves = []
        player = Board.X
        if last_move.player == Board.X:
            player = Board.O

        new_global_row = last_move.row
        new_global_col = last_move.col

        next_local_board = self.board[new_global_row][new_global_col]  # the last move sent the opponent to this board

        if next_local_board.board_completed:
            #  if the board has been won, the player gets a "wild card" - can move to any open space on a non-completed board
            for i in list(range(0, 9)):
                metarow = i // 3
                row = i % 3
                for j in list(range(0, 9)):
                    metacol = j // 3
                    col = j % 3
                    if not self.board[metarow][metacol].board_completed and self.board[metarow][metacol].check_cell(row, col) == Board.EMPTY:
                        valid_moves.append(Move(player, metarow, metacol, row, col))

        else:
            # otherwise the player can move to any open space on THIS board
            for i in [0, 1, 2]:
                for j in [0, 1, 2]:
                    if next_local_board.check_cell(i, j) == Board.EMPTY:
                        valid_moves.append(Move(player, new_global_row, new_global_col, i, j))

        return valid_moves

    def get_possible_moves(self, player=Board.X):
        """
        :return:  a list of all possible moves on a completely empty board
        """
        moves = []
        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                moves.append(Move(player, metarow, metacol, row, col))

        return moves

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

    def to_high_level_string(self):
        representation = ""
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                symbol = 'X'
                if self.board[i][j].winner == Board.O:
                    symbol = 'O'
                elif self.board[i][j].cats_game:
                    symbol = 'C'
                elif self.board[i][j].winner == Board.EMPTY:
                    symbol = '_'
                representation += symbol
            representation += "\n"

        return representation
