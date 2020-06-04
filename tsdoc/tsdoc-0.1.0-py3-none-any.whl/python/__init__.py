from os.path import dirname, join
from textx import language, metamodel_from_file
from .answer_abstract import AnswerAbstract
from .answer_shape import AnswerShape
from .comment_abstract import CommentAbstract
from .comment_concrete import CommentConcrete
from .comment_paragraph import CommentParagraph
from .comment_section import CommentSection
from .comment_sentence import CommentSentence
from .keywords import Keywords
from .line_code import LineCode
from .question_abstract import QuestionAbstract
from .question_review import QuestionReview
from .question_shape import QuestionShape
from .question_structure import QuestionStructure
from .solution_map import SolutionItem
from .solution_pseudocode import SolutionPseudocode
from .solution_shape import SolutionShape


metamodel = metamodel_from_file(
    join(dirname(__file__), "tsdoc.python.tx"),
    classes=[
        AnswerAbstract,
        AnswerShape,
        CommentAbstract,
        CommentConcrete,
        CommentParagraph,
        CommentSection,
        CommentSentence,
        Keywords,
        LineCode,
        QuestionAbstract,
        QuestionReview,
        QuestionShape,
        QuestionStructure,
        SolutionItem,
        SolutionPseudocode,
        SolutionShape,
    ],
    use_regexp_group=True,
)


@language("TSDoc Python", "*.tsdoc.py")
def register():
    "An embedded comment language for TechSmart Python files."
    return metamodel
