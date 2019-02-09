

class Route:
    """
    The class for representing a route to a handler.
    """
    def __init__(self, pattern, handler):
        self.pattern = pattern
        self.handler = handler
