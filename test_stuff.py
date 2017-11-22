"""
Temporary module for running human tests
"""
from models.game import *
from models.data import DatabaseConnection as DB, GameDataModel, BoardDataModel
import timeit, random


def full_game_experiment(total_games, purge=10):
    """
    Simulates many random games from start to finish and records each in the database
    Board states that have fewer than "purge" records will be removed from the database
    :return: None
    """
    p1_wins = 0
    p2_wins = 0
    ties = 0
    total_games = total_games
    total_moves = 0

    p1 = BogoBot(Board.X)
    p2 = BogoBot(Board.O)

    print("Playing %s games... \n" % total_games)
    start_time = timeit.default_timer()

    for i in list(range(0, total_games)):
        print("Playing game %s..." % (i+1))
        game = Game(p1, p2)
        winner = game.finish_game()
        if winner == Board.X:
            p1_wins += 1
        elif winner == Board.O:
            p2_wins += 1
        else:
            ties += 1

        total_moves += len(game.moves)

        game_data = GameDataModel(game)
        game_data.save()

    if purge > 0:
        DB.purge_boards(purge)
    DB.close()



    elapsed = timeit.default_timer() - start_time

    print("Done in %s s \n" % elapsed)

    print("Player 1 Won %s %% of the games" % round(p1_wins*100 / total_games))
    print("Player 2 Won %s %% of the games" % round(p2_wins*100 / total_games))
    print("The Cat got %s %% of the games" % round(ties*100 / total_games))
    print("Average number of moves: %s" % round(total_moves / total_games))


def mid_game_experiment(starting_boards, games_per_board, purge=10):
    STARTING_BOARDS = starting_boards
    GAMES_PER_BOARD = games_per_board
    MOVE_SEQUENCE_LENGTH = 25

    print("Generating mid-game data for %s boards..." % STARTING_BOARDS)

    p1 = BogoBot(Board.X)
    p2 = BogoBot(Board.O)

    print("Generating move sequences...")
    move_sequences = []
    for i in list(range(0, STARTING_BOARDS)):
        game = Game(p1, p2)
        # generate a move sequence that will take us to this board
        sequence = []
        for j in list(range(0, MOVE_SEQUENCE_LENGTH)):
            move = game._take_step()
            sequence.append(move)

        move_sequences.append(sequence)

    # we now have several move sequences that will take us to a fixed mid-game state - generate data for each of these
    for idx, sequence in enumerate(move_sequences):
        print("Generating data for move sequence %s" % (idx + 1))
        for experiment in list(range(0, GAMES_PER_BOARD)):
            game = Game(p1, p2)
            for move in sequence:  # bring the game to its mid-completed state
                game.make_move(move)

            # finish the game randomly and save
            game.finish_game()

            game_data = GameDataModel(game)
            game_data.save()

        # remove all the "junk" data that we don't need - this keeps the database from growing too large when long experiments are run
        DB.purge_boards(purge)

    print("Done!")

    DB.close()


def late_game_experiment(starting_boards, games_per_board, purge=10):
    STARTING_BOARDS = starting_boards
    GAMES_PER_BOARD = games_per_board
    MOVE_SEQUENCE_LENGTH = 45

    print("Generating late-game data for %s boards..." % STARTING_BOARDS)

    p1 = BogoBot(Board.X)
    p2 = BogoBot(Board.O)

    print("Generating move sequences...")
    move_sequences = []
    i = 0
    while i < STARTING_BOARDS:
        game = Game(p1, p2)
        # generate a move sequence that will take us to this board
        sequence = []
        for j in list(range(0, MOVE_SEQUENCE_LENGTH)):
            move = game._take_step()
            sequence.append(move)

        if not game.is_game_over():
            move_sequences.append(sequence)
            i += 1

    # we now have several move sequences that will take us to a fixed mid-game state - generate data for each of these
    for idx, sequence in enumerate(move_sequences):
        print("Generating data for move sequence %s" % (idx + 1))
        for experiment in list(range(0, GAMES_PER_BOARD)):
            game = Game(p1, p2)
            for move in sequence:  # bring the game to its mid-completed state
                game.make_move(move)

            # finish the game randomly and save
            game.finish_game()

            game_data = GameDataModel(game)
            game_data.save()

        # remove all the "junk" data that we don't need - this keeps the database from growing too large when long experiments are run
        DB.purge_boards(purge)

    print("Done!")

    DB.close()

p1 = BogoBot(Board.X, 5)
p2 = BogoBot(Board.O, 5)
experiment = Experiment(p1, p2, 100, True)
experiment.run(callback=lambda x,y: print(x))


# full_game_experiment(10)
# mid_game_experiment(1, 15)
# late_game_experiment(75, 100)