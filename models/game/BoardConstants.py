class BoardConstants:
    X = 1
    X_WIN_COND = X*3
    O = 2
    O_WIN_COND = O*3
    EMPTY = -2

"""
TODO: refactor to get rid of this silliness.  Probably should make a parent Board class from which Macroboard and 
Microboard inherit
"""