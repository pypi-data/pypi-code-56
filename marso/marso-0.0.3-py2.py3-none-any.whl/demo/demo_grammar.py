from marso.grammar import Grammar
from marso.python.errors import ErrorFinderConfig
from marso.python.parser import Parser as PythonParser
from marso.python.tokenizer import tokenize_lines, tokenize
from marso.python.token import PythonTokenTypes
from marso.utils import split_lines, parse_version_string


class DemoGrammar(Grammar):
    _error_normalizer_config = ErrorFinderConfig()
    _token_namespace = PythonTokenTypes
    _start_nonterminal = 'file_input'
    language = "demo"

    def __init__(self, bnf_text):
        super(DemoGrammar, self).__init__(
            bnf_text,
            tokenizer=self._tokenize_lines,
            parser=PythonParser,
            # diff_parser=DiffParser
        )
        self.version_info = parse_version_string("1.0")

    def _tokenize_lines(self, lines, **kwargs):
        return tokenize_lines(lines, self.version_info, **kwargs)

    def _tokenize(self, code):
        # Used by Jedi.
        return tokenize(code, self.version_info)

