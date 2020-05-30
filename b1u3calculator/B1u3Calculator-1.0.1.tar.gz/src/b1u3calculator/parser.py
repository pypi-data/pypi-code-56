from b1u3calculator import lexer, token, ast

LOWEST = 1
SUM = 2
MINUS = 3
PRODUCT = 4
DIVISION = 5
PREFIX = 6
CALL = 7

precedences = {
        token.PLUS: SUM,
        token.MINUS: SUM,
        token.SLASH: PRODUCT,
        token.ASTER: PRODUCT,
        token.LPAREN: CALL
        }

class Parser():
    parsing_block = False


    def __init__(self, lex):
        self.lexer = lex
        self.errors = []
        self.peek_token = None
        self.next_token()
        self.next_token()
        self.prefix_parse_fns = {}
        self.register_prefix(token.ID, self.parse_identifier)
        self.register_prefix(token.INT, self.parse_integer_literal)
        self.register_prefix(token.MINUS, self.parse_prefix_expression)
        self.register_prefix(token.LPAREN, self.parse_grouped_expression)
        self.infix_parse_fns = {}
        self.register_infix(token.MINUS, self.parse_infix_expression)
        self.register_infix(token.PLUS, self.parse_infix_expression)
        self.register_infix(token.ASTER, self.parse_infix_expression)
        self.register_infix(token.SLASH, self.parse_infix_expression)
        self.register_infix(token.LPAREN, self.parse_call_expression)

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = ast.Program()
        while self.cur_token.type != token.EOF:
            stmt = self.parse_statement()
            if stmt != None:
                program.statements.append(stmt)
            # assert cur_token.type == token.SEMICOLON
            # skip SEMICOLON
            self.next_token()
        return program

    def parse_statement(self):
        """ statement 読み込み self.cur_token が token.SEMICOLON で出てくる """
        if self.cur_token.type == token.ID and self.peek_token.type == token.ASSIGN:
            return self.parse_assign_statement()
        elif self.cur_token.type == token.RETURN:
            return self.parse_return_statement()
        elif self.cur_token.type == token.FUNCTION and not self.parsing_block:
            return self.parse_function_statement()
        else:
            return self.parse_expression_statement()
        return None

    def parse_assign_statement(self):
        # statement は cur_token が SEMICOLON で返ってくるようにする
        stmt = ast.AssignStatement(token=self.cur_token)
        if not self.peek_token_is(token.ASSIGN):
            self.peek_error(token.ASSIGN)
            return None
        stmt.name = ast.Identifier(token=self.cur_token, value=self.cur_token.literal)

        self.next_token()
        self.next_token()

        stmt.value = self.parse_expression(LOWEST)
        if self.peek_token.type == token.SEMICOLON:
            self.next_token()
        return stmt

    def peek_error(self, t):
        self.errors.append(f"expected next token to be {t}, got {self.peek_token.type} instead")

    def peek_token_is(self, typ):
        if self.peek_token.type == typ:
            return True
        else:
            self.peek_error(typ)
            return False

    def cur_token_is(self, typ):
        return self.cur_token.type == typ

    def expect_peek(self, t):
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            return False

    def parse_return_statement(self):
        stmt = ast.ReturnStatement(token=self.cur_token, value=None)
        self.next_token();
        stmt.return_value = self.parse_expression(LOWEST)

        if self.peek_token.type == token.SEMICOLON:
            self.next_token()
        return stmt

    def register_prefix(self, token_type, fn):
        """ fn は引数なし """
        self.prefix_parse_fns[token_type] = fn


    def register_infix(self, token_type, fn):
        """ fn は引数 1 つ """
        self.infix_parse_fns[token_type] = fn

    def parse_expression_statement(self):
        stmt = ast.ExpressionStatement(token=self.cur_token)
        stmt.expression = self.parse_expression(LOWEST)
        if self.peek_token.type == token.SEMICOLON:
            self.next_token()
        return stmt

    def parse_expression(self, precedence):
        try:
            prefix = self.prefix_parse_fns[self.cur_token.type]
        except KeyError:
            self.errors.append(f"no prefix parse function for {self.cur_token.type} found")
            return None
        left_exp = prefix()
        while (not self.peek_token.type == token.SEMICOLON) and precedence < self.peek_precedence():
            try:
                infix = self.infix_parse_fns[self.peek_token.type]
            except KeyError:
                return leftExp
            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def parse_identifier(self):
        return ast.Identifier(token=self.cur_token, value=self.cur_token.literal)

    def parse_integer_literal(self):
            return ast.IntegerLiteral(token=self.cur_token, value=int(self.cur_token.literal))

    def parse_prefix_expression(self):
        exp = ast.PrefixExpression(token=self.cur_token, operator=self.cur_token.literal)
        self.next_token()
        exp.right = self.parse_expression(PREFIX)
        return exp

    def peek_precedence(self):
        try:
            return precedences[self.peek_token.type]
        except KeyError:
            return LOWEST

    def cur_precedence(self):
        try:
            return precedences[self.cur_token.type]
        except KeyError:
            return LOWEST

    def parse_infix_expression(self, left):
        exp = ast.InfixExpression(token=self.cur_token, operator=self.cur_token.literal, left=left)
        precedence = self.cur_precedence()
        self.next_token()
        exp.right = self.parse_expression(precedence)

        return exp


    def parse_grouped_expression(self):
        # skip LPAREN token
        self.next_token()
        exp = self.parse_expression(LOWEST)
        if not self.expect_peek(token.RPAREN):
            return None
        return exp

    def expect_peek(self, typ):
        """ 呼び出した後、Trueだったら、self.cur_tokenがtypのまま戻ってくる"""
        if self.peek_token.type == typ:
            self.next_token()
            return True
        else:
            self.errors.append(f"can't find {typ} token")
            return False

            
    def parse_function_statement(self):
        exp = ast.FunctionStatement(token=self.cur_token)
        self.next_token()
        exp.id = self.parse_identifier()
        if not self.expect_peek(token.LPAREN):
            return None
        exp.parameters = self.parse_parameters()
        if not self.expect_peek(token.LBRACE):
            return None
        exp.block = self.parse_block();
        return exp

    def parse_parameters(self):
        """ 呼び終わった後、cur_token は token.RPAREN """
        ids = []
        # expect_peek はエラーがあるときしか使えない
        if self.peek_token.type == token.RPAREN:
            self.next_token()
            return ids
        self.next_token()
        ident = ast.Identifier(token=self.cur_token, value=self.cur_token.literal)
        ids.append(ident)

        while self.peek_token.type == token.COMMA:
            self.next_token()
            self.next_token()
            ident = ast.Identifier(token=self.cur_token, value=self.cur_token.literal)
            ids.append(ident)
        if not self.expect_peek(token.RPAREN):
            return None
        return ids

    def parse_block(self):
        self.parsing_block = True
        exp = ast.BlockStatement(token=self.cur_token)
        self.next_token()

        while (not (self.cur_token.type == token.RBRACE)) and (not (self.cur_token.type == token.EOF)):
            stmt = self.parse_statement()
            if stmt is not None:
                exp.statements.append(stmt)
            self.next_token()
        if self.cur_token.type != token.RBRACE:
            self.errors.append(f"can't find {token.RBRACE}")

        self.parsing_block = False
        return exp
                

    def parse_call_expression(self, function):
        exp = ast.CallExpression(token=self.cur_token, function=function)
        exp.arguments = self.parse_call_arguments()
        return exp

    def parse_call_arguments(self):
        args = []
        if self.peek_token.type == token.RPAREN:
            # token.LPAREN を飛ばす
            self.next_token()
            return args

        self.next_token()
        args.append(self.parse_expression(LOWEST))
        while self.peek_token.type == token.COMMA:
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(LOWEST))

        if not self.expect_peek(token.RPAREN):
            return None

        return args
