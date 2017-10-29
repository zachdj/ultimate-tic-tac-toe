from . import Move, Board, LocalBoard, GlobalBoard, Player


class Game(object):
    def __init__(self, player1, player2):
        """
        Game objects represent a game played between two opponents.  Zero, one, or both of the opponents can be bots
        :param player1: Player or Bot object corresponding to the 'X' player
        :param player2: Player or Bot object corresponding to the 'O' player
        """
        self.board = GlobalBoard()
        self.player1 = player1
        self.player2 = player2
        self.moves = []

    def make_move(self, move):
        """
        Applies the given move to this game
        :param move: the move to make
        :return: None
        """
        self.board.make_move(move)
        self.moves.append(move)


    def get_valid_moves(self):
        """
        Gets the valid moves for the current player.  Wrapper around the get_valid_moves method of GlobalBoard
        :return:
        """
        if len(self.moves) > 0:
            return self.board.get_valid_moves(self.moves[-1])
        else:
            return self.board.get_possible_moves()