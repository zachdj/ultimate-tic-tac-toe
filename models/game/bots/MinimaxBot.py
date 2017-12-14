import random
from .TimeLimitedBot import TimeLimitedBot
from models.game.bots.IterativeMinimaxThread import IterativeMinimaxThread


class MinimaxBot(TimeLimitedBot):
    """ Base class for bots that perform a minimax search with a-B pruning

    This bot works by performing an iterative-deepening minimax search of the game tree until time runs out.
    Standard alpha-beta pruning is used to reduce the size of the search space

    Variants of this bot can be implemented by creating a child class which overrides the compute_score() method
    """
    def __init__(self, number, time_limit=10, name=None):
        """

        :param number:  Board.X for player1 or Board.O for player2
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "Minimax Bot"
        TimeLimitedBot.__init__(self, number, time_limit, name=name)
        self.player_type = 'minimax bot'

    def compute_next_move(self, board, valid_moves):
        """
        Computes the next move for this agent
        :param board: the GlobalBoard object representing the current state of the game
        :param valid_moves: valid moves for the agent
        :return: the Move object recommended for this agent
        """

        search_thread = IterativeMinimaxThread(board, valid_moves, self.number, lambda b: self.compute_score(b))
        search_thread.setDaemon(True)
        search_thread.start()
        search_thread.join(timeout=self.time_limit)  # the join times out after the time limit has expired
        search_thread.stop()  # this will actually cause the thread to terminate

        return search_thread.best_move

    def compute_score(self, board):
        """
        Returns a heuristic score for the board that (ideally) measures how "good" the board is from the perspective of
        the 'X' player.  For the Minimax search to perform correctly, better boards for X should receive higher scores

        :param board: the GlobalBoard object to score
        :return: a float that represents the "goodness" of the given board state from the perspective of 'X'.
        """
        # child classes should override this method.  The base class scores boards randomly
        score = random.uniform(-1, 1)
        return score

    def setup_bot(self, game):
        pass
