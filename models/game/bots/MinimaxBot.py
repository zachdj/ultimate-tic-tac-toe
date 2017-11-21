import random, timeit
from services import ApplicationStatusService
from .Bot import Bot
from models.game.Board import Board

# TODO: consider experimenting with some more aggressive pruning.  Perhaps in a child bot?


class MinimaxBot(Bot):
    """ Base class for bots that perform a minimax search with a-B pruning

    This bot works by performing an iterative-deepening minimax search of the game tree until time runs out.
    Standard alpha-beta pruning is used to reduce the size of the search space

    Variants of this bot can be implemented by creating a child class which overrides the compute_score() method
    """
    def __init__(self, number, time_limit=5, name=None):
        """

        :param number:  Board.X for player1 or Board.O for player2
        :param name: the name of the
        """
        if name is None:
            name = "Minimax Bot"
        Bot.__init__(self, number, time_limit, name=name)
        self.player_type = 'minimax bot'

    def is_bot(self):
        return True

    def compute_next_move(self, board, valid_moves):
        """
        Computes the next move for this agent
        :param board: the GlobalBoard object representing the current state of the game
        :param valid_moves: valid moves for the agent
        :return: the Move object recommended for this agent
        """
        depth = 0
        begin = timeit.default_timer()
        last_iteration_end_time = timeit.default_timer()
        selected_move = None
        # iteratively increase depth until time runs out
        elapsed_time, estimated_time = 0, 0
        while elapsed_time + 2*estimated_time < self.time_limit and not ApplicationStatusService.terminated:
            depth += 1
            alpha = -float('inf')
            beta = float('inf')
            score, selected_move = self._max(board, valid_moves, alpha, beta, depth)

            # update runtime and estimated time for next iteration
            now = timeit.default_timer()
            elapsed_time = now - begin
            estimated_time = now - last_iteration_end_time
            last_iteration_end_time = now

        return selected_move

    def _max(self, board, valid_moves, alpha, beta, max_depth):
        """
        Private function which computes the move that a rational maximizing player would choose
        :param board: GlobalBoard object representing the current state
        :param valid_moves: list of valid moves that can be made on the board object
        :param alpha: the current value of alpha (the best score that MAX can guarantee so far)
        :param beta: the current value of beta (the best score that MIN can guarantee so far)
        :return: the value (score) of the best move and the move object itself
        """
        if board.board_completed or max_depth == 0:  # termination test
            if board.winner == Board.EMPTY:
                return 0, None
            elif board.winner == self.number:
                return 1, None
            else:
                return -1, None

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
        if board.board_completed or max_depth == 0:  # termination test
            if board.winner == Board.EMPTY:
                return 0, None
            elif board.winner == self.number:
                return 1, None
            else:
                return -1, None

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

    def compute_score(self, board):
        """
        Returns a heuristic score for the board that (ideally) measures how "good" the board is from the perspective of
        the 'X' player.  For the Minimax search to perform correctly, better boards MUST receive higher scores.
        In the framework of this application, scores should fall in the range [-1, 1], where -1 represents O winning,
        1 represents a win for X, and 0 represents a tie.

        :param board: the GlobalBoard object to score
        :return: a float in the range [-1, 1] that represents the "goodness" of the given board state from the perspective of 'X'.
        """
        # child classes should override this method.  The base class scores boards randomly
        score = random.uniform(-1, 1)

        return score

    def setup_bot(self, game):
        pass