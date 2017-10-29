from . import Board


class Player(object):
    """ Represents a human player
    """

    def __init__(self, number, name=None):
        self.player_type = 'human'
        if number != Board.X and number != Board.O:
            raise Exception("Tried to initialize player with invalid player symbol.")
        self.number = number
        if name:
            self.name = name
        else:
            self.name = "Player %s" % number
