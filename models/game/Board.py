import numpy

class Board(object):
    """ Abstract base class for board objects.  Implements some methods that are common to both microboards and macroboards.
    """

    """ constants for UTTT boards.
    These are defined such that the sum of three cells is 3 iff X holds all three cells
    and the sum is 6 iff O has captured all three cells """
    X = 1
    X_WIN_COND = X * 3
    O = 2
    O_WIN_COND = O * 3
    EMPTY = -2
    CAT = -3  # value representing a board that was completed but tied

    def __init__(self):
        self.board_completed = False
        self.total_moves = 0
        self.winner = Board.EMPTY

    def make_move(self, move):
        """
        Applies the specified move to this Board
        :param move: the Move object to apply
        :return: None
        """
        raise Exception("The abstract Board method make_move must be overridden by child class")

    # should return X, O, or EMPTY based on the contents of the specified cell
    def check_cell(self, row, col):
        """
        Checks the specified cell and returns the contents.
        :param row: integer between 0 and 2 specifying the vertical coordinate of the cell to check
        :param col: integer between 0 and 2 specifying the horizontal coordinate of the cell to check
        :return: Board.X if the cell is captured by X, Board.O if the cell is captured by O, Board.EMPTY otherwise
        """
        raise Exception("The abstract Board method check_cell must be overridden by the child class")

    def check_board_completed(self, row, col):
        """
        Checks whether the most recent move caused the board to be won, lost, or tied, then sets the
        'board_completed' and 'winner' member variables appropriately.
        A board is defined to be tied if all possible moves have been made but neither X nor O won.
        Winner will be set to Board.EMPTY if the board is incomplete or tied

        :param row: the row of the most recent move
        :param col: the column of the most recent move
        :return: True if the board is completed (won or tied), False otherwise
        """
        rowsum = 0
        colsum = 0
        main_diag_sum = 0  # sum of diagonal from top-left to bottom-right
        alt_diag_sum = 0  # sum of diagonal from top-right to bottom-left
        for i in [0, 1, 2]:
            rowsum += self.check_cell(row, i)
            colsum += self.check_cell(i, col)
            main_diag_sum += self.check_cell(i, i)
            alt_diag_sum += self.check_cell(i, 2 - i)

        if rowsum == Board.X_WIN_COND or colsum == Board.X_WIN_COND or main_diag_sum == Board.X_WIN_COND or alt_diag_sum == Board.X_WIN_COND:
            self.board_completed = True
            self.winner = Board.X
        elif rowsum == Board.O_WIN_COND or colsum == Board.O_WIN_COND or main_diag_sum == Board.O_WIN_COND or alt_diag_sum == Board.O_WIN_COND:
            self.board_completed = True
            self.winner = Board.O

        # check for tie
        completed_boards = 0
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if self.check_cell(row, col) in [Board.X, Board.O, Board.CAT]:
                    completed_boards += 1

        if completed_boards == 9:
            self.board_completed = True

    def get_capture_vector(self, player):
        """ Returns a vector of length 9 with a binary representation of which cells have been captured by the given player
        For example, if the specified player has captured the center and corner cells, then this method returns
        [1, 0, 1, 0, 1, 0, 1, 0, 1]
        If the player has captured the center only, this method returns
        [0, 0, 0, 0, 1, 0, 0, 0, 0]

        :param player: Board.X or Board.O
        :return: the capture vector for the specified player
        """
        if player not in [self.X, self.O]:
            raise Exception("Capture vector requested for invalid player")

        capture_vector = numpy.zeros(9)
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if self.check_cell(row, col) == player:
                    index = 3*row + col
                    capture_vector[index] = 1

        return capture_vector

    def count_attacking_sequences(self, player):
        """ Returns the count of attacking sequences owned by the given player on this board

            :param player: Board.X or Board.O
            :return: an integer count of attacking sequences
        """
        if player not in [self.X, self.O]:
            raise Exception("Capture vector requested for invalid player")

        count = 0
        # check each row
        for row in [0, 1, 2]:
            player_controlled = 0
            empty_cells = 0
            for col in [0, 1, 2]:
                controller = self.check_cell(row, col)
                if controller == player: player_controlled += 1
                elif controller == Board.EMPTY: empty_cells += 1

            if player_controlled == 2 and empty_cells == 1:
                count += 1

        # check each col
        for col in [0, 1, 2]:
            player_controlled = 0
            empty_cells = 0
            for row in [0, 1, 2]:
                controller = self.check_cell(row, col)
                if controller == player: player_controlled += 1
                elif controller == Board.EMPTY: empty_cells += 1

            if player_controlled == 2 and empty_cells == 1:
                count += 1

        # check main diagonal
        player_controlled = 0
        empty_cells = 0
        for i in [0, 1, 2]:
            controller = self.check_cell(i,i)
            if controller == player: player_controlled += 1
            elif controller == Board.EMPTY: empty_cells += 1

        if player_controlled == 2 and empty_cells == 1:
            count += 1

        # check alt diagonal
        player_controlled = 0
        empty_cells = 0
        for i in [0, 1, 2]:
            controller = self.check_cell(i, 2 - i)
            if controller == player: player_controlled += 1
            elif controller == Board.EMPTY: empty_cells += 1

        if player_controlled == 2 and empty_cells == 1:
            count += 1

        return count
