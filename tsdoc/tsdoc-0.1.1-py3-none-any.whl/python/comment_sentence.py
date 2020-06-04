from tsdoc.python.model import Model
from tsdoc.python.segment import Segment
from textwrap import fill
from typing import Final
from typing import Optional

import attr


@attr.s(auto_attribs=True, kw_only=True)
class CommentSentence(Segment):
    parent: Optional[Model] = attr.ib(eq=False)
    indentation: Final[str]  # type: ignore[misc]
    text: Final[str]  # type: ignore[misc]

    @property
    def code(self) -> str:
        text_pruned = self.text.replace("`", "").rstrip(".")
        return self._wrap_comment_or_ignore_string_literal(text_pruned)

    def _wrap_comment_or_ignore_string_literal(self, text: str) -> str:
        # Entire-line string literals are not wrapped because students' may want to
        # copy-and-paste them into their code.
        if text.startswith('"') and text.endswith('"'):
            return f"{self.indentation}# {text}"

        indent = f"{self.indentation}# "
        width = 55

        return fill(text, width, initial_indent=indent, subsequent_indent=indent)

    @property
    def callout(self) -> str:
        return self.text
