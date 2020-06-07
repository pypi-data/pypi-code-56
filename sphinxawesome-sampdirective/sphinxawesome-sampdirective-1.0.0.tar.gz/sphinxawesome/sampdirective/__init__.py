"""
This file defines a new directive `.. samp::`, which behaves like
the `:samp:` role.

:copyright: Copyright 2020, Kai Welke.
:license: MIT, see LICENSE for details
"""

import re
from typing import Any, Dict, List

from docutils import nodes
from docutils.nodes import Node
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)

__version__ = "1.0.0"


class SampDirective(SphinxDirective):
    """
    Directive for a literal block with emphasis.
    That is, anything in '{}' will become emphasized nodes.
    """

    has_content = True

    def run(self) -> List[Node]:
        """Create a literal block and parse the children."""

        code = "\n".join(self.content)
        children = self.parse(code)
        node = nodes.literal_block(code, "", *children)

        self.add_name(node)
        return [node]

    def parse(self, content: str) -> List[Node]:
        """
        Parse a literal code block for {PATTERN}
        """

        result = []
        stack = [""]
        parentheses = re.compile(r"({|})")

        # cheat syntax highlighting for the prompt
        if content[0] in ["$", "#", "~"]:
            prompt, content = content[0], content[1:]
            result.append(nodes.inline(prompt, prompt, classes=["gp"]))

        for token in parentheses.split(content):
            if token == "{":
                stack.append("{")
                stack.append("")
            elif token == "}":
                if len(stack) == 3 and stack[1] == "{" and len(stack[2]) > 0:
                    if stack[0]:
                        result.append(nodes.Text(stack[0], stack[0]))
                        result.append(
                            nodes.emphasis(stack[2], stack[2], classes=["var"])
                        )
                    stack = [""]
                else:
                    stack.append("")
                    stack = ["".join(stack)]
            else:
                stack[-1] += token

        if "".join(stack):
            text = "".join(stack)
            result.append(nodes.Text(text, text))

        return result


def setup(app: "Sphinx") -> Dict[str, Any]:
    """Register the directive."""

    app.add_directive("samp", SampDirective)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
