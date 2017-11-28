from models.game.bots.MinimaxBot import MinimaxBot
from models.data.BoardDataModel import BoardDataModel
import weka.core.serialization as serialization
from weka.classifiers import Classifier


class MinimaxNeuralNetBot(MinimaxBot):
    def __init__(self, number, max_depth=5, name=None):
        """
        Minimax bot which uses a Multilayer Perceptron (MLP) model to score board states

        :param number:  Board.X for player1 or Board.O for player2
        :param max_depth:  The maximum depth of the lookahead
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "Minimax MLP Bot"
        MinimaxBot.__init__(self, number, max_depth, name=name)
        self.player_type = 'mlp minimax'

        objects = serialization.read_all("models/game/bots/weka_models/mlp_final.model")
        self.classifier = Classifier(jobject=objects[0])

    def compute_score(self, board):
        data_model = BoardDataModel(board)
        weka_instance = data_model.get_weka_instance(categorical=True)
        category = self.classifier.classify_instance(weka_instance)  # category will be one of the ten classes
        #  converts the class value into a numeric score between -1 and 1.   E.g. class 1 gets converted to -0.90, class 3 is converted to -0.50, class 10 is converted to 0.90, etc.
        score = ((category - 5.0) / 5.0) - 0.1
        return score
