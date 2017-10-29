from ..Player import Player


class Bot(Player):
    """ Abstract base class for UTTT Bots (non-human players)
    """

    def __init__(self, number, name=None):
        Player.__init__(number, name)
        self.player_type = 'generic bot'

    def compute_next_move(self, board, valid_moves):
        """
        Computes the next move for this agent
        :param board: the GlobalBoard object representing the current state of the game
        :param valid_moves: valid moves for the agent
        :return: the Move object recommended for this agent
        """
        raise Exception("You need to override the compute_next_move method in the child class")