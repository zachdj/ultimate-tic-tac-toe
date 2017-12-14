from .BogoBot import BogoBot
from .RandoMaxBot import RandoMaxBot
from .MCTSBot import MCTSBot
from .Heuristic1Bot import Heuristic1Bot
from .Heuristic2Bot import Heuristic2Bot
from .Heuristic3Bot import Heuristic3Bot

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
        "title": "Monte Carlo Tree Search",
        "description": "Uses the Monte Carlo Tree Search algorithm to play..",
        "difficulty": 5,
        "data": MCTSBot
     },
    {
        "title": "Minimax Bot H1",
        "description": "Uses the H1 heuristic to play",
        "difficulty": 5,
        "data": Heuristic1Bot
     },
    {
        "title": "Minimax Bot H2",
        "description": "Uses the H2 heuristic to play",
        "difficulty": 6,
        "data": Heuristic2Bot
     },
    {
        "title": "Minimax Bot H3",
        "description": "Uses the H3 heuristic to play",
        "difficulty": 7,
        "data": Heuristic3Bot
     }
]


def get_bots():
    return bots

