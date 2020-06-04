from .positionable import Positionable
from .representable import Representable


class QuestionAbstract(Positionable, Representable):
    def __init__(self, parent, indentation, question, answer):
        self.parent = parent
        self.indentation = indentation
        self.question = question
        self.answer = answer

    def __eq__(self, other):
        return (
            self.indentation == other.indentation
            and self.question == other.question  # noqa: W503
            and self.answer == other.answer  # noqa: W503
        )

    def __str__(self):
        return ""
