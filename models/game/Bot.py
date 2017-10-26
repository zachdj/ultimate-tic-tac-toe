class Bot(object):
    """ Abstract base class for UTTT Bots (non-human players)
    """

    def compute_next_move(self, board):
        print("Uh oh! You need to override the compute_next_move method in the base class")