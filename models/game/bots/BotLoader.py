from .BogoBot import BogoBot
from .MonteCarloBot import MonteCarloBot
from .RandoMaxBot import RandoMaxBot
from .MinimaxNeuralNetBot import MinimaxNeuralNetBot

"""
The BotLoader module loads a list of all bots with a human-readable name, description, and difficulty (0-10)

This module is used in the SetupGame and SetupExperiment scenes to provide the user with a selectable list of Bot types
Right now, the "difficulty" and "description" values are not used for anything.  In the future, they may be used in the 
menu where bots are selected
"""

bots = [
    {
        "title" : "Random Bot",
        "description": "Chooses moves at random.",
        "difficulty": 0,
        "data": BogoBot
     },
    {
        "title": "RandoMax Bot",
        "description": "Bot that moves randomly unless a winning move is available",
        "difficulty": 1,
        "data": RandoMaxBot
    },
    {
        "title": "Monte Carlo Search Tree",
        "description": "Uses the Monte Carlo Search Tree algorithm to play..",
        "difficulty": 3,
        "data": MonteCarloBot
     },
    {
        "title": "MLP Minimax Bot",
        "description": "Minimax bot that uses a Neural Net to score boards",
        "difficulty": 5,
        "data": MinimaxNeuralNetBot
    }
]


def get_bots():
    return bots

