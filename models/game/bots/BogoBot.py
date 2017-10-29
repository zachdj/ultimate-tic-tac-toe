import random
from .Bot import Bot


class BogoBot(Bot):
    """
    This bot moves at random
    """
    def __init__(self, number):
        Bot.__init__(number, "BogoBot")
        self.player_type = 'rng bot'
        random.seed()

    def compute_next_move(self, board, valid_moves):
        return random.choice(valid_moves)