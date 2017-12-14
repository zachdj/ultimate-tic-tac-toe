import random
from models.game.bots.Bot import Bot
from models.game.Board import Board


class RandoMaxBot(Bot):
    """ Semi-random bot

    This is a minimax bot that scores moves randomly unless the end of the game is seen within a 2-ply lookahead
    """
    def __init__(self, number, name=None):
        if name is None:
            name = "Rando-Max Bot"
        Bot.__init__(self, number, name=name)
        self.player_type = 'randomax'
        random.seed()

    def compute_next_move(self, board, valid_moves):
        score, selected_move = self._max(board, valid_moves,-float('inf'), float('inf'), 2)
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
        if board.board_completed:  # termination test
            if board.winner == Board.EMPTY or board.winner == Board.CAT:
                return 0, None
            elif board.winner == self.number:
                return 10000000, None
            else:
                return -10000000, None
        elif max_depth == 0:
            # scores are computed from the perspective of the 'X' player, so they need to be flipped if our bot is 'O'
            if self.number == Board.X:
                return self.compute_score(board), None
            else:
                return -self.compute_score(board), None

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
            elif board.winner == self.number:
                return 10000000, None
            else:
                return -10000000, None
        elif max_depth == 0:
            # scores are computed from the perspective of the 'X' player, so they need to be flipped if our bot is 'O'
            if self.number == Board.X:
                return self.compute_score(board), None
            else:
                return -self.compute_score(board), None

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
        return random.uniform(-1, 1)

    def setup_bot(self, game):
        pass
