class InvalidMicroboardMoveException (Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidMacroboardMoveException (Exception):
    def __init__(self, message):
        super().__init__(message)