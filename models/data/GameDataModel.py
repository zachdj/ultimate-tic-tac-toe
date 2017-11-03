import datetime
from . import DatabaseConnection as DB
from . import BoardDataModel
from models.game import GlobalBoard, Board

class GameDataModel(object):
    def __init__(self, game):
        """ Initializes a GameDataModel instance
        The GameDataModel class encapsulates the representation of an Ultimate Tic-Tac-Toe game in the database.
        Each game has a unique id (auto-incremented)

        This class provides a high-level interface for serializing/deserializing models.game.Game objects
        and their associated board states to models understood by the database

        :param game: the models.game.Game object to represent
        """
        if not game.is_game_over():
            raise Exception("You cannot record the result of a game which has not been completed")
        self.game = game

    def save(self):
        # first save the game tuple
        GAME_INSERT_SCRIPT = "INSERT INTO game VALUES ('%s', '%s', '%s', '%s')" \
                             % (self.game.player1.player_type, self.game.player2.player_type,
                                datetime.date.today().strftime("%d/%m/%Y"), len(self.game.moves))
        DB.execute(GAME_INSERT_SCRIPT)

        # get the id of the inserted game tuple
        cursor = DB.query('SELECT max(rowid) FROM game')
        game_id = cursor.fetchone()[0]

        # save each board state
        board = GlobalBoard()
        for move in self.game.moves:
            board.make_move(move)
            if move.player == Board.X:
                next_player = Board.O
            else:
                next_player = Board.X
            board_data = BoardDataModel(board, next_player, game_id)

            if self.game.get_winner() == Board.X:
                board_data.add_win()
            elif self.game.get_winner() == Board.O:
                board_data.add_loss()
            else:
                board_data.add_tie()
