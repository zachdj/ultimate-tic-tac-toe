from .BogoBot import BogoBot
from .MonteCarloBot import MonteCarloBot
from .ExampleMinimaxBot import ExampleMinimaxBot

"""
The BotLoader module loads a list of all bots with a human-readable name, description, and difficulty (0-10)

This module is used in the SetupGame and SetupExperiment scenes to provide the user with a selectable list of Bot types
"""

bots = [
    {
        "title" : "Random Bot",
        "description": "Chooses moves at random.",
        "difficulty": 0,
        'requires_time_limit': False,
        "data": BogoBot
     },
    {
        "title": "Monte Carlo Search Tree",
        "description": "Uses the Monte Carlo Search Tree algorithm to play..",
        "difficulty": 2,
        'requires_time_limit': True,
        "data": MonteCarloBot
     },
    {
        "title": "Example Minimax Bot",
        "description": "Example minimax bot with a nonsensical scoring function",
        "difficulty": 2,
        'requires_time_limit': False,
        "data": ExampleMinimaxBot
    }
]


def get_bots():
    return bots

