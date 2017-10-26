import unittest
from . import Move, Board

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

if __name__ == '__main__':
    unittest.main()