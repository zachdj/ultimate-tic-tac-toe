"""
Temporary module for running human tests
"""
from models.game import *
import timeit

p1_wins = 0
p2_wins = 0
ties = 0
total_games = 10000
total_moves = 0

p1 = BogoBot(Board.X)
p2 = BogoBot(Board.O)

print("Playing %s games... \n" % total_games)
start_time = timeit.default_timer()

for i in list(range(0, total_games)):
    game = Game(p1, p2)
    winner = game.finish_game()
    if winner == Board.X:
        p1_wins += 1
    elif winner == Board.O:
        p2_wins += 1
    else:
        ties += 1

    total_moves += len(game.moves)

elapsed = timeit.default_timer() - start_time

print("Done in %s s \n" % elapsed)

print("Player 1 Won %s %% of the games" % round(p1_wins*100 / total_games))
print("Player 2 Won %s %% of the games" % round(p2_wins*100 / total_games))
print("The Cat got %s %% of the games" % round(ties*100 / total_games))
print("Average number of moves: %s" % round(total_moves / total_games))