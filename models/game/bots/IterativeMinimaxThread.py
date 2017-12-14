from threading import Thread
from models.game import Board
from services import ApplicationStatusService


class IterativeMinimaxThread(Thread):
    def __init__(self, board, valid_moves, player, scoring_function):
        Thread.__init__(self)
        self.done = False # controls when the thread stops
        self.best_move = valid_moves[0]  # this will be updated as the thread runs

        self.board = board
        self.valid_moves = valid_moves
        self.player = player
        self.score_board = scoring_function

    def run(self):
        depth = 0
        board_copy = self.board.clone()
        while not self.done:
            depth += 1
            alpha = -float('inf')
            beta = float('inf')
            score, best_move = self._max(board_copy, self.valid_moves, alpha, beta, depth)
            self.best_move = best_move

    def stop(self):
        self.done = True

    def _max(self, board, valid_moves, alpha, beta, max_depth):
        """
        Private function which computes the move that a rational maximizing player would choose
        :param board: GlobalBoard object representing the current state
        :param valid_moves: list of valid moves that can be made on the board object
        :param alpha: the current value of alpha (the best score that MAX can guarantee so far)
        :param beta: the current value of beta (the best score that MIN can guarantee so far)
        :return: the value (score) of the best move and the move object itself
        """
        if board.board_completed:  # termination test
            if board.winner == Board.EMPTY or board.winner == Board.CAT:
                return 0, None
            elif board.winner == self.player:
                return 10000000, None
            else:
                return -10000000, None
        elif max_depth == 0:
            # scores are computed from the perspective of the 'X' player, so they need to be flipped if our bot is 'O'
            if self.player == Board.X:
                return self.score_board(board), None
            else:
                return -self.score_board(board), None

        a, b = alpha, beta

        value = -float('inf')
        best_move = None
        for move in valid_moves:
            child_board = board.clone()
            child_board.make_move(move)
            move_value, minimizing_move = self._min(child_board, child_board.get_valid_moves(move), a, b, max_depth-1)
            if move_value > value:
                value = move_value
                best_move = move

            if value >= b:
                return value, best_move

            a = max(a, move_value)

        return value, best_move

    def _min(self, board, valid_moves, alpha, beta, max_depth):
        # test for stopping condition
        if board.board_completed:
            if board.winner == Board.EMPTY or board.winner == Board.CAT:
                return 0, None
            elif board.winner == self.player:
                return 10000000, None
            else:
                return -10000000, None
        elif max_depth == 0:
            # scores are computed from the perspective of the 'X' player, so they need to be flipped if our bot is 'O'
            if self.player == Board.X:
                return self.score_board(board), None
            else:
                return -self.score_board(board), None

        a, b = alpha, beta

        value = float('inf')
        best_move = None
        for move in valid_moves:
            child_board = board.clone()
            child_board.make_move(move)
            move_value, maximizing_move = self._max(child_board, child_board.get_valid_moves(move), a, b, max_depth - 1)
            if move_value < value:
                value = move_value
                best_move = move

            if value <= a:
                return value, best_move

            b = min(b, move_value)

        return value, best_move
