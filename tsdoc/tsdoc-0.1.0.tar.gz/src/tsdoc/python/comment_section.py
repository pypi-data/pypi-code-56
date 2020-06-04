from .positionable import Positionable
from .representable import Representable


class CommentSection(Positionable, Representable):
    def __init__(self, parent, indentation, noun):
        self.parent = parent
        self.indentation = indentation
        self.noun = noun

    def __eq__(self, other):
        return self.indentation == other.indentation and self.noun == other.noun

    def __str__(self):
        return "{}#### ---- {} ---- ####".format(self.indentation, self.noun)
