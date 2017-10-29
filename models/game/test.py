import unittest
from . import Move, Board, LocalBoard, GlobalBoard

class MoveUnitTest(unittest.TestCase):
    def setUp(self):
        self.move1 = Move(Board.X, 0, 0, 0, 0)
        self.move2 = Move(Board.X, 1, 0, 0, 0)
        self.move3 = Move(Board.X, 2, 1, 2, 1)
        self.move4 = Move(Board.X, 0, 2, 1, 2)

    def test_abs_row(self):
        self.assertEqual(self.move1.abs_row, 0)
        self.assertEqual(self.move2.abs_row, 3)
        self.assertEqual(self.move3.abs_row, 8)
        self.assertEqual(self.move4.abs_row, 1)
    
    def test_abs_col(self):
        self.assertEqual(self.move1.abs_col, 0)
        self.assertEqual(self.move2.abs_col, 0)
        self.assertEqual(self.move3.abs_col, 4)
        self.assertEqual(self.move4.abs_col, 8)

    def test_out_of_bounds_input(self):
        with self.assertRaises(Exception):
            bad_move = Move(55, 0, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 3, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 3, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 0, 0, 3, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 0, 0, 3)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, -3, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, -3, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 0, 0, -3, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 0, 0, -3)


class LocalBoardUnitTest(unittest.TestCase):
    def test_moves(self):
        board1 = LocalBoard()
        move1 = Move(Board.X, 0, 0, 0, 0)
        board1.make_move(move1)
        self.assertEqual(board1.check_cell(0, 0), Board.X)

        with self.assertRaises(Exception):
            move2 = Move(Board.O, 0, 0, 0, 0)
            board1.make_move(move2)
        with self.assertRaises(Exception):
            move2 = Move(Board.O, 0, 1, 0, 0)
            board1.make_move(move2)

        move2 = Move(Board.O, 0, 1, 1, 0)
        board1.make_move(move2)
        self.assertEqual(board1.check_cell(1, 0), Board.O)

        self.assertFalse(board1.board_completed)
        self.assertEqual(board1.winner, Board.EMPTY)

    def test_game_over(self):
        # win a board and check the winner
        move_seq1 = [
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.X, 0, 0, 1, 1),
            Move(Board.X, 0, 0, 2, 2)
        ]
        board = LocalBoard()
        for move in move_seq1:
            board.make_move(move)
        self.assertTrue(board.board_completed)
        self.assertEqual(board.winner, Board.X)

class GlobalBoardUnitTest(unittest.TestCase):
    def test_moves(self):
        board = GlobalBoard()
        moves = [
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.X, 0, 0, 1, 1),
            Move(Board.X, 0, 0, 2, 2),
            Move(Board.X, 1, 1, 0, 0),
            Move(Board.X, 1, 1, 1, 1),
            Move(Board.X, 1, 1, 2, 2),
            Move(Board.X, 2, 2, 0, 0),
            Move(Board.X, 2, 2, 1, 1),
            Move(Board.X, 2, 2, 2, 2),
        ]

        for move in moves:
            board.make_move(move)

        self.assertTrue(board.board_completed)
        self.assertEqual(board.winner, Board.X)

        with self.assertRaises(Exception):
            board.make_move(Move(Board.O, 2, 2, 0, 0))


if __name__ == '__main__':
    unittest.main()