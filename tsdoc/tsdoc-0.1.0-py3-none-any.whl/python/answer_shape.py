from .positionable import Positionable
from .representable import Representable


class AnswerShape(Positionable, Representable):
    def __init__(self, parent, indentation, text):
        self.parent = parent
        self.indentation = indentation
        self.text = text

    def __eq__(self, other):
        return self.indentation == other.indentation and self.text == other.text
