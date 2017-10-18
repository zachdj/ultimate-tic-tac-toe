class InvalidMicroboardMoveException (Exception):
    """ Exception thrown when an invalid move is attempted at the microboard level
    """
    def __init__(self, message):
        super().__init__(message)