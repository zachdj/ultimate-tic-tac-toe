""" ProcessedBoard class

The ProcessedBoard class encapsulates the high-level representation of an Ultimate Tic-Tac-Toe board in the database.
The high-level representation consists of a set of meta-information about the board.  For example - how many boards are
currently owned by X, how many boards are owned by O, number of "attacking sequences" for either player, or any other
high-level summary attribute that we decide to use.

# TODO ^ This probably needs refinement ^

This class provides a high-level interface for serializing models.game.Macroboard objects to the
high-level board tuples used by the database.
Deserialization is not possible, since the mapping of a board to its high-level representation is not one-to-one

"""

class ProcessedBoard(object):
    # TODO