from game.Microboard import Microboard

board = Microboard()

print(board.board_completed)
print("%s \n\n" % board)

board.make_move(1, 0, 0)
print("%s \n\n" % board)


board.make_move(2, 0, 2)
print("%s \n\n" % board)


board.make_move(2, 1, 2)
print("%s \n\n" % board)


board.make_move(1, 1, 0)
print("%s \n\n" % board)


board.make_move(1, 2, 0)
print("%s \n\n" % board)

board.make_move(2, 2, 2)
print("%s \n\n" % board)

print(board.board_completed)
print(board.winner)