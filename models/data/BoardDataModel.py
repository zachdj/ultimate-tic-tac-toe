from . import DatabaseConnection as DB
from models.game.Board import Board

class BoardDataModel(object):
    def __init__(self, global_board):
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

        :param global_board: the models.game.GlobalBoard to represent
        """
        self.representation = []
        x_count, o_count = 0, 0
        for i in list(range(0, 9)):
            metarow = i//3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j//3
                col = j % 3
                cell = global_board.board[metarow][metacol].check_cell(row, col)
                if cell == Board.X:
                    self.representation.append(1)
                    x_count += 1
                elif cell == Board.O:
                    self.representation.append(2)
                    o_count += 1
                else: self.representation.append(0)

        if x_count > o_count:
            self.next_player = Board.O
        else:
            self.next_player = Board.X

        self.string_representation = ",".join(map(str, self.representation))
        self.KEY_QUERY = "WHERE next_player = %s " % self.next_player
        for row in list(range(0, 9)):
            for col in list(range(0, 9)):
                flattened_index = row * 9 + col
                attr_query = "AND p%s%s = %s " % (row, col, self.representation[flattened_index])
                self.KEY_QUERY += attr_query
        self.INSERT_SCRIPT = "INSERT OR IGNORE INTO board VALUES (%s, %s, 0, 0, 0); " % (self.string_representation, self.next_player)
        self.ADD_WIN_SCRIPT = "UPDATE board SET wins = wins + 1 %s ; " % self.KEY_QUERY
        self.ADD_LOSS_SCRIPT = "UPDATE board SET losses = losses + 1 %s ; " % self.KEY_QUERY
        self.ADD_TIE_SCRIPT = "UPDATE board SET ties = ties + 1 %s ; " % self.KEY_QUERY

        self.processed_representation = None  # TODO

    def get_insert_script(self, type='win'):
        script = "INSERT OR IGNORE INTO board VALUES (%s, %s, 0, 0, 0); " % (self.string_representation, self.next_player)
        if type == 'win':
            script += self.ADD_WIN_SCRIPT
        elif type == 'loss':
            script += self.ADD_LOSS_SCRIPT
        else:
            script += self.ADD_TIE_SCRIPT

        return script

    def _insert_model(self):
        """
        private function to insert this board into the database.  Win, loss, and tie counts are initialized to 0
        This statement will be ignored if the board state already exists in the database
        :return:
        """
        DB.execute(self.INSERT_SCRIPT)

    def add_win(self):
        """
        Tallies up a win for this board state in the current database
        :return: None
        """
        self._insert_model()

        DB.execute(self.ADD_WIN_SCRIPT)

    def add_loss(self):
        """
        Tallies up a loss for this board state in the current database
        :return: None
        """
        self._insert_model()

        DB.execute(self.ADD_LOSS_SCRIPT)

    def add_tie(self):
        """
        Tallies up a tie for this board state in the current database
        :return: None
        """
        self._insert_model()
        DB.execute(self.ADD_TIE_SCRIPT)
