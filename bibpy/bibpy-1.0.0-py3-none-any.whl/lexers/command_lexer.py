# -*- coding: utf-8 -*-

"""Lexer class for LaTeX commands."""

from bibpy.compat import u
from bibpy.lexers.base_lexer import BaseLexer


class CommandLexer(BaseLexer):
    """Lexer for LaTeX commands such \\textyen."""

    def __init__(self):
        super(CommandLexer, self).__init__()
        self.reset('')
        self.mode = ''

        self.modes = {
            'command': self.lex_command,
            'braced': None
        }

        self._compile_regexes([
            ('backslash', (u('\\'), None)),
            ('lbrace',    (u('{'), self.lex_lbrace)),
            ('rbrace',    (u('}'), self.lex_rbrace)),
        ])

    def lex_lbrace(self, value):
        self.brace_level += 1

        if self.brace_level == 1:
            self.mode = 'value'
        elif self.brace_level > 1:
            self.mode = 'value'

        return self.make_token('lbrace', value)

    def lex_rbrace(self, value):
        self.brace_level -= 1

        if self.brace_level == 0:
            self.mode = 'command'
        elif self.brace_level < 0:
            raise self.raise_unbalanced()

        return self.make_token('rbrace', value)

    def lex_command(self):
        _, token = self.until('backslash')

        if token:
            pass
