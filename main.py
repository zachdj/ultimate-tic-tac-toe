from game.Macroboard import Macroboard

board = Macroboard()

board.make_move(1, 0, 0, 0, 0)
board.make_move(1, 0, 0, 1, 1)
board.make_move(1, 0, 0, 2, 2)
board.make_move(1, 1, 1, 0, 0)
board.make_move(1, 1, 1, 1, 1)
board.make_move(1, 1, 1, 2, 2)
board.make_move(1, 2, 2, 0, 0)
board.make_move(1, 2, 2, 1, 1)
board.make_move(1, 2, 2, 2, 2)

print(board)
print(board.board_completed)
print(board.winner)