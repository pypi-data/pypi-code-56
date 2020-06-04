from .positionable import Positionable
from .representable import Representable


class Keywords(Positionable, Representable):
    def __init__(self, parent, indentation, terms):
        self.parent = parent
        self.indentation = indentation
        self.terms = terms

    def __eq__(self, other):
        return self.indentation == other.indentation and self.terms == other.terms

    def __str__(self):
        return ""
