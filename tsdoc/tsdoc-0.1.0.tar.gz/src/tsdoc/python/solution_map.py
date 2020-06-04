from .positionable import Positionable
from .representable import Representable


class SolutionItem(Positionable, Representable):
    def __init__(self, parent, indentation, key, value):
        self.parent = parent
        self.indentation = indentation
        self.key = key
        self.value = value

    def __eq__(self, other):
        return (
            self.indentation == other.indentation
            and self.key == other.key  # noqa: W503
            and self.value == other.value  # noqa: W503
        )
