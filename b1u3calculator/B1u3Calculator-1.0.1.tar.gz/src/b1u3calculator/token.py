#reserve 1 characters token
reserve_token = ['=', '+', '-', '*', '/', ',', ';', '(', ')', '{', '}']

ILLEGAL = "ILLEGAL"
EOF = "EOF"
ASSIGN = "="
PLUS = "+"
MINUS = "-"
ASTER = "*"
SLASH = "/"
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
ID = "ID"
INT = "INT"
RETURN = "RETURN"
# keyword
FUNCTION = "def"

lookuptable = {'def': FUNCTION, 'return': RETURN}

class Token():
    def __init__(self, typ, lit):
        self.type = typ
        self.literal = lit
