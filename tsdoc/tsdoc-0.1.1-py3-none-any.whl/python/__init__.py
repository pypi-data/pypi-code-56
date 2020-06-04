from os.path import dirname, join
from textx import language, metamodel_from_file
from textx.metamodel import TextXMetaModel
from tsdoc.python.activity_header import ActivityHeader
from tsdoc.python.activity_part import ActivityPart
from tsdoc.python.answer_abstract import AnswerAbstract
from tsdoc.python.answer_shape import AnswerShape
from tsdoc.python.comment_abstract import CommentAbstract
from tsdoc.python.comment_concrete import CommentConcrete
from tsdoc.python.comment_paragraph import CommentParagraph
from tsdoc.python.comment_run_your_code import CommentRunYourCode
from tsdoc.python.comment_section import CommentSection
from tsdoc.python.comment_sentence import CommentSentence
from tsdoc.python.keywords import Keywords
from tsdoc.python.model import Model
from tsdoc.python.solution_code import SolutionCode
from tsdoc.python.line_blank import LineBlank
from tsdoc.python.point_tricky import PointTricky
from tsdoc.python.question_abstract import QuestionAbstract
from tsdoc.python.question_review import QuestionReview
from tsdoc.python.question_shape import QuestionShape
from tsdoc.python.question_structure import QuestionStructure
from tsdoc.python.segment import Segment  # noqa :F401
from tsdoc.python.solution_item import SolutionItem
from tsdoc.python.solution_pseudocode import SolutionPseudocode
from tsdoc.python.solution_shape import SolutionShape
from tsdoc.python.vocabulary_term import VocabularyTerm
from tsdoc.python.vocabulary import Vocabulary
from tsdoc import __version__

filename_ext = f".tsdoc{__version__.split('.')[0]}.py"

metamodel: TextXMetaModel = metamodel_from_file(
    join(dirname(__file__), "tsdoc.python.tx"),
    classes=[
        ActivityHeader,
        ActivityPart,
        AnswerAbstract,
        AnswerShape,
        CommentAbstract,
        CommentConcrete,
        CommentParagraph,
        CommentRunYourCode,
        CommentSection,
        CommentSentence,
        Keywords,
        Model,
        SolutionCode,
        LineBlank,
        PointTricky,
        QuestionAbstract,
        QuestionReview,
        QuestionShape,
        QuestionStructure,
        SolutionItem,
        SolutionPseudocode,
        SolutionShape,
        VocabularyTerm,
        Vocabulary,
    ],
    use_regexp_group=True,
)

metamodel.register_obj_processors(
    {
        "QuestionAbstract": QuestionAbstract.process_optional_answer,
        "QuestionShape": QuestionShape.process_optional_answer,
    }
)


@language("TSDoc Python", f"*{filename_ext}")
def register() -> TextXMetaModel:
    "An embedded comment language for TechSmart Python files."
    return metamodel
