from b1u3calculator import lexer, token


class Node():
    def __init__(self, **kwargs):
        for k in kwargs:
            assert type(k) == str
            setattr(self, k, kwargs[k])

    def token_literal(self) -> str:
        raise NotImplementedError()


    def __str__(self):
        return ""


class Statement(Node):
    def statement_node(self):
        raise NotImplementedError()


class ExpressionNode(Node):
    def expression_node(self):
        raise NotImplementedError()


class Program(Node):
    def __init__(self):
        self.statements = []


    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        return '\n'.join([str(s) for s in self.statements])


class AssignStatement(Node):
    token = None
    name = None
    value = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"{str(self.name)} = {str(self.value)};"


class Identifier(ExpressionNode):
    token = None
    "value: store identifier string"
    value = ""


    def expression_node(self):
        # TODO
        super().expression_node()


    def token_literal(self):
        return self.token.literal


    def __str__(self):
        return self.value


class ReturnStatement(Statement):
    token = None
    return_value = None
    def statement_node(self):
        # TODO
        super().statement_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        if self.return_value is not None:
            return f"{self.token_literal()};"
        else:
            return f"{self.token_literal()} {str(self.return_value)};"


class ExpressionStatement(Statement):
    token = None
    expression = None

    def statement_node(self):
        # TODO
        super().statement_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        if self.expression:
            return str(self.expression)
        else:
            return ""


class IntegerLiteral(ExpressionNode):
    token = None
    value = None
    def expression_node(self):
        # TODO
        super().expression_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class PrefixExpression(ExpressionNode):
    token = None
    operator = None
    right = None

    def expression_node(self):
        # TODO
        super().expression_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"({self.operator}{str(self.right)})"

class InfixExpression(ExpressionNode):
    token = None
    operator = None
    right = None
    left = None

    def expression_node(self):
        # TODO
        super().expression_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"({str(self.left)} {self.operator} {str(self.right)})"

class FunctionStatement(Statement):
    token = None
    id = None
    block = None
    parameters = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parameters = []

    def statement_node(self):
        # TODO
        super().statement_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"{self.token.literal} {str(self.id)}({', '.join([str(i) for i in self.parameters])}) {str(self.block)}"


class BlockStatement(Statement):
    statements = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.statements = []

    def statement_node(self):
        # TODO
        super().statement_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return "\n{" + "\n".join([str(s) for s in statements]) + "\n}"

class CallExpression(ExpressionNode):
    token = None
    function = None
    arguments = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arguemtns = []

    def statement_node(self):
        super().statement_node()

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return str(self.function) + f"(" + ", ".join([str(e) for e in self.arguments]) + ")"

