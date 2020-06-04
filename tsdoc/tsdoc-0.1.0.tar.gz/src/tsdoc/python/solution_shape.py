from .positionable import Positionable
from .representable import Representable


class SolutionShape(Positionable, Representable):
    def __init__(self, parent, indentation, pseudocodes, items):
        self.parent = parent
        self.indentation = indentation
        self.pseudocodes = pseudocodes
        self.items = items

    def __eq__(self, other):
        return (
            self.indentation == other.indentation
            and self.pseudocodes == other.pseudocodes  # noqa: W503
            and self.items == other.items  # noqa: W503
        )

    def __str__(self):
        return ""
