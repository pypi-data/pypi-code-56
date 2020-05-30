from b1u3calculator import token
import string

class Lexer():
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0
        self.read_position = 0
        self.ch = None
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = ""
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        self.skip_whitespace()
        tok = None
        if self.ch == "=":
            tok = token.Token(token.ASSIGN, self.ch)
        elif self.ch == ";":
            tok = token.Token(token.SEMICOLON, self.ch)
        elif self.ch == "(":
            tok = token.Token(token.LPAREN, self.ch)
        elif self.ch == ")":
            tok = token.Token(token.RPAREN, self.ch)
        elif self.ch == "{":
            tok = token.Token(token.LBRACE, self.ch)
        elif self.ch == "}":
            tok = token.Token(token.RBRACE, self.ch)
        elif self.ch == ",":
            tok = token.Token(token.COMMA, self.ch)
        elif self.ch == "+":
            tok = token.Token(token.PLUS, self.ch)
        elif self.ch == "-":
            tok = token.Token(token.MINUS, self.ch)
        elif self.ch == "/":
            tok = token.Token(token.SLASH, self.ch)
        elif self.ch == "*":
            tok = token.Token(token.ASTER, self.ch)
        elif self.ch == "":
            tok = token.Token(token.EOF, self.ch)
        elif self.ch == "　":
            tok = token.Token(token.ILLEGAL, self.ch)
        else:
            if self.ch in list(string.digits):
                tok = token.Token(token.INT, self.read_int())
                return tok
            else:
                literal = self.read_id()
                typ = None
                try:
                    typ = token.lookuptable[literal]
                except KeyError:
                    typ = token.ID
                tok = token.Token(typ, literal)
                return tok
        self.read_char()
        return tok

    def read_int(self):
        position = self.position
        while self.ch in list(string.digits):
            self.read_char()
        return self.input[position:self.position]

    def read_id(self):
        position = self.position
        while self.ch != ' ' and self.ch != '\t' and self.ch != '\r' and self.ch != '\n' and self.ch != ''  and not self.ch in token.reserve_token:
            self.read_char()
        return self.input[position:self.position]

    def skip_whitespace(self):
        while self.ch in [' ', '\t', '\n', '\r']:
            self.read_char()


