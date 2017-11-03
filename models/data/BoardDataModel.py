from . import DatabaseConnection as DB
from models.game.Board import Board

""" BoardDataModel class

The BoardDataModel class encapsulates the low-level representation of an Ultimate Tic-Tac-Toe board in the database.
The low-level representation of a board is a tuple with 86 attributes + a primary key.  
The primary key is a string representation of the flattened board, where 1 indicates an X, 2 indicates an O, 
    and 0 indicates an empty cell
    
The first 81 attributes list the values of the cells of the board starting from the top row.  
The 82nd attribute is an identifier for the player whose turn comes next
Attribute 83 is the number of wins recorded for this board state
Attribute 84 is the number of losses recorded for this board state
Attribute 85 is the number of ties recorded for this board state
Attribute 86 is the id of the game tuple in which this board was found

This class provides a high-level interface for serializing/deserializing models.game.GlobalBoard objects to/from the
low-level board tuples used by the database

"""


class BoardDataModel(object):
    def __init__(self, global_board, next_player, game_id):
        """
        Initializes a BoardDataModel
        :param global_board: the models.game.GlobalBoard to represent
        :param next_player: the player who would play next on the board (Board.X or Board.O)
        :param game_id: the id of the parent GameDataModel stored in this DB
        """
        self.parent_game_id = game_id
        self.next_player = next_player
        self.representation = []
        range = [0, 1, 2]
        for metarow in range:
            for metacol in range:
                for row in range:
                    for col in range:
                        if global_board.board[metarow][metacol].check_cell(row, col) == Board.X:
                            self.representation.append(1)
                        elif global_board.board[metarow][metacol].check_cell(row, col) == Board.O:
                            self.representation.append(2)
                        else:
                            self.representation.append(0)

        self.primary_key = "".join(map(str, self.representation)) + "np%s" % self.next_player
        self.string_representation = ",".join(map(str, self.representation))

        self.processed_representation = None  # TODO

    def _insert_model(self):
        """
        private function to insert this board into the database.  Win, loss, and tie counts are initialized to 0
        This should only be called if the board doesn't already exist in the database
        :return:
        """
        insert_script = "INSERT INTO board VALUES ('%s', %s, %s, 0, 0, 0, %s)" % (self.primary_key, self.string_representation, self.next_player, self.parent_game_id)
        DB.execute(insert_script)

    def _check_for_model(self):
        """
        private function to check if an instance of this board exists in the database
        :return: True if a board with this configuration already exists in the database.  False otherwise
        """
        cursor = DB.query("SELECT * FROM board WHERE id = '%s' ;" % self.primary_key)
        return cursor.fetchone() is not None

    def add_win(self):
        """
        Tallies up a win for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_WIN_SCRIPT = "UPDATE board SET wins = wins + 1 WHERE id = '%s' ;" % self.primary_key
        DB.execute(ADD_WIN_SCRIPT)

    def add_loss(self):
        """
        Tallies up a loss for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_LOSS_SCRIPT = "UPDATE board SET losses = losses + 1 WHERE id = '%s' ;" % self.primary_key
        DB.execute(ADD_LOSS_SCRIPT)

    def add_tie(self):
        """
        Tallies up a tie for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_TIE_SCRIPT = "UPDATE board SET ties = ties + 1 WHERE id = '%s' ;" % self.primary_key
        DB.execute(ADD_TIE_SCRIPT)
