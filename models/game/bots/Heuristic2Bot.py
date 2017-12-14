import numpy
from models.game.bots.MinimaxBot import MinimaxBot
from models.game.Board import Board


class Heuristic2Bot(MinimaxBot):
    """ Minimax bot that plays using the H2 Heuristic
    """

    def __init__(self, number, time_limit=10, name=None):
        """ Minimax bot that plays with the H2 heuristic

        :param number:  Board.X for player1 or Board.O for player2
        :param time_limit:  The maximum time that the bot has to make a move
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "Heuristic2 Minimax"
        MinimaxBot.__init__(self, number, time_limit, name=name)
        self.player_type = 'h2 minimax'

    def compute_score(self, board):
        """
        This heuristic scores the board by awarding:
        9 points for capturing the center small board
        7 points for capturing the corner small boards
        5 points for capturing the edge small boards
        3 points for capturing the center of a small board
        2 points for capturing the corner of a small board
        1 point for capturing the edge of a small board
        It deducts points if the opponent has captured any of these positions.

        :param board: the board state to score
        :return: the score computed by this heuristic
        """
        # weights used to score board
        G_CENTER = 10
        G_CORNER = 8
        G_EDGE = 6
        L_CENTER = 3
        L_CORNER = 2
        L_EDGE = 1
        global_capture_weight = numpy.array([G_CORNER, G_EDGE, G_CORNER, G_EDGE, G_CENTER, G_EDGE, G_CORNER, G_EDGE, G_CORNER])
        global_adjustment_weights = numpy.array([1.2, 1.0, 1.2, 1.0, 1.4, 1.0, 1.2, 1.0, 1.2])
        local_capture_weight = numpy.array([L_CORNER, L_EDGE, L_CORNER, L_EDGE, L_CENTER, L_EDGE, L_CORNER, L_EDGE, L_CORNER])

        our_capture_vector = board.get_capture_vector(Board.X)
        opponent_capture_vector = board.get_capture_vector(Board.O)

        score = 0
        # modify score for global board
        score += numpy.dot(our_capture_vector, global_capture_weight) - numpy.dot(opponent_capture_vector, global_capture_weight)
        # modify score for each local board:
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                local_board = board.board[row][col]
                if not local_board.board_completed:
                    our_capture_vector = local_board.get_capture_vector(Board.X)
                    opponent_capture_vector = local_board.get_capture_vector(Board.O)
                    index = row*3 + col
                    adjusted_weight = local_capture_weight * global_adjustment_weights[index]
                    score += numpy.dot(our_capture_vector, adjusted_weight) - numpy.dot(opponent_capture_vector, adjusted_weight)

        return score
