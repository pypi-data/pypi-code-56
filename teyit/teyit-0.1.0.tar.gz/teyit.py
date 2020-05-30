import argparse
import ast
import copy
import tokenize
from contextlib import suppress
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List

OPERATOR_TABLE = {
    ast.Eq: "assertEqual",
    ast.NotEq: "assertNotEqual",
    ast.Lt: "assertLess",
    ast.LtE: "assertLessEqual",
    ast.Gt: "assertGreater",
    ast.GtE: "assertGreaterEqual",
    ast.In: "assertIn",
    ast.NotIn: "assertNotIn",
    ast.Is: "assertIs",
    ast.IsNot: "assertIsNot",
}


@dataclass
class Rewrite:
    node: ast.Call
    func: str
    args: List[ast.AST]

    def __hash__(self):
        return hash(id(self))

    @lru_cache(maxsize=1)
    def build_node(self):
        new_node = copy.deepcopy(self.node)
        new_node.func.attr = self.func
        new_node.args = self.args
        return new_node

    @lru_cache(maxsize=1)
    def get_arg_offset(self):
        new_node = self.build_node()
        prev_args = len(self.node.args + self.node.keywords)
        return len(new_node.args + new_node.keywords) - prev_args


class AssertRewriter(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        self.asserts = []
        super().__init__(*args, **kwargs)

    def visit_Call(self, node):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and ast.unparse(node.func.value) == "self"
            and node.func.attr.startswith("assert")
            and hasattr(self, f"visit_{node.func.attr}")
        ):
            return node
        if rewrite := getattr(self, f"visit_{node.func.attr}")(node):
            self.asserts.append(rewrite)

    def visit_assertTrue(self, node):
        expr, *args = node.args
        if isinstance(expr, ast.Compare) and len(expr.ops) == 1:
            left = expr.left
            operator = type(expr.ops[0])
            (comparator,) = expr.comparators
            if (
                operator in (ast.Is, ast.IsNot)
                and isinstance(comparator, ast.Constant)
                and comparator.value is None
            ):
                func = f"assert{operator.__name__}None"
                args = [left, *args]
            elif operator in OPERATOR_TABLE:
                func = OPERATOR_TABLE[operator]
                args = [left, comparator, *args]
            else:
                return None
        elif (
            isinstance(expr, ast.Call)
            and ast.unparse(expr.func) == "isinstance"
            and len(expr.args) == 2
        ):
            func = "assertIsInstance"
            args = [*expr.args, *args]
        else:
            return None
        return Rewrite(node, func, args)


class _FormattedUnparser(ast._Unparser):
    # do not use private APIs, unless you
    # authored it :P
    def __init__(self, indent_width=4, comments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_first_call = True
        self._indent_text = " " * indent_width
        self._comments = comments

    def visit_Call(self, node):
        first_call = self._is_first_call
        if self._is_first_call:
            self._is_first_call = False
        self.set_precedence(ast._Precedence.ATOM, node.func)
        self.traverse(node.func)
        self.write("(")
        self._indent += 1

        total_args = len(node.args + node.keywords)
        for n, item in enumerate(node.args + node.keywords):
            add_comma = n + 1 != total_args
            if first_call:
                self.fill()
            self.traverse(item)

            if add_comma:
                self.write(",")
            if first_call:
                if comment := self._comments.get(n):
                    self.write(f" {comment}")
            elif add_comma:
                self.write(" ")
        self._indent -= 1
        if first_call:
            self.fill()
        self.write(")")


def as_source(node, *, is_multi_line=False, comments=None, next_indent=4):
    indent = node.col_offset
    source = ast.unparse(node)
    if is_multi_line:
        formatted_unparser = _FormattedUnparser(
            indent_width=next_indent, comments=comments
        )
        formatted_unparser._indent = node.col_offset // next_indent
        source = formatted_unparser.visit(node)
    source = " " * indent + source
    if comments is not None and len(comments) >= 1 and not is_multi_line:
        source += " " + comments.popitem()[1]
    return source


def recover_comments(source_lines):
    comments, arg_lines = {}, set()
    with suppress(tokenize.TokenError):
        nesting = -1
        tokens = tuple(tokenize.generate_tokens(iter(source_lines).__next__))
        for index, token in enumerate(tokens):
            if token.string in "([{":
                nesting += 1
            elif token.string in ")]}":
                nesting -= 1

            if nesting == 0 and token.exact_type == tokenize.COMMA:
                arg_lines.add(token.start[0])
            elif nesting == -1 and token.exact_type == tokenize.RPAR:
                arg_lines.add(tokens[index - 1].start[0])

            if token.type == tokenize.COMMENT:
                comments[token.start[0]] = token.string

        return {
            arg_index: comments[arg_line]
            for arg_index, arg_line in enumerate(arg_lines)
            if arg_line in comments
        }


def _adjust_comments(comments, arg_offset):
    for operation, arg_index in enumerate(reversed(comments.copy().keys())):
        if operation > arg_index:
            break
        comment = comments.pop(arg_index)
        comments[arg_index + arg_offset] = comment
    return comments


def rewrite_source(source):
    tree = ast.parse(source)
    rewriter = AssertRewriter()
    rewriter.visit(tree)

    offset_shift = 0
    trailing_newline = source[-1] == "\n"
    for rewrite in rewriter.asserts:
        node = rewrite.node
        lines = source.splitlines()  # todo: ast._splitlines_no_ff
        col_offset = node.col_offset
        start, end = (
            node.lineno - 1 - offset_shift,
            node.end_lineno - offset_shift,
        )
        comments = recover_comments(lines[start:end])
        new_source = as_source(
            rewrite.build_node(),
            is_multi_line=end - 1 - start,
            comments=_adjust_comments(comments, rewrite.get_arg_offset()),
        )
        lines[start:end] = (new_source,)
        source = "\n".join(lines)
        if trailing_newline:
            source += "\n"
        offset_shift += end - len(new_source.splitlines()) - start
    return source, len(rewriter.asserts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--pattern",
        default="test_*.py",
        help="Wildcard pattern for capturing test files.",
    )
    parser.add_argument("--show-stats", action="store_true")
    options = parser.parse_args()

    total_files, total_refactors = 0, 0
    if not options.path.exists():
        raise FileNotFoundError(f"Given path ({options.path}) does not exist")

    for test_file in options.path.glob(options.pattern):
        with tokenize.open(test_file) as file:
            source = file.read()
            encoding = file.encoding
        refactored_source, refactors = rewrite_source(source)
        total_refactors += refactors
        if refactored_source != source:
            test_file.write_text(refactored_source, encoding=encoding)
            total_files += 1

    if options.show_stats:
        print(
            f"{total_refactors} assertions (in {total_files} files) have been refactored."
        )


if __name__ == "__main__":
    main()
