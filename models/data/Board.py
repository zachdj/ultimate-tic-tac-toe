""" Board class

The Board class encapsulates the low-level representation of an Ultimate Tic-Tac-Toe board in the database.
The low-level representation of a board is a tuple with 82 attributes.  The first 81 attributes list the values of the
cells of the board starting from the top row.  The 82nd attribute is an identifier for the player whose turn comes next

# TODO ^ This probably needs refinement ^

This class provides a high-level interface for serializing/deserializing models.game.Macroboard objects to/from the
low-level board tuples used by the database

"""

class Board(object):
    # TODO