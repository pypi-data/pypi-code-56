from .positionable import Positionable
from .representable import Representable


class CommentConcrete(Positionable, Representable):
    def __init__(self, parent, indentation, sentences):
        self.parent = parent
        self.indentation = indentation
        self.sentences = sentences

    def __eq__(self, other):
        return (
            self.indentation == other.indentation and self.sentences == other.sentences
        )

    def __str__(self):
        return ""
