from models.game.bots.Bot import Bot
from models.game.Game import Game
from models.data.GameDataModel import GameDataModel


class Experiment(object):
    def __init__(self, player1, player2, iterations, record=True):
        """ An Experiment is a sequence of several games between two bots.  Results can be saved or discarded

        :param player1: the Bot playing as 'X'
        :param player2: the Bot playing as 'O'
        :param iterations: the number of games to play for this experiment
        :param record: boolean indicator - should the result of games be recorded or not?
        """
        if not isinstance(player1, Bot) or not isinstance(player2, Bot):
            raise Exception("Invalid Experiment: both players must be bots")

        self.p1 = player1
        self.p2 = player2
        self.iterations = iterations
        self.record_result = record

    def run(self, callback):
        """ Runs the current experiment.  The callback function will be called after each game is finished.

        :param callback: a function to call at the termination of each game.  The iteration number and winner will be passed as arguments
        :return: None
        """
        for i in list(range(0, self.iterations)):
            game = Game(self.p1, self.p2)
            game.finish_game()
            if self.record_result:
                game_dm = GameDataModel(game)
                game_dm.save()

            callback(i+1, game.get_winner())
