from . import DatabaseConnection as DB
from models.game.Board import Board

""" BoardDataModel class

The BoardDataModel class encapsulates the low-level representation of an Ultimate Tic-Tac-Toe board in the database.
The low-level representation of a board is a tuple with 85 attributes + a primary key.  
The primary key is a string representation of the flattened board, where 1 indicates an X, 2 indicates an O, 
    and 0 indicates an empty cell
    
The first 81 attributes list the values of the cells of the board starting from the top row.  
The 82nd attribute is an identifier for the player whose turn comes next
Attribute 83 is the number of wins recorded for this board state
Attribute 84 is the number of losses recorded for this board state
Attribute 85 is the number of ties recorded for this board state

This class provides a high-level interface for serializing/deserializing models.game.GlobalBoard objects to/from the
low-level board tuples used by the database

"""


class BoardDataModel(object):
    def __init__(self, global_board, next_player):
        """
        Initializes a BoardDataModel
        :param global_board: the models.game.GlobalBoard to represent
        :param next_player: the player who would play next on the board (Board.X or Board.O)
        :param game_id: the id of the parent GameDataModel stored in this DB
        """
        self.next_player = next_player
        self.representation = []
        for i in list(range(0, 9)):
            metarow = i//3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j//3
                col = j % 3
                cell = global_board.board[metarow][metacol].check_cell(row, col)
                if cell == Board.X: self.representation.append(1)
                elif cell == Board.O: self.representation.append(2)
                else: self.representation.append(0)

        # self.primary_key = "".join(map(str, self.representation)) + "np%s" % self.next_player
        self.string_representation = ",".join(map(str, self.representation))

        self.processed_representation = None  # TODO

    def _insert_model(self):
        """
        private function to insert this board into the database.  Win, loss, and tie counts are initialized to 0
        This should only be called if the board doesn't already exist in the database
        :return:
        """
        insert_script = "INSERT INTO board VALUES (%s, %s, 0, 0, 0)" % (self.string_representation, self.next_player)
        DB.execute(insert_script)

    def _check_for_model(self):
        """
        private function to check if an instance of this board exists in the database
        :return: True if a board with this configuration already exists in the database.  False otherwise
        """
        cursor = DB.query("SELECT * FROM board %s ;" % self.assemble_key_query())
        return cursor.fetchone() is not None

    def add_win(self):
        """
        Tallies up a win for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_WIN_SCRIPT = "UPDATE board SET wins = wins + 1 %s ;" % self.assemble_key_query()
        DB.execute(ADD_WIN_SCRIPT)

    def add_loss(self):
        """
        Tallies up a loss for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_LOSS_SCRIPT = "UPDATE board SET losses = losses + 1 %s ;" % self.assemble_key_query()
        DB.execute(ADD_LOSS_SCRIPT)

    def add_tie(self):
        """
        Tallies up a tie for this board state in the current database
        :return: None
        """
        if not self._check_for_model():
            self._insert_model()

        ADD_TIE_SCRIPT = "UPDATE board SET ties = ties + 1 %s ;" % self.assemble_key_query()
        DB.execute(ADD_TIE_SCRIPT)

    def assemble_key_query(self):
        """
        Creates the WHERE statement that asks for the board with a matching representation
        :return: a String "WHERE p00 = <value> AND p01 = <value> ... AND next_player = <value>"
        """
        query = "WHERE next_player = %s " % self.next_player
        for row in list(range(0, 9)):
            for col in list(range(0, 9)):
                flattened_index = row * 9 + col
                attr_query = "AND p%s%s = %s " % (row, col, self.representation[flattened_index])
                query += attr_query

        return query

