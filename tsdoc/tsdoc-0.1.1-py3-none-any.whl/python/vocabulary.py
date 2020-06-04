from tsdoc.python.model import Model
from tsdoc.python.segment import Segment
from tsdoc.python.vocabulary_term import VocabularyTerm
from typing import Final
from typing import Iterable
from typing import Optional
from typing import Tuple

import attr


# This converter wrapper-function is used because of a bug with the mypy-attrs plugin.
# https://github.com/python/mypy/issues/8389
def _tuple(iterable: Iterable[VocabularyTerm]) -> Tuple[VocabularyTerm, ...]:
    return tuple(iterable)


@attr.s(auto_attribs=True, kw_only=True)
class Vocabulary(Segment):
    parent: Optional[Model] = attr.ib(eq=False)
    indentation: Final[str]  # type: ignore[misc]
    terms: Final[Tuple[VocabularyTerm, ...]] = attr.ib(converter=_tuple)
